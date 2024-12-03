"""med URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, re_path
from django.contrib import admin

from reception.views import (
    CreateReception, CreateReceptionRedirectView, reception_success,
    doctor_free_times)

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),

    re_path(r'^$', CreateReceptionRedirectView.as_view()),
    re_path(r'^reception/new/', CreateReception.as_view()),
    re_path(r'^reception/success/', reception_success),
    re_path(r'^reception/get-free-time-choices/', doctor_free_times)
]
