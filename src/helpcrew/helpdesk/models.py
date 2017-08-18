import uuid
from django.db import models

from ..toolbox.models import Global
from ..userext.models import User


class Crew(models.Model):
    slug = models.SlugField(
        unique=True,
        verbose_name=u'Ключ'
    )
    name = models.CharField(
        default='',
        max_length=255,
        verbose_name=u'Название команды'
    )
    url = models.CharField(
        default='',
        max_length=255,
        verbose_name=u'Ссылка'
    )
    user = models.ForeignKey(
        User,
        verbose_name=u'Создатель команды'
    )
    added = models.DateTimeField(
        auto_now_add=True
    )
    deleted = models.BooleanField(
        default=False,
        verbose_name=u'Команда удалена'
    )
    crew_user_limit = models.IntegerField(
        default=0,
        verbose_name=u'Ограничение на количество членов команды'
    )
    start_task = models.IntegerField(default=0)
    incident_time_one = models.IntegerField(default=0)
    incident_time_two = models.IntegerField(default=0)
    request_time_one = models.IntegerField(default=0)
    request_time_two = models.IntegerField(default=0)

    def __str__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid1()
            self.crew_user_limit = Global.get('crew_user_limit')
            self.start_task = Global.get('start_task')
            self.incident_time_one = Global.get('incident_time_one')
            self.incident_time_two = Global.get('incident_time_two')
            self.request_time_one = Global.get('request_time_one')
            self.request_time_two = Global.get('request_time_two')
        super(Crew, self).save(*args, **kwargs)

    @staticmethod
    def exist_url(url):
        c = Crew.objects.filter(url=url)
        if c:
            return True
        else:
            return False


    class Meta:
        ordering = ['name']
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'


class CrewUsers(models.Model):
    ADMINISTRATOR_TYPE = 0
    DISPATCHER_TYPE = 1
    OPERATOR_TYPE = 2

    USER_TYPE_CHOICES = (
        (ADMINISTRATOR_TYPE, 'Administrator'),
        (DISPATCHER_TYPE, 'Dispatcher'),
        (OPERATOR_TYPE, 'Operator'),
    )

    crew = models.ForeignKey(
        Crew,
        verbose_name=u'Команда'
    )
    user = models.ForeignKey(
        User,
        verbose_name=u'Пользователь'
    )
    type = models.IntegerField(
        choices=USER_TYPE_CHOICES,
        default=OPERATOR_TYPE,
        verbose_name=u'Уровеь доступа'
    )
    deleted = models.BooleanField(
        default=False,
        verbose_name=u'Член команды удален'
    )

    def __str__(self):
        return '%s %s' % (self.crew, self.user)

    class Meta:
        ordering = ['type', 'user']
        verbose_name = 'Член команды'
        verbose_name_plural = 'Члены команд'


class CrewService(models.Model):
    crew = models.ForeignKey(Crew, verbose_name=u'Команда')
    name = models.CharField(
        max_length=200,
        default='',
        verbose_name=u'Наименование'
    )
    time1 = models.IntegerField(
        default=10,
        verbose_name=u'Время первой реакции'
    )
    time2 = models.IntegerField(
        default=48,
        verbose_name=u'Время на завершение заявки'
    )
    time3 = models.IntegerField(
        default=480,
        verbose_name=u'Время провала заявки'
    )
    unit = models.CharField(
        max_length=50,
        default='',
        verbose_name=u'Единица измерения'
    )
    deleted = models.BooleanField(
        default=False,
        verbose_name=u'Услуга удалена'
    )

    def __str__(self):
        return '%s %s' % (self.crew, self.name)

    class Meta:
        ordering = ['crew', 'name']
        verbose_name = u'Услуга'
        verbose_name_plural = u'Услуги'


class ServicePrice(models.Model):
    service = models.ForeignKey(
        CrewService,
        verbose_name=u'Услуга'
    )
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=u'Дата начала тействия цены'
    )
    cost = models.DecimalField(
        default=0,
        max_digits=9,
        decimal_places=2,
        verbose_name=u'Стоимость услуги'
    )
    prepay = models.DecimalField(
        default=0,
        max_digits=9,
        decimal_places=2,
        verbose_name=u'Предоплата'
    )
    fine1 = models.DecimalField(
        default=0,
        max_digits=9,
        decimal_places=2,
        verbose_name=u'Штраф за невыполнение заявки в срок'
    )
    fine2 = models.DecimalField(
        default=0,
        max_digits=9,
        decimal_places=2,
        verbose_name=u'Штраф за просроченную заявку'
    )

    def __str__(self):
        return '%s %s %s' % (self.service, self.start_date, self.cost)

    class Meta:
        ordering = ['service', 'start_date']
        verbose_name = u'Строимость услуги'
        verbose_name_plural = u'Стоимость услуг'
