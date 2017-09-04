import uuid
from django.db import models
from ..helpdesk.models import Crew


class Table(models.Model):
    crew = models.ForeignKey(
        Crew,
        verbose_name=u'Команда'
    )
    uuid = models.SlugField(
        unique=True,
        verbose_name=u'Ключ'
    )
    name = models.CharField(
        max_length=200,
        default='',
        verbose_name=u'Имя таблицы'
    )
    deleted = models.BooleanField(
        default=False,
        verbose_name=u'Запись удалена'
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid1()
        super(Table, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = u'Динамическая таблица'
        verbose_name_plural = u'Динамические таблицы'


class Field(models.Model):
    TYPE_NUMERIC = 1
    TYPE_STRING = 2
    TYPE_DATE = 3
    TYPE_IP = 4
    TYPE_PASSWORD = 5
    TYPES = (
        (TYPE_NUMERIC, 'Число'),
        (TYPE_STRING, 'Строка'),
        (TYPE_DATE, 'Дата'),
        (TYPE_IP, 'IP'),
        (TYPE_PASSWORD, 'Пароль')
    )
    table = models.ForeignKey(
        Table,
        verbose_name=u'Таблица'
    )
    uuid = models.SlugField(
        unique=True,
        verbose_name=u'Ключ'
    )
    name = models.CharField(
        max_length=50,
        default='',
        verbose_name=u'Наименование поля'
    )
    type = models.IntegerField(
        choices=TYPES,
        default=TYPE_STRING,
        verbose_name=u'Тип поля'
    )
    order = models.IntegerField(
        default=10,
        verbose_name=u'Сортировка'
    )
    deleted = models.BooleanField(
        default=False,
        verbose_name=u'Запись удалена'
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid1()
        super(Field, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = u'Поле таблицы'
        verbose_name_plural = u'Поля таблицы'
