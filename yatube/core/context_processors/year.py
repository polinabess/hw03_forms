import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    return {
        'year_now': datetime.datetime.now().year
    }
