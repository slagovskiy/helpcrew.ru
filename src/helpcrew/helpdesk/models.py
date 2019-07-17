import uuid
import os
from django.utils import timezone
import datetime
from holidays import HolidayBase
import pytz
import businesstimedelta
from django.db import models

from ..toolbox.utils import getUserHostAddress
from ..toolbox.models import Global
from ..userext.models import User


class Crew(models.Model):
    def logo_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(str(uuid.uuid1()), ext)
        return os.path.join(os.path.join('crew', instance.slug), filename)

    slug = models.SlugField(
        unique=True,
        verbose_name=u'Key'
    )
    name = models.CharField(
        default='',
        max_length=255,
        verbose_name=u'Crew name'
    )
    url = models.CharField(
        default='',
        max_length=255,
        verbose_name=u'Crew link'
    )
    user = models.ForeignKey(
        User,
        verbose_name=u'Crew creator',
        on_delete=models.DO_NOTHING
    )
    added = models.DateTimeField(
        auto_now_add=True
    )
    order = models.IntegerField(
        default=10000,
        verbose_name=u'Sort'
    )
    logo = models.ImageField(
        'Logo',
        blank=True,
        null=True,
        upload_to=logo_path
    )
    description = models.TextField(
        default='',
        verbose_name=u'Description'
    )
    user_page = models.TextField(
        default='',
        verbose_name=u'Description for user'
    )
    password = models.CharField(
        default='',
        max_length=255,
        verbose_name=u'Password for add tasks'
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name=u'Show crew in crew list'
    )
    deleted = models.BooleanField(
        default=False,
        verbose_name=u'Crew is deleted'
    )
    crew_user_limit = models.IntegerField(
        default=0,
        verbose_name=u'Limit on the number of crew members'
    )
    work_start_time = models.CharField(
        default='9:00',
        max_length=5,
        verbose_name=u'The begining of the work day'
    )
    work_end_time = models.CharField(
        default='18:00',
        max_length=5,
        verbose_name=u'The end of the working day'
    )
    work_day_0 = models.BooleanField(
        default=True,
        verbose_name=u'Working day 0'
    )
    work_day_1 = models.BooleanField(
        default=True,
        verbose_name=u'Working day 1'
    )
    work_day_2 = models.BooleanField(
        default=True,
        verbose_name=u'Working day 2'
    )
    work_day_3 = models.BooleanField(
        default=True,
        verbose_name=u'Working day 3'
    )
    work_day_4 = models.BooleanField(
        default=True,
        verbose_name=u'Working day 4'
    )
    work_day_5 = models.BooleanField(
        default=False,
        verbose_name=u'Working day 5'
    )
    work_day_6 = models.BooleanField(
        default=False,
        verbose_name=u'Working day 6'
    )
    lunch_start_time = models.CharField(
        default='13:00',
        max_length=5,
        verbose_name=u'Start of lunch break'
    )
    lunch_end_time = models.CharField(
        default='14:00',
        max_length=5,
        verbose_name=u'The end of the lunch break'
    )
    holidays = models.TextField(
        default='',
        verbose_name=u'Holidays'
    )
    start_task = models.IntegerField(default=0)
    incident_time_one = models.IntegerField(default=0)
    incident_time_two = models.IntegerField(default=0)
    request_time_one = models.IntegerField(default=0)
    request_time_two = models.IntegerField(default=0)

    def __str__(self):
        return '%s' % self.name

    def user_setting(self, user):
        return self.crewusers_set.filter(user=user).first()

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
        ordering = ['order', 'name']
        verbose_name = u'Crew'
        verbose_name_plural = u'Crews'


class CrewEvent(models.Model):
    crew = models.ForeignKey(
        Crew,
        verbose_name=u'Crew',
        on_delete=models.DO_NOTHING
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=u'Event time'
    )
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        verbose_name=u'User',
        on_delete=models.SET_NULL
    )
    ip = models.GenericIPAddressField(
        default='',
        max_length=60,
        verbose_name=u'User ip address'
    )
    user_agent = models.CharField(
        default='',
        max_length=200,
        verbose_name=u'User agent name'
    )
    message = models.TextField(
        default='',
        verbose_name=u'Event'
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
                ip=getUserHostAddress(request),
                user_agent=request.META['HTTP_USER_AGENT'],
                message=message
            )
            event.save()

    class Meta:
        ordering = ['-date']
        verbose_name = u'Crew event'
        verbose_name_plural = u'Crew events'


