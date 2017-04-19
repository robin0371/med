import datetime
import json

from django.core.exceptions import ValidationError
from django.test import TestCase

from reception.models import Doctor, Reception
from reception.tests.utils import get_next_weekday


class AddReceptionCase(TestCase):
    """Набор тестовых случаев создания карточки приема к врачу."""

    def setUp(self):
        Doctor.objects.create(
            name='Иван', surname='Александров', patronymic='Петрович')
        super(AddReceptionCase, self).setUp()

    def test_create_reception(self):
        """Тест создания карточки приема с валидными данными."""
        doctor = Doctor.objects.get(surname='Александров')
        monday = get_next_weekday(datetime.date.today(), 0)
        time = Reception.TIME_CHOICES[0][0]  # 9:00
        patient = 'Иванов Иван Иванович'

        reception = Reception.objects.create(
            doctor=doctor, date=monday, time=time, fio=patient)

        self.assertEqual(reception.fio, patient)
        self.assertEqual(reception.verbose_time, '09:00')

    def test_create_reception_in_day_off(self):
        """Тест создания карточки приема в выходной день."""
        doctor = Doctor.objects.get(surname='Александров')
        saturday = get_next_weekday(datetime.date.today(), 5)
        time = Reception.TIME_CHOICES[0][0]  # 9:00
        patient = 'Иванов Иван Иванович'

        with self.assertRaises(ValidationError):
            reception = Reception(
                doctor=doctor, date=saturday, time=time, fio=patient)
            reception.full_clean()

    def test_create_reception_in_last_day(self):
        """Тест создания карточки приема в прошедший день."""
        doctor = Doctor.objects.get(surname='Александров')
        monday_15_04_2013 = datetime.date(2013, 4, 15)
        time = Reception.TIME_CHOICES[0][0]  # 9:00
        patient = 'Иванов Иван Иванович'

        with self.assertRaises(ValidationError):
            reception = Reception(
                doctor=doctor, date=monday_15_04_2013, time=time, fio=patient)
            reception.full_clean()

    def test_create_reception_in_time_off(self):
        """Тест создания карточки приема в не рабочее время."""
        doctor = Doctor.objects.get(surname='Александров')
        tuesday = get_next_weekday(datetime.date.today(), 1)  # Вторник
        time = 999  # Не рабочее время
        patient = 'Иванов Иван Иванович'

        with self.assertRaises(ValidationError):
            reception = Reception(
                doctor=doctor, date=tuesday, time=time, fio=patient)
            reception.full_clean()

    def test_create_reception_in_busy_time(self):
        """Тест создания карточки приема к врачу в занятое время."""
        doctor = Doctor.objects.get(surname='Александров')
        monday = get_next_weekday(datetime.date.today(), 0)
        time = Reception.TIME_CHOICES[0][0]  # 9:00
        ivanov_ii = 'Иванов Иван Иванович'
        petrov_ad = 'Петров Александр Дмитриевич'

        # Карточка приема пациента Иванова И.И. на понедельник
        # к врачу Александрову И.П. на 9:00
        Reception.objects.create(
            doctor=doctor, date=monday, time=time, fio=ivanov_ii)

        with self.assertRaises(ValidationError):
            reception = Reception(
                doctor=doctor, date=monday, time=time, fio=petrov_ad)
            reception.full_clean()


