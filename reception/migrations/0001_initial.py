# Generated by Django 5.1.3 on 2024-12-05 18:49

import django.db.models.deletion
import reception.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('surname', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('patronymic', models.CharField(max_length=50, verbose_name='Отчество')),
            ],
            options={
                'verbose_name': 'Врач',
                'verbose_name_plural': 'Врачи',
                'db_table': 'doctors',
            },
        ),
        migrations.CreateModel(
            name='Reception',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(validators=[reception.validators.validate_week_day, reception.validators.validate_not_past_date], verbose_name='Дата')),
                ('time', models.TimeField(default='09:00', verbose_name='Время посещения')),
                ('fio', models.CharField(max_length=150, verbose_name='ФИО')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reception.doctor', verbose_name='К врачу')),
            ],
            options={
                'verbose_name': 'Карточка приема',
                'verbose_name_plural': 'Карточки приема',
                'db_table': 'receptions',
                'unique_together': {('doctor', 'date', 'time')},
            },
        ),
    ]
