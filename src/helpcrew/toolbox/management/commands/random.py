from random import randint, choice
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker.factory import Factory

import urllib.request
import os
import uuid

from ....userext.models import User
from ....helpdesk.models import *

fake_ru = Factory.create('ru-RU')
fake_en = Factory.create('en-US')
fake = None


def clean():
    CrewUsers.objects.all().delete()
    Crew.objects.all().delete()
    User.objects.all().delete()


def users():
    user = User.objects.create_user('slagovskiy@gmail.com', '1212qwqw')
    user.firstname = 'Sergey'
    user.lastname = 'Lagovskiy'
    user.is_checked = True
    user.is_superuser = True
    user.save()
    print('added user ' + user.email)

    user = User.objects.create_user('user1@helpcrew.ru', '1212qwqw')
    user.firstname = 'User'
    user.lastname = 'One'
    user.is_checked = True
    user.is_superuser = True
    user.save()
    print('added user ' + user.email)

    user = User.objects.create_user('user2@helpcrew.ru', '1212qwqw')
    user.firstname = 'User'
    user.lastname = 'Two'
    user.is_checked = True
    user.is_superuser = True
    user.save()
    print('added user ' + user.email)

    user = User.objects.create_user('user3@helpcrew.ru', '1212qwqw')
    user.firstname = 'User'
    user.lastname = 'Three'
    user.is_checked = True
    user.is_superuser = True
    user.save()
    print('added user ' + user.email)

    user = User.objects.create_user('user4@helpcrew.ru', '1212qwqw')
    user.firstname = 'User'
    user.lastname = 'Four'
    user.is_checked = True
    user.is_superuser = True
    user.save()
    print('added user ' + user.email)

    user = User.objects.create_user('user5@helpcrew.ru', '1212qwqw')
    user.firstname = 'User'
    user.lastname = 'Five'
    user.is_checked = True
    user.is_superuser = True
    user.save()
    print('added user ' + user.email)

    user = User.objects.create_user('user6@helpcrew.ru', '1212qwqw')
    user.firstname = 'User'
    user.lastname = 'Six'
    user.is_checked = True
    user.is_superuser = True
    user.save()
    print('added user ' + user.email)

    user = User.objects.create_user('user7@helpcrew.ru', '1212qwqw')
    user.firstname = 'User'
    user.lastname = 'Seven'
    user.is_checked = True
    user.is_superuser = True
    user.save()
    print('added user ' + user.email)

    user = User.objects.create_user('user8@helpcrew.ru', '1212qwqw')
    user.firstname = 'User'
    user.lastname = 'Eight'
    user.is_checked = True
    user.is_superuser = True
    user.save()
    print('added user ' + user.email)

    user = User.objects.create_user('user9@helpcrew.ru', '1212qwqw')
    user.firstname = 'User'
    user.lastname = 'Nine'
    user.is_checked = True
    user.is_superuser = True
    user.save()
    print('added user ' + user.email)


def crews(count):
    userlist = User.objects.all()
    for _ in range(0, count):
        name = ' '.join(fake_ru.words(randint(1, 3)))
        url = fake_en.slug()
        user = choice(userlist)
        if not Crew.exist_url(url):
            c = Crew.objects.create(
                name=name,
                url=url,
                user=user
            )
            c.save()
            cu = CrewUsers.objects.create(
                crew=c,
                user=user,
                type=CrewUsers.ADMINISTRATOR_TYPE
            )
            cu.save()
            print('Added crew ' + c.name + ' admin is ' + c.user.email)
            for _ in range(1, 5):
                user = choice(userlist)
                if not user.id in CrewUsers.objects.filter(crew=c).values_list('user', flat=True):
                    cu = CrewUsers.objects.create(
                        crew=c,
                        user=user,
                        type=CrewUsers.OPERATOR_TYPE
                    )
                    cu.save()
                    print('Added operator ' + c.user.email + ' in crew ' + c.name)
            for _ in range(1, 3):
                user = choice(userlist)
                if not user.id in CrewUsers.objects.filter(crew=c).values_list('user', flat=True):
                    cu = CrewUsers.objects.create(
                        crew=c,
                        user=user,
                        type=CrewUsers.DISPATCHER_TYPE
                    )
                    cu.save()
                    print('Added operator ' + c.user.email + ' in crew ' + c.name)


def roga():
    user = User.objects.filter(email='slagovskiy@gmail.com').first()
    c = Crew.objects.create(
        name=u'Рога и Копыта inc',
        url='roga',
        user=user
    )
    c.save()
    print('Created crew ' + c.name)
    cu = CrewUsers.objects.create(
        crew=c,
        user=user,
        type=CrewUsers.ADMINISTRATOR_TYPE
    )
    cu.save()
    print('Added user ' + cu.user.email + ' in crew ' + c.name)
    for _ in range(1, 5):
        user = choice(User.objects.all())
        if not user.id in CrewUsers.objects.filter(crew=c).values_list('user', flat=True):
            cu = CrewUsers.objects.create(
                crew=c,
                user=user,
                type=randint(0, 3)
            )
            cu.save()
            print('Added user ' + cu.user.email + ' in crew ' + c.name)
    for _ in range(1, 30):
        name = ' '.join(fake_ru.words(randint(2, 5)))
        time = randint(10, 20)
        cs = CrewService.objects.create(
            crew=c,
            name=name,
            time1=time,
            time2=time*2,
            time3=time*3,
            unit=u'шт',
            template=' '.join(fake_ru.words(randint(3, 15)))
        )
        cs.save()
        print('Added service ' + cs.name)
        for _ in range(1, randint(3, 10)):
            p = ServicePrice.objects.create(
                service=cs,
                start_date=timezone.now()-datetime.timedelta(randint(5, 600)),
                cost=randint(500, 1000)/randint(1, 4),
                prepay=randint(100, 500)/randint(1, 4),
                fine1=0.15,
                fine2=0.25
            )
            p.save()
            print('Added price to ' + cs.name)
    sp = TaskPriority.objects.create(
        crew=c,
        name='Очень низкий',
        time_factor=2,
        cost_factor=1,
        default=False
    )
    sp.save()
    sp = TaskPriority.objects.create(
        crew=c,
        name='Низкий',
        time_factor=1.5,
        cost_factor=1,
        default=False
    )
    sp.save()
    sp = TaskPriority.objects.create(
        crew=c,
        name='Нормальный',
        time_factor=1,
        cost_factor=1,
        default=True
    )
    sp.save()
    sp = TaskPriority.objects.create(
        crew=c,
        name='Высокий',
        time_factor=0.75,
        cost_factor=1.25,
        default=False
    )
    sp.save()
    sp = TaskPriority.objects.create(
        crew=c,
        name='Очень высокий',
        time_factor=0.5,
        cost_factor=1.5,
        default=False
    )
    sp.save()



class Command(BaseCommand):
    help = 'generate random data'

    def handle(self, **options):
        clean()
        users()
        crews(20)
        roga()
