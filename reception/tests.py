import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from reception.models import Doctor, Reception


def get_next_weekday(date, weekday):
    """Возвращает день weekday из следующей недели.

    :param date: Дата, после которой найти день недели
    :type date: datetime.date
    :param weekday: Порядковый номер дня недели
    :type weekday: int

    :rtype datetime.date
    """
    days_ahead = weekday - date.weekday()
    if days_ahead <= 0:
        days_ahead += 7

    return date + datetime.timedelta(days_ahead)


class AddReceptionCase(TestCase):
    """Набор тестовых случаев создания карточки приема к врачу."""

    def setUp(self):
        Doctor.objects.create(
            name='Иван', surname='Александров', patronymic='Петрович')

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
        tuesday = get_next_weekday(datetime.date.today(), 1)
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

        # Карточка приема пациента Иванова И.И. на понедельник (17.04.2017)
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


class AdminPanelCase(TestCase):
    """Набор тестов панели администрирования."""

    def setUp(self):
        username = 'admin'
        password = User.objects.make_random_password()

        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        self.client.login(username=username, password=password)

    def test_receptions_in_admin_panel(self):
        """Список карточек приема к врачу в админке."""
        doctor = Doctor.objects.create(
            name='Иван', surname='Александров', patronymic='Петрович')
        monday = get_next_weekday(datetime.date.today(), 0)
        time = Reception.TIME_CHOICES[0][0]  # 9:00
        patient = 'Иванов Иван Иванович'

        reception = Reception.objects.create(
            doctor=doctor, date=monday, time=time, fio=patient)

        response = self.client.get('/admin/reception/reception/')

        # Проверка, что успешно прошел переход на страницу списка карточек
        # приема к врачу и на странице есть созданная карточка.
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.rendered_content.find(str(reception)), -1)

    def test_doctors_in_admin_panel(self):
        """Список врачей в админке."""
        Doctor.objects.bulk_create([
            Doctor(name='Иван', surname='Александров', patronymic='Петрович'),
            Doctor(name='Андрей', surname='Петров', patronymic='Петрович')
        ])

        response = self.client.get('/admin/reception/doctor/')

        # Проверка, что успешно прошел переход на страницу списка врачей
        # и на странице есть созданные врачи.
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.rendered_content.find('Александров'), -1)
        self.assertNotEqual(response.rendered_content.find('Петров'), -1)
