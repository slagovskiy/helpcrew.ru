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

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid1()
        super(Table, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = u'Динамическая таблица'
        verbose_name_plural = u'Динамические таблицы'
