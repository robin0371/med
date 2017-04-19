import datetime
import os
import sys
from unittest import skipIf

from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import Select

from reception.models import Doctor, Reception
from reception.tests.utils import get_next_weekday


@skipIf(sys.platform != 'linux', 'For Linux test')
@skipIf(not os.path.exists('/usr/lib/chromium-browser/chromedriver'),
        'not install chromedriver')
class SeleniumNewReceptionFormCase(LiveServerTestCase):
    """Selenium-тесты формы добавления карточки приема к врачу"""

    def setUp(self):
        self.browser = webdriver.Chrome(
            '/usr/lib/chromium-browser/chromedriver')

        Doctor.objects.create(
            name='Иван', surname='Александров', patronymic='Петрович')
        super(SeleniumNewReceptionFormCase, self).setUp()

    def tearDown(self):
        self.browser.quit()
        super(SeleniumNewReceptionFormCase, self).tearDown()

    def test_add_new_reception(self):
        """Тест создания карточки приема с валидными данными."""
        self.browser.get(
            '{0}/{1}'.format(self.live_server_url, 'reception/new'))

        doctor_field = Select(self.browser.find_element_by_id('id_doctor'))
        date_field = self.browser.find_element_by_id('id_date')
        time_field = Select(self.browser.find_element_by_id('id_time'))
        fio_field = self.browser.find_element_by_id('id_fio')
        submit_button = self.browser.find_element_by_tag_name('button')

        doctor = Doctor.objects.get(surname='Александров')
        monday = get_next_weekday(datetime.date.today(), 0)
        time = Reception.TIME_CHOICES[0][0]  # 09:00
        fio = 'Петров Илья Евгеньевич'

        # Заполняем форму
        doctor_field.select_by_visible_text('Александров Иван Петрович')
        date_field.send_keys(monday.strftime('%d.%m.%Y'))
        time_field.select_by_visible_text('09:00')
        fio_field.send_keys(fio)
        # и отправляем
        submit_button.click()

        self.assertEqual(
            self.browser.title, 'Карточка на прием успешно создана')

        reception, created = Reception.objects.get_or_create(
            doctor=doctor, date=monday, time=time, fio=fio)

        self.assertEquals(created, False)

    def test_add_new_reception_day_off(self):
        """Тест создания карточки приема в выходной день."""
        self.browser.get(
            '{0}/{1}'.format(self.live_server_url, 'reception/new'))

        doctor_field = Select(self.browser.find_element_by_id('id_doctor'))
        date_field = self.browser.find_element_by_id('id_date')
        time_field = Select(self.browser.find_element_by_id('id_time'))
        fio_field = self.browser.find_element_by_id('id_fio')
        submit_button = self.browser.find_element_by_tag_name('button')

        doctor = Doctor.objects.get(surname='Александров')
        saturday = get_next_weekday(datetime.date.today(), 5)
        time = Reception.TIME_CHOICES[0][0]  # 09:00
        fio = 'Петров Илья Евгеньевич'

        # Заполняем форму
        doctor_field.select_by_visible_text('Александров Иван Петрович')
        date_field.send_keys(saturday.strftime('%d.%m.%Y'))
        time_field.select_by_visible_text('09:00')
        fio_field.send_keys(fio)
        # и отправляем
        submit_button.click()

        alert_div = self.browser.find_element_by_class_name('alert')
        self.assertEqual(
            alert_div.text, '×\nВыбранная дата - {0}, является выходным днем.'
                            ''.format(saturday))

        with self.assertRaises(Reception.DoesNotExist):
            Reception.objects.get(
                doctor=doctor, date=saturday, time=time, fio=fio)

    def test_add_new_reception_in_last_day(self):
        """Тест создания карточки приема в прошедший день."""
        self.browser.get(
            '{0}/{1}'.format(self.live_server_url, 'reception/new'))

        doctor_field = Select(self.browser.find_element_by_id('id_doctor'))
        date_field = self.browser.find_element_by_id('id_date')
        time_field = Select(self.browser.find_element_by_id('id_time'))
        fio_field = self.browser.find_element_by_id('id_fio')
        submit_button = self.browser.find_element_by_tag_name('button')

        doctor = Doctor.objects.get(surname='Александров')
        monday_15_04_2013 = datetime.date(2013, 4, 15)
        time = Reception.TIME_CHOICES[0][0]  # 09:00
        fio = 'Петров Илья Евгеньевич'

        # Заполняем форму
        doctor_field.select_by_visible_text('Александров Иван Петрович')
        date_field.send_keys(monday_15_04_2013.strftime('%d.%m.%Y'))
        time_field.select_by_visible_text('09:00')
        fio_field.send_keys(fio)
        # и отправляем
        submit_button.click()

        alert_div = self.browser.find_element_by_class_name('alert')
        self.assertEqual(
            alert_div.text, '×\nВыбранная дата - {0}, уже прошла.'
                            ''.format(monday_15_04_2013))

        with self.assertRaises(Reception.DoesNotExist):
            Reception.objects.get(
                doctor=doctor, date=monday_15_04_2013, time=time, fio=fio)

    def test_add_new_reception_in_time_off(self):
        """Тест создания карточки приема в не рабочее время."""
        self.browser.get(
            '{0}/{1}'.format(self.live_server_url, 'reception/new'))

        doctor_field = Select(self.browser.find_element_by_id('id_doctor'))
        date_field = self.browser.find_element_by_id('id_date')
        time_field = Select(self.browser.find_element_by_id('id_time'))
        fio_field = self.browser.find_element_by_id('id_fio')
        submit_button = self.browser.find_element_by_tag_name('button')

        doctor = Doctor.objects.get(surname='Александров')
        tuesday = get_next_weekday(datetime.date.today(), 1)  # Вторник
        time = 999  # Не рабочее время
        fio = 'Петров Илья Евгеньевич'

        # Заполняем форму
        doctor_field.select_by_visible_text('Александров Иван Петрович')
        date_field.send_keys(tuesday.strftime('%d.%m.%Y'))
        time_field.select_by_visible_text('09:00')
        fio_field.send_keys(fio)
        # и отправляем
        submit_button.click()

        with self.assertRaises(Reception.DoesNotExist):
            Reception.objects.get(
                doctor=doctor, date=tuesday, time=time, fio=fio)

    def test_add_new_reception_in_busy_time(self):
        """Тест создания карточки приема к врачу в занятое время."""
        self.browser.get(
            '{0}/{1}'.format(self.live_server_url, 'reception/new'))

        doctor_field = Select(self.browser.find_element_by_id('id_doctor'))
        date_field = self.browser.find_element_by_id('id_date')
        time_field = Select(self.browser.find_element_by_id('id_time'))
        fio_field = self.browser.find_element_by_id('id_fio')
        submit_button = self.browser.find_element_by_tag_name('button')

        doctor = Doctor.objects.get(surname='Александров')
        monday = get_next_weekday(datetime.date.today(), 0)
        time = Reception.TIME_CHOICES[0][0]  # 9:00
        ivanov_ii = 'Иванов Иван Иванович'
        petrov_ad = 'Петров Александр Дмитриевич'

        # Карточка приема пациента Иванова И.И. на понедельник
        # к врачу Александрову И.П. на 9:00
        Reception.objects.create(
            doctor=doctor, date=monday, time=time, fio=ivanov_ii)

        # Заполняем форму
        doctor_field.select_by_visible_text('Александров Иван Петрович')
        date_field.send_keys(monday.strftime('%d.%m.%Y'))
        time_field.select_by_visible_text('09:00')
        fio_field.send_keys(petrov_ad)
        # и отправляем
        submit_button.click()

        alert_div = self.browser.find_element_by_class_name('alert')
        self.assertEqual(
            alert_div.text, '×\nКарточка приема с такими значениями полей '
                            'К врачу, Дата и Время уже существует.')

        with self.assertRaises(Reception.DoesNotExist):
            Reception.objects.get(
                doctor=doctor, date=monday, time=time, fio=petrov_ad)