class CrewUsers(models.Model):
    ADMINISTRATOR_TYPE = 0
    DISPATCHER_TYPE = 1
    OPERATOR_TYPE = 2
    OBSERVER_TYPE = 3

    USER_TYPE_CHOICES = (
        (ADMINISTRATOR_TYPE, 'Administrator'),
        (DISPATCHER_TYPE, 'Dispatcher'),
        (OPERATOR_TYPE, 'Operator'),
        (OBSERVER_TYPE, 'Observer')
    )

    crew = models.ForeignKey(
        Crew,
        verbose_name=u'Crew',
        on_delete=models.DO_NOTHING
    )
    user = models.ForeignKey(
        User,
        verbose_name=u'User',
        on_delete=models.DO_NOTHING
    )
    type = models.IntegerField(
        choices=USER_TYPE_CHOICES,
        default=OPERATOR_TYPE,
        verbose_name=u'Type of user'
    )
    deleted = models.BooleanField(
        default=False,
        verbose_name=u'User is deleted'
    )

    dtable_filter = models.BooleanField(default=True)
    dtable_paging = models.BooleanField(default=True)
    dtable_page_size = models.IntegerField(default=100)

    task_show_closed = models.BooleanField(default=True)
    task_show_canceled = models.BooleanField(default=True)
    task_filter = models.BooleanField(default=True)
    task_paging = models.BooleanField(default=True)
    task_page_size = models.IntegerField(default=100)

    def __str__(self):
        return '%s %s' % (self.crew, self.user)

    class Meta:
        ordering = ['type', 'user']
        verbose_name = 'Crew user'
        verbose_name_plural = 'Crew users'


class CrewService(models.Model):
    crew = models.ForeignKey(
        Crew,
        verbose_name=u'Crew',
        on_delete=models.DO_NOTHING
    )
    name = models.CharField(
        max_length=200,
        default='',
        verbose_name=u'Service name'
    )
    time1 = models.IntegerField(
        default=10,
        verbose_name=u'First reaction time'
    )
    time2 = models.IntegerField(
        default=48,
        verbose_name=u'Time to complete the task'
    )
    time3 = models.IntegerField(
        default=480,
        verbose_name=u'Time of failure'
    )
    unit = models.CharField(
        max_length=50,
        default='',
        verbose_name=u'Unit'
    )
    auto_wait_status = models.BooleanField(
        default=False,
        verbose_name=u'The task is automatically transferred to the status of "Pending"'
    )
    template = models.TextField(
        default='',
        verbose_name=u'Task template'
    )
    deleted = models.BooleanField(
        default=False,
        verbose_name=u'Service is deleted'
    )

    def __str__(self):
        return '%s %s' % (self.crew, self.name)

    class Meta:
        ordering = ['crew', 'name']
        verbose_name = u'Service'
        verbose_name_plural = u'Services'


class ServicePrice(models.Model):
    service = models.ForeignKey(
        CrewService,
        verbose_name=u'Service',
        on_delete=models.DO_NOTHING
    )
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=u'Starting date of the price'
    )
    cost = models.DecimalField(
        default=0,
        max_digits=9,
        decimal_places=2,
        verbose_name=u'Service cost'
    )
    prepay = models.DecimalField(
        default=0,
        max_digits=9,
        decimal_places=2,
        verbose_name=u'Prepayment'
    )
    fine1 = models.DecimalField(
        default=0,
        max_digits=9,
        decimal_places=2,
        verbose_name=u'Fine for not completing the application on time'
    )
    fine2 = models.DecimalField(
        default=0,
        max_digits=9,
        decimal_places=2,
        verbose_name=u'Fine for overdue application'
    )

    def __str__(self):
        return '%s %s %s' % (self.service, self.start_date, self.cost)

    class Meta:
        ordering = ['service', 'start_date']
        verbose_name = u'Service price'
        verbose_name_plural = u'Services price'


