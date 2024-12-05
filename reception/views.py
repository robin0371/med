import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic import RedirectView

from reception.forms import ReceptionForm
from reception.models import Reception


class CreateReception(CreateView):
    """Представление создания карточки на прием к врачу."""

    model = Reception
    form_class = ReceptionForm
    success_url = '/reception/success'


def reception_success(request):
    """Представление успешного создания карточки на прием к врачу."""
    return render(request, 'reception/reception_success.html')


class CreateReceptionRedirectView(RedirectView):
    """Представление для перенаправления на страницу создания карточки."""

    url = 'reception/new'


def doctor_free_times(request):
    """Представление для получения свободного времени приема врача на дату."""
    doctor_id = int(request.GET['doctor_id'])
    date = datetime.datetime.strptime(request.GET['date'], "%d.%m.%Y")

    busy_time = Reception.objects.filter(
        doctor=doctor_id, date=date).values_list('time', flat=True)


    return HttpResponse(
        json.dumps({'busy_time': [str(bt) for bt in busy_time]}), content_type='application/json')

