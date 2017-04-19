import datetime


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