class SmokeReceptionCase(TestCase):
    """Набор smoke-тестов."""

    def test_new_reception(self):
        """Переход на страницу создания карточки приема к врачу."""
        response = self.client.get('/reception/new/')

        self.assertEqual(response.status_code, 200)

    def test_success_reception(self):
        """Переход на страницу после создания карточки приема к врачу."""
        response = self.client.get('/reception/success/')

        self.assertEqual(response.status_code, 200)

    def test_redirect_to_new_reception(self):
        """Тест представления для перенаправления."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'reception/new')


class ReceptionFreeTimeCase(TestCase):
    """Набор тестов представления получения свободного времени приема врача."""

    def setUp(self):
        Doctor.objects.create(
            name='Иван', surname='Александров', patronymic='Петрович')
        super(ReceptionFreeTimeCase, self).setUp()

    def test_doctor_free_time_busy(self):
        """Тест представления получения свободного времени приема врача.
        
        По условию в понедельник у врача заняты часы приема с 9:00 до 13:00.
        """
        doctor = Doctor.objects.get(surname='Александров')
        monday = get_next_weekday(datetime.date.today(), 0)
        busy_times = (
            Reception.TIME_CHOICES[0][0],  # 9:00
            Reception.TIME_CHOICES[1][0],  # 10:00
            Reception.TIME_CHOICES[2][0],  # 11:00
            Reception.TIME_CHOICES[3][0],  # 12:00
        )
        ivanov_ii = 'Иванов Иван Иванович'

        # Создаем расписание врача Александрова И.П на понедельник,
        # занятое с 9:00 до 13:00
        for time in busy_times:
            Reception.objects.create(
                doctor=doctor, date=monday, time=time, fio=ivanov_ii)

        # Отправляем запрос для получения свободного времени приема врача
        response = self.client.get(
            '/reception/get-free-time-choices/',
            {'doctor_id': doctor.id, 'date': monday.strftime('%d.%m.%Y')})

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(
            response.content,
            b'{"free_time": [[4, "13:00"], [5, "14:00"], [6, "15:00"], '
            b'[7, "16:00"], [8, "17:00"]]}')

        self.assertEqual(
            content['free_time'][0][0], Reception.TIME_CHOICES[4][0])  # 13:00
        self.assertEqual(
            content['free_time'][1][0], Reception.TIME_CHOICES[5][0])  # 14:00
        self.assertEqual(
            content['free_time'][2][0], Reception.TIME_CHOICES[6][0])  # 15:00
        self.assertEqual(
            content['free_time'][3][0], Reception.TIME_CHOICES[7][0])  # 16:00
        self.assertEqual(
            content['free_time'][4][0], Reception.TIME_CHOICES[8][0])  # 17:00

    def test_doctor_free_time(self):
        """Тест представления получения свободного времени приема врача.

        По условию во вторник у врача не заняты часы приема.
        """
        doctor = Doctor.objects.get(surname='Александров')
        tuesday = get_next_weekday(datetime.date.today(), 1)  # Вторник

        # Отправляем запрос для получения свободного времени приема врача
        response = self.client.get(
            '/reception/get-free-time-choices/',
            {'doctor_id': doctor.id, 'date': tuesday.strftime('%d.%m.%Y')})

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(
            response.content,
            b'{"free_time": [[0, "09:00"], [1, "10:00"], [2, "11:00"], '
            b'[3, "12:00"], [4, "13:00"], [5, "14:00"], [6, "15:00"], '
            b'[7, "16:00"], [8, "17:00"]]}')

        self.assertEqual(
            content['free_time'][0][0], Reception.TIME_CHOICES[0][0])  # 09:00
        self.assertEqual(
            content['free_time'][1][0], Reception.TIME_CHOICES[1][0])  # 10:00
        self.assertEqual(
            content['free_time'][2][0], Reception.TIME_CHOICES[2][0])  # 11:00
        self.assertEqual(
            content['free_time'][3][0], Reception.TIME_CHOICES[3][0])  # 12:00
        self.assertEqual(
            content['free_time'][4][0], Reception.TIME_CHOICES[4][0])  # 13:00
        self.assertEqual(
            content['free_time'][5][0], Reception.TIME_CHOICES[5][0])  # 14:00
        self.assertEqual(
            content['free_time'][6][0], Reception.TIME_CHOICES[6][0])  # 15:00
        self.assertEqual(
            content['free_time'][7][0], Reception.TIME_CHOICES[7][0])  # 16:00
        self.assertEqual(
            content['free_time'][8][0], Reception.TIME_CHOICES[8][0])  # 17:00

    def test_doctor_all_busy_time(self):
        """Тест представления получения свободного времени приема врача.

        По условию во вторник у врача заняты все часы приема.
        """
        doctor = Doctor.objects.get(surname='Александров')
        tuesday = get_next_weekday(datetime.date.today(), 1)  # Вторник
        busy_times = (
            Reception.TIME_CHOICES[0][0],  # 9:00
            Reception.TIME_CHOICES[1][0],  # 10:00
            Reception.TIME_CHOICES[2][0],  # 11:00
            Reception.TIME_CHOICES[3][0],  # 12:00
            Reception.TIME_CHOICES[4][0],  # 13:00
            Reception.TIME_CHOICES[5][0],  # 14:00
            Reception.TIME_CHOICES[6][0],  # 15:00
            Reception.TIME_CHOICES[7][0],  # 16:00
            Reception.TIME_CHOICES[8][0],  # 17:00
        )
        ivanov_ii = 'Иванов Иван Иванович'

        # Создаем расписание врача Александрова И.П на вторник,
        # все часы приема заняты.
        for time in busy_times:
            Reception.objects.create(
                doctor=doctor, date=tuesday, time=time, fio=ivanov_ii)

        # Отправляем запрос для получения свободного времени приема врача
        response = self.client.get(
            '/reception/get-free-time-choices/',
            {'doctor_id': doctor.id, 'date': tuesday.strftime('%d.%m.%Y')})

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.content, b'{"free_time": []}')

        self.assertEqual(content['free_time'], [])  # Не свободных часов
