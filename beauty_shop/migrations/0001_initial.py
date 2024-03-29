# Generated by Django 4.1.3 on 2023-05-23 19:52

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phonenumber', phonenumber_field.modelfields.PhoneNumberField(db_index=True, max_length=128, region=None, verbose_name='Телефон')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Имя')),
                ('surname', models.CharField(blank=True, max_length=200, null=True, verbose_name='Фамилия')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
            },
        ),
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Имя')),
                ('surname', models.CharField(max_length=200, verbose_name='Фамилия')),
                ('profession', models.CharField(max_length=200, verbose_name='Профессия')),
                ('experience', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Стаж с')),
                ('image', models.FileField(blank=True, null=True, upload_to='images/masters', validators=[django.core.validators.FileExtensionValidator(['png', 'jpeg', 'svg'])], verbose_name='Аватарка')),
            ],
            options={
                'verbose_name': 'мастер',
                'verbose_name_plural': 'мастера',
            },
        ),
        migrations.CreateModel(
            name='Salon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('address', models.CharField(db_index=True, max_length=200, unique=True, verbose_name='Адрес')),
                ('latitude', models.FloatField(default=59.940722, verbose_name='Широта')),
                ('longitude', models.FloatField(default=30.396429, verbose_name='Долгота')),
                ('image', models.FileField(blank=True, null=True, upload_to='images/salons', validators=[django.core.validators.FileExtensionValidator(['png', 'jpeg', 'svg'])], verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'салон',
                'verbose_name_plural': 'салоны',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200, unique=True, verbose_name='Название')),
                ('duration', models.TimeField(default=datetime.datetime(1900, 1, 1, 0, 30), verbose_name='Длительность')),
                ('price', models.PositiveSmallIntegerField(verbose_name='Цена')),
                ('image', models.FileField(blank=True, null=True, upload_to='images/services', validators=[django.core.validators.FileExtensionValidator(['png', 'jpeg', 'svg'])], verbose_name='Изображение')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='beauty_shop.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'услуга',
                'verbose_name_plural': 'услуги',
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, verbose_name='Сообщение')),
                ('date_time_start', models.DateTimeField(verbose_name='Начало')),
                ('date_time_end', models.DateTimeField(verbose_name='Конец')),
                ('payment', models.BooleanField(default=False, verbose_name='Оплата')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='beauty_shop.client', verbose_name='Клиента')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='beauty_shop.master', verbose_name='Мастер')),
                ('salon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='beauty_shop.salon', verbose_name='Салон')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='beauty_shop.service', verbose_name='Услуги')),
            ],
            options={
                'verbose_name': 'запись',
                'verbose_name_plural': 'записи',
            },
        ),
        migrations.AddField(
            model_name='master',
            name='salon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='masters', to='beauty_shop.salon', verbose_name='Салон'),
        ),
        migrations.AddField(
            model_name='master',
            name='service',
            field=models.ManyToManyField(related_name='masters', to='beauty_shop.service', verbose_name='Услуги'),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default='5', verbose_name='Оценка')),
                ('text', models.TextField(blank=True, verbose_name='Текст')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='beauty_shop.client', verbose_name='Клиента')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='beauty_shop.master', verbose_name='Мастер')),
            ],
            options={
                'verbose_name': 'отзыв',
                'verbose_name_plural': 'отзывы',
            },
        ),
    ]
