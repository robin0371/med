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
