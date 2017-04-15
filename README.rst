Приложение "Форма для записи на прием к врачу"
==============================================


Стандартный запуск
++++++++++++++++++

Устанавливаем зависимости и запускаем с указанием пути к файлу настроек:

.. code:: shell

    $ cd /path/to/med
    $ source /venv/bin/activate
    $ pip install -r requirements/base.txt
    $ python manage.py runserver


В Docker-контейнере
+++++++++++++++++++

Так как образы нигде не хранятся, сначала создадим docker-образ, а затем
запустим контейнер из него.

.. code:: shell

    $ cd /path/to/med
    $ sudo docker build -t python/med:0.1 .
    $ sudo docker run -t -i -d -p 127.0.0.1:80:8000 python/med:0.1


После выполнения этих команд, приложение будет доступно по адресу
http://127.0.0.1, на 80 порту.


Запуск тестов
+++++++++++++

.. code:: shell

    $ source /venv/bin/activate
    $ cd /path/to/med
    $ pip install -r requirements/test.txt
    $ coverage run --source='.' manage.py test reception
    $ coverage report
    $ coverage html