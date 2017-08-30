import uuid
import os
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
        verbose_name = u'Команда'
        verbose_name_plural = u'Команды'


class CrewEvent(models.Model):
    crew = models.ForeignKey(
        Crew,
        verbose_name=u'Команда'
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=u'Время события'
    )
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        verbose_name=u'Пользователь'
    )
    ip = models.GenericIPAddressField(
        default='',
        max_length=60,
        verbose_name=u'IP адрес пользователя'
    )
    host = models.CharField(
        default='',
        max_length=60,
        verbose_name=u'Хост пользователя'
    )
    user_agent = models.CharField(
        default='',
        max_length=200,
        verbose_name=u'Идентификатор браузера'
    )
    message = models.TextField(
        default='',
        verbose_name=u'Событие'
    )

    def __str__(self):
        return self.date.strftime('%Y/%m/%d %H:%M:%S')

    @staticmethod
    def addEvent(request, crew, message):
        if request and crew:
            user = request.user
            if user.is_anonymous:
                user = None
            event = CrewEvent(
                crew=crew,
                user=user,
                ip=request.META['REMOTE_ADDR'],
                host=request.META['REMOTE_HOST'],
                user_agent=request.META['HTTP_USER_AGENT'],
                message=message
            )
            event.save()

    class Meta:
        ordering = ['-date']
        verbose_name = u'Событие в команде'
        verbose_name_plural = u'События в команде'


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
    auto_wait_status = models.BooleanField(
        default=False,
        verbose_name=u'Заявка автоматически переводится в статус "В ожидании"'
    )
    template = models.TextField(
        default='',
        verbose_name=u'Шаблон заявки'
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


class TaskPriority(models.Model):
    crew = models.ForeignKey(
        Crew,
        verbose_name=u'Команда'
    )
    name = models.CharField(
        max_length=200,
        default='',
        verbose_name=u'Наименование'
    )
    time_factor = models.DecimalField(
        default=0,
        max_digits=9,
        decimal_places=2,
        verbose_name=u'Коэффициент времени выполнения'
    )
    cost_factor = models.DecimalField(
        default=0,
        max_digits=9,
        decimal_places=2,
        verbose_name=u'Коэффициент стоимости'
    )
    default = models.BooleanField(
        default=False,
        verbose_name=u'Выбрано по умолчанию'
    )
    deleted = models.BooleanField(
        default=False,
        verbose_name=u'Приоритет удален'
    )

    def __str__(self):
        return '%s [%s %s]' % (self.name, self.time_factor, self.cost_factor)

    class Meta:
        ordering = ['crew', 'name']
        verbose_name = u'Приоритет выполнения'
        verbose_name_plural = u'Приоритеты выполнения'


class CrewTask(models.Model):
    TASK_TYPE_NORMAL = 0
    TASK_TYPE_INCIDENT = 1
    TASK_TYPE_SUBSCRIBE = 2

    TASK_TYPE_CHOICES = (
        (TASK_TYPE_NORMAL, 'Normal'),
        (TASK_TYPE_INCIDENT, 'Incident'),
        (TASK_TYPE_SUBSCRIBE, 'Subscribe'),
    )

    TASK_STATUS_NEW = 0
    TASK_STATUS_WAITING = 1
    TASK_STATUS_PAUSED = 2
    TASK_STATUS_IN_WORK = 3
    TASK_STATUS_CANCELED = 4
    TASK_STATUS_FINISHED = 5
    TASK_STATUS_CLOSED = 6

    TASK_STATUS_CHOICES = (
        (TASK_STATUS_NEW, 'New'),
        (TASK_STATUS_WAITING, 'Waiting'),
        (TASK_STATUS_PAUSED, 'Paused'),
        (TASK_STATUS_IN_WORK, 'In work'),
        (TASK_STATUS_CANCELED, 'Canceled'),
        (TASK_STATUS_FINISHED, 'Finished'),
        (TASK_STATUS_CLOSED, 'Closed')
    )
    uuid = models.CharField(
        max_length=200,
        default='',
        verbose_name=u'Уникальный ключ'
    )
    crew = models.ForeignKey(
        Crew,
        verbose_name=u'Команда'
    )
    type = models.IntegerField(
        choices=TASK_TYPE_CHOICES,
        default=TASK_TYPE_NORMAL,
        verbose_name=u'Тип заявки'
    )
    status = models.IntegerField(
        choices=TASK_STATUS_CHOICES,
        default=TASK_STATUS_NEW,
        verbose_name=u'Статус заявки'
    )
    service = models.ForeignKey(
        CrewService,
        null=True,
        blank=True,
        verbose_name=u'Услуга'
    )
    description = models.TextField(
        default='',
        verbose_name=u'Текстовое описание'
    )
    priority = models.ForeignKey(
        TaskPriority,
        verbose_name=u'Приоритет заявки'
    )
    date_in = models.DateTimeField(
        verbose_name=u'Дата подачи заявки'
    )
    date_end = models.DateTimeField(
        verbose_name=u'Дата окончания подписки'
    )
    date_finish = models.DateTimeField(
        verbose_name=u'Дата выполнения заявки'
    )
    date_close = models.DateTimeField(
        verbose_name=u'Дата закрытия заявки'
    )
    contact_name = models.CharField(
        max_length=200,
        default='',
        verbose_name=u'Имя контакта'
    )
    contact_email = models.CharField(
        max_length=200,
        default='',
        verbose_name=u'Электронный адрес контакта'
    )
    observer = models.ForeignKey(
        User,
        related_name='observer',
        null=True,
        blank=True,
        verbose_name=u'Наблюдатель, подавший заявку'
    )
    dispatcher_in = models.ForeignKey(
        User,
        related_name='dispatcher_in',
        null=True,
        blank=True,
        verbose_name=u'Диспетчер, обработавший новую заявку'
    )
    dispatcher_close = models.ForeignKey(
        User,
        related_name='dispatcher_close',
        null=True,
        blank=True,
        verbose_name=u'Диспетчер, закрывший заявку'
    )
    operator = models.ForeignKey(
        User,
        related_name='operator',
        null=True,
        blank=True,
        verbose_name=u'Оператор, выполнивший заявку'
    )
    qty = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0,
        verbose_name=u'Количество оказанной услуги'
    )
    fine = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0,
        verbose_name=u'Штраф к стоимости, накладываемый администратором'
    )

    def __str__(self):
        return self.uuid

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid1()
        super(CrewTask, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-date_in']
        verbose_name = u'Заявка'
        verbose_name_plural = u'Заявки'


class TaskFiles(models.Model):
    def file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(str(uuid.uuid1()), ext)
        return os.path.join(os.path.join(instance.task.uuid, 'tasks'), filename)

    task = models.ForeignKey(
        CrewTask,
        verbose_name=u'Заявка'
    )
    file = models.FileField(
        blank=True,
        null=True,
        upload_to=file_path,
        verbose_name=u'Вложение'
    )


class TaskEvent(models.Model):
    task = models.ForeignKey(
        CrewTask,
        verbose_name=u'Заявка'
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=u'Время события'
    )
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        verbose_name=u'Пользователь'
    )
    ip = models.GenericIPAddressField(
        default='',
        max_length=60,
        verbose_name=u'IP адрес пользователя'
    )
    host = models.CharField(
        default='',
        max_length=60,
        verbose_name=u'Хост пользователя'
    )
    user_agent = models.CharField(
        default='',
        max_length=200,
        verbose_name=u'Идентификатор браузера'
    )
    message = models.TextField(
        default='',
        verbose_name=u'Событие'
    )

    def __str__(self):
        return self.date.strftime('%Y/%m/%d %H:%M:%S')

    @staticmethod
    def addEvent(request, task, message):
        if request and task:
            user = request.user
            if user.is_anonymous:
                user = None
            event = TaskEvent(
                task=task,
                user=user,
                ip=request.META['REMOTE_ADDR'],
                host=request.META['REMOTE_HOST'],
                user_agent=request.META['HTTP_USER_AGENT'],
                message=message
            )
            event.save()

    class Meta:
        ordering = ['-date']
        verbose_name = u'Событие в заявке'
        verbose_name_plural = u'События в заявке'