class TaskPriority(models.Model):
    crew = models.ForeignKey(
        Crew,
        verbose_name=u'Crew',
        on_delete=models.DO_NOTHING
    )
    name = models.CharField(
        max_length=200,
        default='',
        verbose_name=u'Priority name'
    )
    time_factor = models.DecimalField(
        default=0,
        max_digits=9,
        decimal_places=2,
        verbose_name=u'Time factor'
    )
    cost_factor = models.DecimalField(
        default=0,
        max_digits=9,
        decimal_places=2,
        verbose_name=u'Cost factor'
    )
    default = models.BooleanField(
        default=False,
        verbose_name=u'Selected by default'
    )
    deleted = models.BooleanField(
        default=False,
        verbose_name=u'Priority is deleted'
    )

    def __str__(self):
        return '%s [%s %s]' % (self.name, self.time_factor, self.cost_factor)

    class Meta:
        ordering = ['crew', 'time_factor']
        verbose_name = u'Execution priority'
        verbose_name_plural = u'Execution priorities'


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
        verbose_name=u'Key'
    )
    crew = models.ForeignKey(
        Crew,
        verbose_name=u'Crew',
        on_delete=models.DO_NOTHING
    )
    type = models.IntegerField(
        choices=TASK_TYPE_CHOICES,
        default=TASK_TYPE_NORMAL,
        verbose_name=u'Task type'
    )
    status = models.IntegerField(
        choices=TASK_STATUS_CHOICES,
        default=TASK_STATUS_NEW,
        verbose_name=u'Task status'
    )
    service = models.ForeignKey(
        CrewService,
        null=True,
        blank=True,
        verbose_name=u'Service',
        on_delete=models.SET_NULL
    )
    description = models.TextField(
        default='',
        verbose_name=u'Description'
    )
    commentary = models.TextField(
        default='',
        verbose_name=u'Commentary'
    )
    priority = models.ForeignKey(
        TaskPriority,
        verbose_name=u'Execution priority',
        on_delete=models.DO_NOTHING
    )
    date_in = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'In date'
    )
    date_work = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Start work date'
    )
    date_end = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'End of subscribe'
    )
    date_finish = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'End of work date'
    )
    date_close = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Close date'
    )
    contact_name = models.CharField(
        max_length=200,
        default='',
        verbose_name=u'Contact name'
    )
    contact_email = models.CharField(
        max_length=200,
        default='',
        verbose_name=u'Contact email'
    )
    qty = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0,
        verbose_name=u'Quantity'
    )
    fine = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0,
        verbose_name=u'The fine to the cost imposed by the administrator'
    )

    def __str__(self):
        return self.uuid

    def user_observer(self):
        _user = self.taskusers_set.filter(type=TaskUsers.OBSERVER_TYPE).first()
        if _user:
            return _user.user
        else:
            return None

    def user_dispatcher(self):
        _user = self.taskusers_set.filter(type=TaskUsers.DISPATCHER_TYPE).first()
        if _user:
            return _user.user
        else:
            return None

    def user_operator(self):
        _user = self.taskusers_set.filter(type=TaskUsers.OPERATOR_TYPE)
        _rez = []
        for __user in _user:
            _rez.append(__user.user)
        return _rez

    def user_close(self):
        _user = self.taskusers_set.filter(type=TaskUsers.CLOSE_TYPE).first()
        if _user:
            return _user.user
        else:
            return None

    def date_prepare(self):
        working_days = []
        if self.crew.work_day_0:
            working_days.append(0)
        if self.crew.work_day_1:
            working_days.append(1)
        if self.crew.work_day_2:
            working_days.append(2)
        if self.crew.work_day_3:
            working_days.append(3)
        if self.crew.work_day_4:
            working_days.append(4)
        if self.crew.work_day_5:
            working_days.append(5)
        if self.crew.work_day_6:
            working_days.append(6)

        workday = businesstimedelta.WorkDayRule(
            start_time=datetime.time(
                int(self.crew.work_start_time.split(':')[0]),
                int(self.crew.work_start_time.split(':')[1])
            ),
            end_time=datetime.time(
                int(self.crew.work_end_time.split(':')[0]),
                int(self.crew.work_end_time.split(':')[1]),
            ),
            working_days=working_days,
            tz=timezone.get_current_timezone()
        )

        lunchbreak = businesstimedelta.LunchTimeRule(
            start_time=datetime.time(
                int(self.crew.lunch_start_time.split(':')[0]),
                int(self.crew.lunch_start_time.split(':')[1]),
            ),
            end_time=datetime.time(
                int(self.crew.lunch_end_time.split(':')[0]),
                int(self.crew.lunch_end_time.split(':')[1]),
            ),
            working_days=working_days,
            tz=timezone.get_current_timezone()
        )

        _holidays = HolidayBase()
        btd = None

        # not work!
        '''
        if self.crew.holidays:
            for day in self.crew.holidays.split('\n'):
                if day != '':
                    _holidays.append({day: 'day'})
            holidays = businesstimedelta.HolidayRule(
                holidays=_holidays,
                tz=timezone.get_current_timezone()
            )
            btd = businesstimedelta.Rules([workday, lunchbreak, holidays])
        else:
            btd = businesstimedelta.Rules([workday, lunchbreak])
        '''
        btd = businesstimedelta.Rules([workday, lunchbreak])
        return btd

    def date1_calc(self):
        btd = self.date_prepare()
        delta = None
        if self.service:
            delta = businesstimedelta.BusinessTimeDelta(btd, hours=self.service.time1)
        else:
            delta = businesstimedelta.BusinessTimeDelta(btd, hours=self.crew.incident_time_one)
        rez = self.date_in + delta
        return rez

    def date2_calc(self):
        btd = self.date_prepare()
        delta = None
        if self.service:
            delta = businesstimedelta.BusinessTimeDelta(btd, hours=self.service.time2)
        else:
            delta = businesstimedelta.BusinessTimeDelta(btd, hours=self.crew.incident_time_two)
        rez = self.date_in + delta
        return rez

    def date3_calc(self):
        btd = self.date_prepare()
        delta = None
        if self.service:
            delta = businesstimedelta.BusinessTimeDelta(btd, hours=self.service.time3)
        else:
            delta = businesstimedelta.BusinessTimeDelta(btd, hours=self.crew.incident_time_two)
        rez = self.date_in + delta
        return rez

    def fail_work(self):
        rez = False
        date_reaction = self.date1_calc()
        if self.date_work:
            if self.date_work > date_reaction:
                rez = True
            else:
                rez = False
        else:
            if timezone.now() > date_reaction:
                rez = True
            else:
                rez = False
        return rez

    def fail_finish(self):
        rez = False
        date_finish = self.date2_calc()
        if self.date_finish:
            if self.date_finish > date_finish:
                rez = True
            else:
                rez = False
        else:
            if timezone.now() > date_finish:
                rez = True
            else:
                rez = False
        return rez

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid1()
        super(CrewTask, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-date_in']
        verbose_name = u'Task'
        verbose_name_plural = u'Tasks'


class TaskUsers(models.Model):
    OBSERVER_TYPE = 0
    DISPATCHER_TYPE = 1
    OPERATOR_TYPE = 2
    RESPONSIBLE_TYPE = 3

    USER_TYPE_CHOICES = (
        (OBSERVER_TYPE, 'OBSERVER'),
        (DISPATCHER_TYPE, 'DISPATCHER'),
        (OPERATOR_TYPE, 'OPERATOR'),
        (RESPONSIBLE_TYPE, 'RESPONSIBLE')
    )

    task = models.ForeignKey(
        CrewTask,
        verbose_name=u'Task',
        on_delete=models.DO_NOTHING
    )
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        verbose_name=u'User',
        on_delete=models.SET_NULL
    )
    type = models.IntegerField(
        choices=USER_TYPE_CHOICES,
        default=OBSERVER_TYPE,
        verbose_name=u'User type'
    )

    class Meta:
        ordering = ['task', 'user', 'type']
        verbose_name = u'Task user'
        verbose_name_plural = u'Task users'


