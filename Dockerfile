FROM python:3.12
MAINTAINER Lashmanov Vitaly <lashmanov.vitaly@gmail.ru>

ARG APP=/opt/med

RUN useradd -ms /bin/bash med
ENV PATH="${PATH}:/home/med/.local/bin"
USER med

COPY --chown=med:med ./requirements/base.txt $APP/requirements.txt
RUN pip install -U pip && pip install --user -r $APP/requirements.txt
ENV DJANGO_SETTINGS_MODULE med.settings

WORKDIR $APP
COPY --chown=med:med . $APP
RUN pip install . && python manage.py migrate

CMD python manage.py runserver 0.0.0.0:8000
