FROM python:3.5
MAINTAINER Lashmanov Vitaly <lashmanov.vitaly@gmail.ru>

COPY . /opt/med

WORKDIR /opt/med

ENV DJANGO_SETTINGS_MODULE med.settings

RUN pip install -U pip
RUN pip install -r requirements/base.txt
RUN python setup.py install

CMD python manage.py runserver 0.0.0.0:8000