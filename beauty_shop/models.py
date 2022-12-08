import datetime

from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    title = models.CharField(
        verbose_name='Название',
        db_index=True,
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.title


class Salon(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    address = models.CharField(
        verbose_name='Адрес',
        db_index=True,
        max_length=200,
        unique=True,
    )
    latitude = models.FloatField(
        verbose_name='Широта',
        default=59.940722
    )
    longitude = models.FloatField(
        verbose_name='Долгота',
        default=30.396429
    )
    image = models.FileField(
        verbose_name='Изображение',
        blank=True,
        null=True,
        upload_to='images/salons',
        validators=[FileExtensionValidator(['png', 'jpeg', 'svg'])]
    )

    class Meta:
        verbose_name = 'салон'
        verbose_name_plural = 'салоны'

    def __str__(self):
        return self.address


class Service(models.Model):
    title = models.CharField(
        verbose_name='Название',
        db_index=True,
        max_length=200,
        unique=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='services',
    )
    duration = models.TimeField(
        verbose_name='Длительность',
        default=datetime.datetime.strptime('00:30', '%H:%M')
    )
    price = models.PositiveSmallIntegerField(
        verbose_name='Цена'
    )
    image = models.FileField(
        verbose_name='Изображение',
        blank=True,
        null=True,
        upload_to='images/services',
        validators=[FileExtensionValidator(['png', 'jpeg', 'svg'])]
    )

    class Meta:
        verbose_name = 'услуга'
        verbose_name_plural = 'услуги'

    def __str__(self):
        return self.title


class Master(models.Model):
    name = models.CharField(
        verbose_name='Имя',
        max_length=200,
    )
    surname = models.CharField(
        verbose_name='Фамилия',
        max_length=200,
    )
    profession = models.CharField(
        verbose_name='Профессия',
        max_length=200,
    )
    service = models.ManyToManyField(
        Service,
        verbose_name='Услуги',
        related_name='masters',
    )
    salon = models.ForeignKey(
        Salon,
        on_delete=models.SET_NULL,
        verbose_name='Салон',
        blank=True,
        null=True,
        related_name='masters',
    )
    experience = models.DateField(
        verbose_name='Стаж с',
        default=timezone.now,
        blank=True,
        null=True,
    )
    image = models.FileField(
        verbose_name='Аватарка',
        blank=True,
        null=True,
        upload_to='images/masters',
        validators=[FileExtensionValidator(['png', 'jpeg', 'svg'])]
    )

    class Meta:
        verbose_name = 'мастер'
        verbose_name_plural = 'мастера'

    def __str__(self):
        return self.name


class Client(models.Model):
    phonenumber = PhoneNumberField(
        verbose_name='Телефон',
        db_index=True,
        # region='RU',
        # unique=True,
    )
    name = models.CharField(
        verbose_name='Имя',
        max_length=200,
        blank=True,
        null=True,
    )
    surname = models.CharField(
        verbose_name='Фамилия',
        max_length=200,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self):
        return self.name


class Feedback(models.Model):
    ASSESSMENT_CHOICES = (
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
    )

    subject = models.CharField(
        verbose_name='Тема отзыва',
        max_length=200,
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Клиента',
        related_name='feedbacks',
    )
    master = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        verbose_name='Мастер',
        related_name='feedbacks',
    )
    assessment = models.PositiveSmallIntegerField(
        choices=ASSESSMENT_CHOICES,
        default='5',
    )
    text = models.TextField(blank=True)

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        return self.subject


class Note(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Клиента',
        related_name='notes',
    )
    master = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        verbose_name='Мастер',
        related_name='notes',
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='Услуги',
        related_name='notes',
    )
    salon = models.ForeignKey(
        Salon,
        on_delete=models.CASCADE,
        verbose_name='Салон',
        related_name='notes',
    )
    date_time_start = models.DateTimeField(
        verbose_name='Начало',
    )
    date_time_end = models.DateTimeField(
        verbose_name='Конец',
    )

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'записи'

    # def __str__(self):
    #     return self.master
