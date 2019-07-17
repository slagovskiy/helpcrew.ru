import uuid
import os
from django.db import models
from ..helpdesk.models import Crew


class Table(models.Model):
    def import_path(instance, filename):
        #ext = filename.split('.')[-1]
        #filename = '{}.{}'.format(str(uuid.uuid1()), ext)
        return os.path.join(os.path.join('import', instance.uuid), filename)

    crew = models.ForeignKey(
        Crew,
        verbose_name=u'Crew',
        on_delete=models.DO_NOTHING
    )
    uuid = models.SlugField(
        unique=True,
        verbose_name=u'Key'
    )
    name = models.CharField(
        max_length=200,
        default='',
        verbose_name=u'Table name'
    )
    deleted = models.BooleanField(
        default=False,
        verbose_name=u'Record is deleted'
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid1()
        super(Table, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = u'Dynamic table'
        verbose_name_plural = u'Dynamic tables'


class Field(models.Model):
    TYPE_NUMERIC = 1
    TYPE_STRING = 2
    TYPE_DATE = 3
    TYPE_IP = 4
    TYPE_PASSWORD = 5
    TYPES = (
        (TYPE_NUMERIC, 'Number'),
        (TYPE_STRING, 'String'),
        (TYPE_DATE, 'Date'),
        (TYPE_IP, 'IP'),
        (TYPE_PASSWORD, 'Password')
    )
    table = models.ForeignKey(
        Table,
        verbose_name=u'Table',
        on_delete=models.DO_NOTHING
    )
    uuid = models.SlugField(
        unique=True,
        verbose_name=u'Key'
    )
    name = models.CharField(
        max_length=50,
        default='',
        verbose_name=u'Field name'
    )
    type = models.IntegerField(
        choices=TYPES,
        default=TYPE_STRING,
        verbose_name=u'Field type'
    )
    order = models.IntegerField(
        default=10,
        verbose_name=u'Sort'
    )
    deleted = models.BooleanField(
        default=False,
        verbose_name=u'Field is deleted'
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid1()
        super(Field, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = u'Table field'
        verbose_name_plural = u'Table fields'


class Index(models.Model):
    table = models.ForeignKey(
        Table,
        verbose_name=u'Table',
        on_delete=models.DO_NOTHING
    )
    num = models.IntegerField(
        default=0,
        verbose_name=u'Row number'
    )
    deleted = models.BooleanField(
        default=False,
        verbose_name=u'Row is deleted'
    )

    def __str__(self):
        return str(self.num)

    class Meta:
        ordering = ['table', 'num']
        verbose_name = u'Row number'
        verbose_name_plural = u'Row numbers'


class Record(models.Model):
    index = models.ForeignKey(
        Index,
        verbose_name=u'Row number',
        on_delete=models.DO_NOTHING
    )
    field = models.ForeignKey(
        Field,
        verbose_name=u'Field',
        on_delete=models.DO_NOTHING
    )
    value = models.CharField(
        max_length=255,
        default='',
        verbose_name=u'Value'
    )

    def __str__(self):
        return self.value

    class Meta:
        ordering = ['index', 'field']
        verbose_name = u'Field value'
        verbose_name_plural = u'Fields values'
