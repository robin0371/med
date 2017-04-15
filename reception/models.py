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
        return '{self.surname} {self.name} {self.patronymic}'.format(self=self)


class Reception(models.Model):
    """Карточка записи на прием."""

    TIME_CHOICES = (
        (0, '09:00'),
        (1, '10:00'),
        (2, '11:00'),
        (3, '12:00'),
        (4, '13:00'),
        (5, '14:00'),
        (6, '15:00'),
        (7, '16:00'),
        (8, '17:00'),
    )

    doctor = models.ForeignKey(Doctor, verbose_name='К врачу')
    date = models.DateField(
        'Дата', validators=[validate_week_day, validate_not_past_date])
    time = models.PositiveSmallIntegerField('Время', choices=TIME_CHOICES)
    fio = models.CharField('ФИО', max_length=150)

    class Meta:
        db_table = 'receptions'
        verbose_name = 'Карточка приема'
        verbose_name_plural = 'Карточки приема'
        unique_together = 'doctor', 'date', 'time'

    def __str__(self):
        return '{self.doctor}: {self.date} {self.verbose_time}'.format(
            self=self)

    @property
    def verbose_time(self):
        return dict(self.TIME_CHOICES).get(self.time)
