import os
from pip.download import PipSession
from pip.req.req_file import parse_requirements
from setuptools import setup


def get_requirements(file_name):
    """Возвращает список зависимостей med."""
    requirements = parse_requirements(file_name, session=PipSession())
    return [str(ir.req) for ir in requirements]


def read(file_name):
    """Возвращает текст файла."""
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name='med',
    version='0.1',
    description='Приложение формы записи к врачу',
    long_description=read('README.rst'),
    install_requires=get_requirements('requirements/base.txt'),
    license='MIT License',
    keywords='med form reception',
    author='Lashmanov Vitaly',
    author_email='lashmanov.vitaly@gmail.ru',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Customer Service',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