class TaskFiles(models.Model):
    def file_path(instance, filename):
        #ext = filename.split('.')[-1]
        #filename = '{}.{}'.format(str(uuid.uuid1()), ext)
        return os.path.join(os.path.join('task', str(instance.task.uuid)), filename)

    task = models.ForeignKey(
        CrewTask,
        verbose_name=u'Task',
        on_delete=models.DO_NOTHING
    )
    file = models.FileField(
        blank=True,
        null=True,
        upload_to=file_path,
        verbose_name=u'file'
    )

    class Meta:
        verbose_name = u'Attachment'
        verbose_name_plural = u'Attachments'

class TaskEvent(models.Model):
    task = models.ForeignKey(
        CrewTask,
        verbose_name=u'Task',
        on_delete=models.DO_NOTHING
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=u'Event time'
    )
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        verbose_name=u'User',
        on_delete=models.SET_NULL
    )
    ip = models.GenericIPAddressField(
        default='',
        max_length=60,
        verbose_name=u'User IP address'
    )
    user_agent = models.CharField(
        default='',
        max_length=200,
        verbose_name=u'User Agent'
    )
    message = models.TextField(
        default='',
        verbose_name=u'Event text'
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
                ip=getUserHostAddress(request),
                user_agent=request.META['HTTP_USER_AGENT'],
                message=message
            )
            event.save()

    class Meta:
        ordering = ['-date']
        verbose_name = u'Task event'
        verbose_name_plural = u'Task events'
