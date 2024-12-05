from django.db import models

from reception.validators import validate_week_day, validate_not_past_date


class Doctor(models.Model):
    """Врач."""

    name = models.CharField('Имя', max_length=50)
    surname = models.CharField('Фамилия', max_length=50)
    patronymic = models.CharField('Отчество', max_length=50)

    class Meta:
        db_table = 'doctors'
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'


class Reception(models.Model):
    """Карточка записи на прием."""

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='К врачу')
    date = models.DateField(
        'Дата', validators=[validate_week_day, validate_not_past_date])
    time = models.TimeField('Время посещения', auto_now_add=False, default='09:00')
    fio = models.CharField('ФИО', max_length=150)

    class Meta:
        db_table = 'receptions'
        verbose_name = 'Карточка приема'
        verbose_name_plural = 'Карточки приема'
        unique_together = 'doctor', 'date', 'time'

    def __str__(self):
        return f'{self.doctor}: {self.date} {self.time}'

