FROM python:3.12
MAINTAINER Lashmanov Vitaly <lashmanov.vitaly@gmail.ru>

ARG APP=/opt/med

COPY ./requirements/base.txt $APP/requirements.txt
RUN pip install -U pip && pip install -r $APP/requirements.txt
ENV DJANGO_SETTINGS_MODULE med.settings

WORKDIR $APP
COPY . $APP
RUN python setup.py install && python manage.py migrate

CMD python manage.py runserver 0.0.0.0:8000
