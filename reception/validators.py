import datetime

from django.core.exceptions import ValidationError


def validate_week_day(date):
    """Валидирует дату.

    :param date: Дата
    :type date: datetime.date

    :raise django.core.exceptions.ValidationError
    """
    # Проверяем, что дата не является выходным днем
    if date.weekday() in (5, 6):
        raise ValidationError(
            'Выбранная дата - {date}, является выходным днем.'.format(
                date=date)
        )


def validate_not_past_date(date):
    """Валидирует дату.

    :param date: Дата
    :type date: datetime.date

    :raise django.core.exceptions.ValidationError
    """
    # Проверяем, что дата не меньше сегодняшней
    if date < datetime.date.today():
        raise ValidationError(
            'Выбранная дата - {date}, уже прошла.'.format(date=date)
        )
