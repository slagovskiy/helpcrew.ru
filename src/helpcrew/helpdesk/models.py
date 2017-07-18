import uuid
from django.db import models

from ..toolbox.models import Global
from ..userext.models import User


class Crew(models.Model):
    slug = models.SlugField(
        unique=True
    )
    name = models.CharField(
        default='',
        max_length=255
    )
    url = models.CharField(
        default='',
        max_length=255
    )
    user = models.ForeignKey(User)
    added = models.DateTimeField(
        auto_now_add=True
    )
    deleted = models.BooleanField(
        default=False
    )
    crew_user_limit = models.IntegerField(default=0)
    start_task = models.IntegerField(default=0)
    incident_time_one = models.IntegerField(default=0)
    incident_time_two = models.IntegerField(default=0)
    request_time_one = models.IntegerField(default=0)
    request_time_two = models.IntegerField(default=0)

    def __str__(self):
        return '<Crew %s>' % self.name

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
        verbose_name = 'Crew'
        verbose_name_plural = 'Crews'


class CrewUsers(models.Model):
    ADMINISTRATOR_TYPE = 0
    DISPATCHER_TYPE = 1
    OPERATOR_TYPE = 2

    USER_TYPE_CHOICES = (
        (ADMINISTRATOR_TYPE, 'Administrator'),
        (DISPATCHER_TYPE, 'Dispatcher'),
        (OPERATOR_TYPE, 'Operator'),
    )

    crew = models.ForeignKey(Crew)
    user = models.ForeignKey(User)
    type = models.IntegerField(choices=USER_TYPE_CHOICES, default=OPERATOR_TYPE)

    class Meta:
        ordering = ['crew', 'user']
        verbose_name = 'Crew user'
        verbose_name_plural = 'Crew users'
