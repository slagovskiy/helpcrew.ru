from datetime import datetime
import re
import json

import os
from django.utils.timezone import get_current_timezone
from django.template.loader import render_to_string
from django.utils import timezone
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.core import serializers

from ..settings import UPLOAD_DIR
from ..taskqueue.utils import add_email
from .models import Crew, CrewUsers, CrewService, ServicePrice, TaskPriority, CrewEvent, CrewTask, TaskEvent, TaskFiles, TaskUsers
from ..userext.models import User
from .utils import get_crews_list, check_member, check_member_admin, check_member_dispatcher, statusLikeText, \
    check_member_observer


def crew_edit(request, url=None):
    if request.user.is_anonymous:
        return redirect(reverse('user_login'))
    if not request.user.is_checked:
        return redirect(reverse('user_profile'))
    if request.method == 'GET':
        if url==None:
            content = {'action': request.GET.get('action', '')}
            return render(request, 'helpdesk/crew_edit.html', content)
        else:
            crew = Crew.objects.filter(url=url).first()
            if crew and check_member(request.user, crew):
                content = {'crew': crew}
                return render(request, 'helpdesk/crew_edit.html', content)
            else:
                messages.error(request, u'Команда не найдена')
                return redirect(reverse('user_profile'))
    elif request.method=='POST':
        if 'name' in request.POST:
            name = request.POST['name']
            url = request.POST.get('url', '')
            if not Crew.exist_url(url):
                crew = Crew.objects.create(
                    name=name,
                    url=url,
                    user=request.user
                )
                crew.save()
                CrewEvent.addEvent(request, crew, u'Создана новая команда')
                if crew.url=='':
                    crew.url = crew.slug
                    crew.save()
                cu = CrewUsers.objects.create(
                    crew=crew,
                    user=request.user,
                    type=CrewUsers.ADMINISTRATOR_TYPE
                )
                cu.save()
                CrewEvent.addEvent(request, crew, u'В команду добавлен администратор ' + request.user.email)
                return redirect(reverse('crew_view_redirect', kwargs={'url': crew.url}))
            else:
                messages.error(request, u'Ошибка сохранения')
                content = {
                    'form': {
                        'name': name,
                        'url': url
                    }
                }
                return render(request, 'helpdesk/crew_edit.html', content)
        elif 'uuid' in request.POST:
            crew = Crew.objects.filter(slug=request.POST.get('uuid', '')).first()
            if crew:
                if not CrewUsers.objects.filter(user=request.user, crew=crew):
                    cu = CrewUsers.objects.create(
                        crew=crew,
                        user=request.user,
                        type=CrewUsers.OPERATOR_TYPE
                    )
                    cu.save()
                    CrewEvent.addEvent(request, crew, u'В команду добавлен оператор ' + request.user.email)
                return redirect(reverse('crew_view_redirect', kwargs={'url': crew.url}))
            return render(request, 'helpdesk/crew_edit.html', {})
        else:
            return render(request, 'helpdesk/crew_edit.html', {})


def crew_view(request, url=None):
    if request.user.is_anonymous:
        return redirect(reverse('user_login'))
    if not request.user.is_checked:
        return redirect(reverse('user_profile'))
    crew = Crew.objects.filter(url=url)
    if crew:
        crew = crew[0]
        if check_member(request.user, crew):
            content = {
                'crew': crew,
                'crews': get_crews_list(request.user, flat=True)
            }
            return render(request, 'helpdesk/crew_view.html', content)
        else:
            messages.error(request, u'Вы не участник этой команды')
            return redirect(reverse('user_profile'))
    else:
        messages.error(request, u'Команда не найдена')
        return redirect(reverse('user_profile'))


def crew_list_public(request):
    crews = Crew.objects.filter(deleted=False, is_public=True)
    content = {
        'crews': crews
    }
    return render(request, 'helpdesk/crew_list_public.html', content)


def task_new(request, url=None):
    crew = Crew.objects.filter(url=url).first()
    if request.method == 'GET':
        if crew:
            if crew.password == request.session.get(crew.slug, ''):
                content = {
                    'crew': crew,
                    'password': 'ok'
                }
            else:
                content = {
                    'crew': crew,
                    'password': 'no'
                }
            return render(request, 'helpdesk/task_new.html', content)
        else:
            messages.error(request, u'Команда не найдена')
            return redirect(reverse('home'))
    elif request.method == 'POST':
        if 'password' in request.POST:
            if crew.password == request.POST.get('password', ''):
                request.session[crew.slug] = crew.password
            else:
                request.session[crew.slug] = ''
        return redirect(reverse('crew_view_redirect', kwargs={'url': crew.url}))


@csrf_exempt
def api_crew_edit(request, crew=None):
    if request.method == 'GET':
        crew = Crew.objects.filter(slug=crew).first()
        if not check_member_admin(request.user, crew):
            return JsonResponse({
                'message': u'access denied!',
                'data': ''
            })
        if crew:
            data = serializers.serialize('json', [crew,])
            return JsonResponse({
                'message': '',
                'data': json.loads(data)
            })
        else:
            return JsonResponse({
                'message': u'Команда не найдена',
                'data': ''
            })
    if request.method == 'POST':
        crew = Crew.objects.filter(slug=request.POST.get('slug', '')).first()
        if check_member_admin(request.user, crew):
            if crew:
                crew.name = request.POST.get('name', '_')
                crew.url = request.POST.get('url', crew.slug)
                crew.description = request.POST.get('description', '')
                crew.user_page = request.POST.get('user_page', '')
                crew.password = request.POST.get('password', '')
                crew.work_start_time = request.POST.get('work_start_time', '9:00')
                crew.work_end_time = request.POST.get('work_end_time', '18:00')
                crew.lunch_start_time = request.POST.get('lunch_start_time', '12:00')
                crew.lunch_end_time = request.POST.get('lunch_end_time', '13:00')
                crew.holidays = request.POST.get('holidays', '')
                crew.is_public = request.POST.get('is_public', False)
                crew.work_day_0 = request.POST.get('work_day_0', False)
                crew.work_day_1 = request.POST.get('work_day_1', False)
                crew.work_day_2 = request.POST.get('work_day_2', False)
                crew.work_day_3 = request.POST.get('work_day_3', False)
                crew.work_day_4 = request.POST.get('work_day_4', False)
                crew.work_day_5 = request.POST.get('work_day_5', False)
                crew.work_day_6 = request.POST.get('work_day_6', False)
                crew.save()
                if 'logo' in request.FILES:
                    up_file = request.FILES['logo']
                    file = os.path.join(UPLOAD_DIR, Crew.logo_path(crew, up_file.name))
                    filename = os.path.basename(file)
                    if not os.path.exists(os.path.dirname(file)):
                        os.makedirs(os.path.dirname(file))
                    destination = open(file, 'wb+')
                    for chunk in up_file.chunks():
                        destination.write(chunk)
                    crew.logo.save(filename, destination, save=False)
                    crew.save()
                    destination.close()
                    CrewEvent.addEvent(request, crew, u'Изменены параметры команды')
                return HttpResponse('ok')
            else:
                return HttpResponse('crew not found!')
        else:
            return HttpResponse('access denied!')


@csrf_exempt
def api_service_list(request, crew=None):
    crew = Crew.objects.filter(slug=crew).first()
    if crew:
        data = serializers.serialize('json', crew.crewservice_set.all().order_by('deleted', 'name'))
        return JsonResponse({
            'message': '',
            'data': json.loads(data)
        })
    else:
        return JsonResponse({
            'message': u'Команда не найдена',
            'model': ''
        })


@csrf_exempt
def api_service_template(request, service=None):
    s = CrewService.objects.filter(id=service).first()
    if s:
        data = s.template
        return HttpResponse(data)
    else:
        return HttpResponse('')


@csrf_exempt
def api_service_edit(request, service=None):
    if request.method == 'GET':
        serv = CrewService.objects.filter(id=service).first()
        if not check_member_admin(request.user, serv.crew):
            return JsonResponse({
                'message': u'access denied!',
                'data': ''
            })
        if serv:
            data = serializers.serialize('json', [serv,])
            return JsonResponse({
                'message': '',
                'data': json.loads(data)
            })
        else:
            return JsonResponse({
                'message': u'Услуга не найдена',
                'data': ''
            })
    if request.method == 'POST':
        if service == '0':
            crew = Crew.objects.filter(id=request.POST.get('crew', '0')).first()
            if crew:
                if check_member_admin(request.user, crew):
                    serv = CrewService.objects.create(
                        crew=crew,
                        name=request.POST.get('name', '_'),
                        time1=request.POST.get('time1', '0'),
                        time2=request.POST.get('time2', '0'),
                        unit=request.POST.get('unit', '_'),
                        template=request.POST.get('template', ''),
                        auto_wait_status=request.POST.get('auto_wait_status', 'False')
                    )
                    serv.save()
                    CrewEvent.addEvent(request, crew, u'Добавлена услуга ' + serv.name)
                    return HttpResponse('ok')
                else:
                    return HttpResponse('access denied!')
            else:
                return HttpResponse('crew not found!')
        serv = CrewService.objects.filter(id=service).first()
        if check_member_admin(request.user, serv.crew):
            if serv:
                serv.name = request.POST.get('name', '_')
                serv.time1 = request.POST.get('time1', '0')
                serv.time2 = request.POST.get('time2', '0')
                serv.unit = request.POST.get('unit', '_')
                serv.template = request.POST.get('template', '')
                serv.auto_wait_status = request.POST.get('auto_wait_status', 'False')
                serv.save()
                CrewEvent.addEvent(request, serv.crew, u'Изменена услуга ' + serv.name)
                return HttpResponse('ok')
            else:
                return HttpResponse('service not found!')
        else:
            return HttpResponse('access denied!')


@csrf_exempt
def api_service_delete(request, service=None):
    serv = CrewService.objects.filter(id=service).first()
    if check_member_admin(request.user, serv.crew):
        if serv:
            serv.deleted = not serv.deleted
            serv.save()
            if serv.deleted:
                CrewEvent.addEvent(request, serv.crew, u'Услуга ' + serv.name + ' помечена удаленной')
            else:
                CrewEvent.addEvent(request, serv.crew, u'Услуга ' + serv.name + ' восстановлена')
            return HttpResponse('ok')
        else:
            return HttpResponse('service not found!')
    else:
        return HttpResponse('access denied!')


@csrf_exempt
def api_service_price_list(request, service=None):
    serv = CrewService.objects.filter(id=service).first()
    if serv:
        if check_member_admin(request.user, serv.crew):
            data = serializers.serialize('json', serv.serviceprice_set.all())
            return JsonResponse({
                'message': '',
                'service': serv.id,
                'data': json.loads(data)
            })
        else:
            return JsonResponse({
                'message': u'access denied!',
                'data': ''
            })

    else:
        return JsonResponse({
            'message': u'Услуга не найдена',
            'data': ''
        })


@csrf_exempt
def api_service_price_edit(request, price=None):
    if request.method == 'GET':
        price = ServicePrice.objects.filter(id=price).first()
        if not check_member_admin(request.user, price.service.crew):
            return JsonResponse({
                'message': u'access denied!',
                'data': ''
            })
        if price:
            data = serializers.serialize('json', [price,])
            return JsonResponse({
                'message': '',
                'data': json.loads(data)
            })
        else:
            return JsonResponse({
                'message': u'Прайс не найдена',
                'data': ''
            })
    if request.method == 'POST':
        if price == '0':
            service = CrewService.objects.filter(id=request.POST.get('service', '0')).first()
            if service:
                if check_member_admin(request.user, service.crew):
                    price = ServicePrice.objects.create(
                        service=service,
                        start_date=request.POST.get('start_date', '_'),
                        cost=float(request.POST.get('cost', '0')),
                        prepay=float(request.POST.get('prepay', '0')),
                        fine1=float(request.POST.get('fine1', '0')),
                        fine2=float(request.POST.get('fine2', '0'))
                    )
                    price.save()
                    CrewEvent.addEvent(request, price.service.crew, u'Услуге ' + price.service.name + ' добавлен прайс')
                    return HttpResponse('ok')
                else:
                    return HttpResponse('access denied!')
            else:
                return HttpResponse('service not found!')
        price = ServicePrice.objects.filter(id=price).first()
        if check_member_admin(request.user, price.service.crew):
            if price:
                price.start_date = request.POST.get('start_date', '_')
                price.cost = float(request.POST.get('cost', '0'))
                price.prepay = float(request.POST.get('prepay', '0'))
                price.fine1 = float(request.POST.get('fine1', '_'))
                price.fine2 = float(request.POST.get('fine2', '_'))
                price.save()
                CrewEvent.addEvent(request, price.service.crew, u'Услуге ' + price.service.name + ' изменен прайс')
                return HttpResponse('ok')
            else:
                return HttpResponse('price not found!')
        else:
            return HttpResponse('access denied!')


@csrf_exempt
def api_user_list(request, crew=None):
    crew = Crew.objects.filter(slug=crew).first()
    if crew:
        if check_member(request.user, crew):
            list = []
            for item in CrewUsers.objects.select_related('user', 'crew').filter(crew=crew).order_by('type'):
                list.append(
                    {
                        'crew_id': item.crew.id,
                        'crew_url': item.crew.url,
                        'member_type': item.type,
                        'member_id': item.id,
                        'member_deleted': item.deleted,
                        'user_id': item.user.id,
                        'user_email': item.user.email,
                        'user_firstname': item.user.firstname,
                        'user_lastname': item.user.lastname
                    }
                )
            data = json.dumps(list)
            return JsonResponse({
                'message': '',
                'data': json.loads(data)
            })
        else:
            return JsonResponse({
                'message': u'Доступ запрещен',
                'model': ''
            })
    else:
        return JsonResponse({
            'message': u'Команда не найдена',
            'model': ''
        })


@csrf_exempt
def api_user_edit(request, member=None, type=None):
    if not type:
        return HttpResponse('type not found')
    user = CrewUsers.objects.filter(id=member).first()
    if user:
        if check_member_admin(request.user, user.crew):
            if user.type == CrewUsers.ADMINISTRATOR_TYPE:
                _cu = CrewUsers.objects.filter(crew=user.crew, type=CrewUsers.ADMINISTRATOR_TYPE)
                if len(_cu) < 2 and str(type).lower() != 'a':
                    return HttpResponse(u'Нельзя убрать последнего администратора')
            if str(type).lower() == 'a':
                user.type = CrewUsers.ADMINISTRATOR_TYPE
                user.save()
                CrewEvent.addEvent(request, user.crew, u'Пользователь ' + user.user.email + ' назначен администратором')
            elif str(type).lower() == 'd':
                user.type = CrewUsers.DISPATCHER_TYPE
                user.save()
                CrewEvent.addEvent(request, user.crew, u'Пользователь ' + user.user.email + ' назначен диспетчером')
            elif str(type).lower() == 'o':
                user.type = CrewUsers.OPERATOR_TYPE
                user.save()
                CrewEvent.addEvent(request, user.crew, u'Пользователь ' + user.user.email + ' назначен оператором')
            return HttpResponse('ok')
        else:
            return HttpResponse('access denied!')
    else:
        return HttpResponse('member not found')


@csrf_exempt
def api_user_delete(request, member=None):
    user = CrewUsers.objects.filter(id=member).first()
    if user:
        if check_member_admin(request.user, user.crew):
            _cu = CrewUsers.objects.filter(crew=user.crew, type=CrewUsers.ADMINISTRATOR_TYPE)
            if len(_cu) < 2 and user.type == CrewUsers.ADMINISTRATOR_TYPE:
                return HttpResponse(u'Нельзя убрать последнего администратора')
            user.deleted = not user.deleted
            user.save()
            if user.deleted:
                CrewEvent.addEvent(request, user.crew, u'Пользователь ' + user.name + ' помечен удаленным')
            else:
                CrewEvent.addEvent(request, user.crew, u'Пользователь ' + user.name + ' восстановлен')
            return HttpResponse('ok')
        else:
            return HttpResponse('access denied!')
    else:
        return HttpResponse('member not found')


@csrf_exempt
def api_user_invite(request, email=None):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        crew = Crew.objects.filter(slug=request.POST.get('crew', '')).first()
        if crew and email:
            add_email(
                msg_to=email,
                subject=u'Приглашение к работе в команде',
                body=render_to_string('helpdesk/email_invite.html', {'crew': crew})
            )
            CrewEvent.addEvent(request, crew, u'Отправлено приглашение на адрес ' + email)
            return HttpResponse('ok')
        else:
            return HttpResponse('Команда не найдена')
    else:
        return HttpResponse('ok')


@csrf_exempt
def api_user_add(request, email=None, type=None):
    return HttpResponse('ok')


@csrf_exempt
def api_priority_list(request, crew=None):
    crew = Crew.objects.filter(slug=crew).first()
    if crew:
        data = serializers.serialize('json', crew.taskpriority_set.all().order_by('time_factor', 'name'))
        return JsonResponse({
            'message': '',
            'data': json.loads(data)
        })
    else:
        return JsonResponse({
            'message': u'Команда не найдена',
            'model': ''
        })


@csrf_exempt
def api_priority_edit(request, priority=None):
    if request.method == 'GET':
        priority = TaskPriority.objects.filter(id=priority).first()
        if not check_member_admin(request.user, priority.crew):
            return JsonResponse({
                'message': u'access denied!',
                'data': ''
            })
        if priority:
            data = serializers.serialize('json', [priority,])
            return JsonResponse({
                'message': '',
                'data': json.loads(data)
            })
        else:
            return JsonResponse({
                'message': u'Приоритет не найден',
                'data': ''
            })
    if request.method == 'POST':
        if priority == '0':
            crew = Crew.objects.filter(id=request.POST.get('crew', '0')).first()
            if crew:
                if check_member_admin(request.user, crew):
                    priority = TaskPriority.objects.create(
                        crew=crew,
                        name=request.POST.get('name', '_'),
                        time_factor=request.POST.get('time_factor', '0'),
                        cost_factor=request.POST.get('cost_factor', '0'),
                        default=request.POST.get('default', 'False')
                    )
                    priority.save()
                    CrewEvent.addEvent(request, priority.crew, u'Добавлен новый приоритет ' + priority.name)
                    return HttpResponse('ok')
                else:
                    return HttpResponse('access denied!')
            else:
                return HttpResponse('crew not found!')
        priority = TaskPriority.objects.filter(id=priority).first()
        if check_member_admin(request.user, priority.crew):
            if priority:
                priority.name = request.POST.get('name', '_')
                priority.time_factor = request.POST.get('time_factor', '0')
                priority.cost_factor = request.POST.get('cost_factor', '0')
                priority.default = request.POST.get('default', 'False')
                priority.save()
                CrewEvent.addEvent(request, priority.crew, u'Изменен приоритет ' + priority.name)
                return HttpResponse('ok')
            else:
                return HttpResponse('service not found!')
        else:
            return HttpResponse('access denied!')


@csrf_exempt
def api_priority_delete(request, priority=None):
    priority = TaskPriority.objects.filter(id=priority).first()
    if check_member_admin(request.user, priority.crew):
        if priority:
            priority.deleted = not priority.deleted
            priority.save()
            if priority.deleted:
                CrewEvent.addEvent(request, priority.crew, u'Приоритет ' + priority.name + ' помечен удаленным')
            else:
                CrewEvent.addEvent(request, priority.crew, u'Приоритет ' + priority.name + ' восстановлен')
            return HttpResponse('ok')
        else:
            return HttpResponse('service not found!')
    else:
        return HttpResponse('access denied!')


@csrf_exempt
def api_event_list(request, crew=None, limit=100):
    import pytz
    crew = Crew.objects.filter(slug=crew).first()
    if crew:
        if check_member_admin(request.user, crew):
            list = []
            for item in CrewEvent.objects.select_related('user', 'crew').filter(crew=crew).order_by('-date')[0:int(limit)]:
                list.append(
                    {
                        'id': item.id,
                        'crew_id': item.crew.id,
                        'date': timezone.localtime(item.date, timezone.get_current_timezone()).strftime('%Y/%m/%d %H:%M:%S'),
                        'ip': item.ip,
                        'user_agent': item.user_agent,
                        'message': item.message,
                        'user_firstname': item.user.firstname if item.user else u'Гость',
                        'user_lastname': item.user.lastname if item.user else '',
                        'user_email': item.user.email if item.user else '',
                    }
                )
            data = json.dumps(list)
            return JsonResponse({
                'message': '',
                'data': json.loads(data)
            })
        else:
            return JsonResponse({
                'message': u'Доступ запрещен',
                'model': ''
            })
    else:
        return JsonResponse({
            'message': u'Команда не найдена',
            'model': ''
        })


@csrf_exempt
def api_task_list(request, crew=None):
    crew = Crew.objects.filter(slug=crew).first()
    if crew:
        if check_member(request.user, crew):
            list = []
            for item in CrewTask.objects.filter(crew=crew).order_by('status', '-date_in'): #select_related('user', 'crew')
                list.append(
                    {
                        'uuid': item.uuid,
                        'type': item.type,
                        'status': statusLikeText(item.status),
                        'status_code': item.status,
                        'description': item.description[0:150],
                        'priority': item.priority.name,
                        'date_in': timezone.localtime(item.date_in, timezone.get_current_timezone()).strftime('%Y/%m/%d %H:%M:%S'),
                        'service': item.service.name if item.service else u'Проблема',
                        'crew_id': item.crew.id,
                        'crew_uuid': item.crew.slug
                    }
                )
            data = json.dumps(list)
            return JsonResponse({
                'message': '',
                'data': json.loads(data)
            })
        else:
            return JsonResponse({
                'message': u'Доступ запрещен',
                'model': ''
            })
    else:
        return JsonResponse({
            'message': u'Команда не найдена',
            'model': ''
        })

@csrf_exempt
def api_task_new(request, crew=None):
    crew = Crew.objects.filter(slug=crew).first()
    if crew:
        service = serializers.serialize('json', CrewService.objects.filter(crew=crew, deleted=False))
        priority = serializers.serialize('json', TaskPriority.objects.filter(crew=crew, deleted=False))
        return JsonResponse({
            'message': u'',
            'service': json.loads(service),
            'priority': json.loads(priority),
            'task': True if request.GET.get('type', '0') == '0' else False,
            'subscribe': True if request.GET.get('type', '0') == '2' else False,
            'type': request.GET.get('type', '0'),
            'model': ''
        })
    else:
        return JsonResponse({
            'message': u'Команда не найдена',
            'model': ''
        })


def api_task_view(request, uuid=None):
    task = CrewTask.objects.select_related('crew', 'service', 'priority').filter(uuid=uuid).first()
    if task:
        list = []
        events = []
        for event in task.taskevent_set.select_related('user'):
            events.append({
                'date': timezone.localtime(event.date, timezone.get_current_timezone()).strftime('%Y/%m/%d %H:%M:%S') if event.date else '',
                'user': event.user.name() if event.user else u'Гость',
                'ip': event.ip,
                'user_agent': event.user_agent,
                'message': event.message
            })

        user_observer = []
        _user = task.user_observer()
        if _user:
            user_observer.append({
                'name': _user.name(),
                'first_name': _user.firstname,
                'last_name': _user.lastname,
                'email': _user.email
            })

        user_dispatcher = []
        _user = task.user_dispatcher()
        if _user:
            user_dispatcher.append({
                'name': _user.name(),
                'first_name': _user.firstname,
                'last_name': _user.lastname,
                'email': _user.email
            })

        user_close = []
        _user = task.user_close()
        if _user:
            user_close.append({
                'name': _user.name(),
                'first_name': _user.firstname,
                'last_name': _user.lastname,
                'email': _user.email
            })

        user_operator = []
        _user = task.user_operator()
        for __user in _user:
            user_operator.append({
                'name': __user.name(),
                'first_name': __user.firstname,
                'last_name': __user.lastname,
                'email': __user.email
            })

        date_reaction = task.date1_calc()
        date_finish = task.date2_calc()
        date_fail = task.date3_calc()
        fail_work = task.fail_work()
        fail_finish = task.fail_finish()

        list.append({
            'id': task.id,
            'uuid': task.uuid,
            'crew_id': task.crew.id,
            'type': task.type,
            'status': statusLikeText(task.status),
            'status_code': task.status,
            'priority': task.priority.name,
            'priority_code': task.priority.id,
            'service': task.service.name if task.service else u'Проблема',
            'service_code': task.service.id if task.service else '',
            'description': task.description,
            'date_in': timezone.localtime(task.date_in, timezone.get_current_timezone()).strftime('%Y/%m/%d %H:%M:%S') if task.date_in else '',
            'date_work': timezone.localtime(task.date_work, timezone.get_current_timezone()).strftime('%Y/%m/%d %H:%M:%S') if task.date_work else '',
            'date_end': timezone.localtime(task.date_end, timezone.get_current_timezone()).strftime('%Y/%m/%d %H:%M:%S') if task.date_end else '',
            'date_finish': timezone.localtime(task.date_finish, timezone.get_current_timezone()).strftime('%Y/%m/%d %H:%M:%S') if task.date_finish else '',
            'date_close': timezone.localtime(task.date_close, timezone.get_current_timezone()).strftime('%Y/%m/%d %H:%M:%S') if task.date_close else '',
            'date__reaction': timezone.localtime(date_reaction, timezone.get_current_timezone()).strftime('%Y/%m/%d %H:%M:%S') if task.date_in else '',
            'date__finish': timezone.localtime(date_finish, timezone.get_current_timezone()).strftime('%Y/%m/%d %H:%M:%S') if task.date_in else '',
            'date__fail': timezone.localtime(date_fail, timezone.get_current_timezone()).strftime('%Y/%m/%d %H:%M:%S') if task.date_in else '',
            'fail_work': fail_work,
            'fail_finish': fail_finish,
            'user_observer': user_observer,
            'user_dispatcher': user_dispatcher,
            'user_operator': user_operator,
            'user_close': user_close,
            'contact_name': task.contact_name,
            'contact_email': task.contact_email,
            'qty': str(task.qty),
            'fine': str(task.fine),
            'events': events
        })
        return JsonResponse({
            'message': u'',
            'task': json.loads(json.dumps(list)),
            'model': ''
        })
    else:
        messages.error(request, u'Заявка не найдена')
        return redirect(reverse('home'))


def api_task_save(request):
    crew = Crew.objects.filter(slug=request.POST.get('crew', '')).first()
    type = int(request.POST.get('type', 0))
    if crew:
        service = None
        if type != CrewTask.TASK_TYPE_INCIDENT:
            service = CrewService.objects.filter(id=int(request.POST.get('service', '-1'))).first()
        status = CrewTask.TASK_STATUS_NEW
        priority = None
        if type == CrewTask.TASK_TYPE_NORMAL:
            priority = TaskPriority.objects.filter(id=int(request.POST.get('priority', '-1'))).first()
        else:
            priority = TaskPriority.objects.filter(default=True).first()
        description = request.POST.get('description', '')
        task_type = type
        contact_name = request.POST.get('name', '')
        contact_email = request.POST.get('email', '')
        date_in = None
        date_end = None
        if type == CrewTask.TASK_TYPE_SUBSCRIBE:
            date_in = request.POST.get('start_date', timezone.now())
            date_end = request.POST.get('end_date', timezone.now())
        else:
            date_in = timezone.now()

        task = CrewTask.objects.create(
            crew=crew,
            type=task_type,
            status=status,
            service=service,
            description=description,
            priority=priority,
            date_in=date_in,
            date_end=date_end,
            contact_name=contact_name,
            contact_email=contact_email
        )
        task.save()
        CrewEvent.addEvent(request, crew, u'Добавлена новая заявка ' + str(task.uuid))
        TaskEvent.addEvent(request, task, u'Добавлена новая заявка ' + str(task.uuid))

        for file in request.FILES.getlist('files'):
            up_file = file
            tfile = TaskFiles.objects.create(
                task=task
            )
            tfile.save()
            file = os.path.join(UPLOAD_DIR, TaskFiles.file_path(tfile, up_file.name))
            filename = os.path.basename(file)
            if not os.path.exists(os.path.dirname(file)):
                os.makedirs(os.path.dirname(file))
            destination = open(file, 'wb+')
            for chunk in up_file.chunks():
                destination.write(chunk)
            tfile.file.save(filename, destination, save=False)
            tfile.save()
            destination.close()
            TaskEvent.addEvent(request, task, u'К заявке добавлено вложение ' + up_file.name)

        if service and service.auto_wait_status:
            task.status = CrewTask.TASK_STATUS_WAITING
            task.save()
            TaskEvent.addEvent(request, task, u'Заявка автоматически переведена в статус "В ожидании"')

        if service and task.type == CrewTask.TASK_TYPE_SUBSCRIBE:
            task.status = CrewTask.TASK_STATUS_IN_WORK
            task.save()
            TaskEvent.addEvent(request, task, u'Подписка автоматически переведена в статус "В работе"')

        if not request.user.is_anonymous:
            u = TaskUsers.objects.create(
                task=task,
                user=request.user,
                type=TaskUsers.OBSERVER_TYPE
            )
            u.save()
            TaskEvent.addEvent(request, task, u'Подписке назначен наблюдатель ' + request.user.name())

            if not CrewUsers.objects.filter(user=request.user).first():
                cu = CrewUsers.objects.create(
                    crew=crew,
                    user=request.user,
                    type=CrewUsers.OBSERVER_TYPE
                )
                cu.save()
                CrewEvent.addEvent(request, crew, u'В команду добавлен наблюдатель ' + request.user.name())

        return HttpResponse('ok')
    else:
        return HttpResponse(u'Команда не найдена')


@csrf_exempt
def api_task_description(request, uuid=None):
    task = CrewTask.objects.filter(uuid=uuid).first()
    if task:
        return HttpResponse(task.description)
    else:
        return HttpResponse(u'Задача не найдена')


def task_status_changing(request, task, status):
    if status == 1:
        u = TaskUsers.objects.filter(task=task, type=TaskUsers.DISPATCHER_TYPE).first()
        if u:
            u.user = request.user
            u.save()
            TaskEvent.addEvent(request, task, u'Изменен диспетчер на ' + request.user.name())
        else:
            TaskUsers.objects.create(
                task=task,
                user=request.user,
                type=TaskUsers.DISPATCHER_TYPE
            )
            TaskEvent.addEvent(request, task, u'Назначен диспетчер ' + request.user.name())

    if status == 2:
        u = TaskUsers.objects.filter(task=task, type=TaskUsers.DISPATCHER_TYPE).first()
        if u:
            u.user = request.user
            u.save()
            TaskEvent.addEvent(request, task, u'Изменен диспетчер на ' + request.user.name())
        else:
            TaskUsers.objects.create(
                task=task,
                user=request.user,
                type=TaskUsers.DISPATCHER_TYPE
            )
            TaskEvent.addEvent(request, task, u'Назначен диспетчер ' + request.user.name())

    if status == 3:
        TaskUsers.objects.create(
            task=task,
            user=request.user,
            type=TaskUsers.OPERATOR_TYPE
        )
        TaskEvent.addEvent(request, task, u'Назначен оператор ' + request.user.name())

    if status == 4:
        u = TaskUsers.objects.filter(task=task, type=TaskUsers.CLOSE_TYPE).first()
        if u:
            u.user = request.user
            u.save()
            TaskEvent.addEvent(request, task, u'Изменен ответственный на ' + request.user.name())
        else:
            TaskUsers.objects.create(
                task=task,
                user=request.user,
                type=TaskUsers.CLOSE_TYPE
            )
            TaskEvent.addEvent(request, task, u'Назначен ответственный ' + request.user.name())

    if status == 6:
        u = TaskUsers.objects.filter(task=task, type=TaskUsers.CLOSE_TYPE).first()
        if u:
            u.user = request.user
            u.save()
            TaskEvent.addEvent(request, task, u'Изменен ответственный на ' + request.user.name())
        else:
            TaskUsers.objects.create(
                task=task,
                user=request.user,
                type=TaskUsers.CLOSE_TYPE
            )
            TaskEvent.addEvent(request, task, u'Назначен ответственный ' + request.user.name())


@csrf_exempt
def api_task_status_save(request):
    task = CrewTask.objects.filter(uuid=request.POST.get('task', '-1')).first()
    status = int(request.POST.get('status', '-1'))
    if task:
        if task.status == 0 and status in [1, 2, 4] and check_member_dispatcher(request.user, task.crew):
            task.status = status
        elif task.status == 1 and status in [2, 3, 4] and check_member_dispatcher(request.user, task.crew):
            task.status = status
        elif task.status == 1 and status == 3 and check_member(request.user, task.crew) and not check_member_observer(request.user, task.crew):
            task.status = status
        elif task.status == 2 and status in [1, 4] and check_member_dispatcher(request.user, task.crew):
            task.status = status
        elif task.status == 3 and status == 5 and not check_member_observer(request.user, task.crew):
            task.status = status
        elif task.status == 4 and status in [1, 2] and check_member_admin(request.user, task.crew):
            task.status = status
        elif task.status == 5 and status in [1, 6] and check_member_dispatcher(request.user, task.crew):
            task.status = status
        elif task.status == 6 and status in [1, 2, 4] and check_member_admin(request.user, task.crew):
            task.status = status
        else:
            return HttpResponse(u'Отказано в доступе')

        TaskEvent.addEvent(request, task, u'Заявка переведена в статус ' + statusLikeText(status))
        task_status_changing(request, task, status)
        task.save()
        return HttpResponse('ok')
    else:
        return HttpResponse(u'Задача не найдена')


@csrf_exempt
def api_task_priority_save(request):
    task = CrewTask.objects.filter(uuid=request.POST.get('task', '-1')).first()
    if task:
        if check_member_dispatcher(request.user, task.crew):
            priority = TaskPriority.objects.filter(id=int(request.POST.get('priority', '-1'))).first()
            if priority:
                task.priority = priority
                task.save()
                TaskEvent.addEvent(request, task, u'Заявке назначен новый статус ' + priority.name)
                return HttpResponse('ok')
            else:
                return HttpResponse(u'Приоритет не найден')
        else:
            return HttpResponse(u'Доступ запрещен')
    else:
        return HttpResponse(u'Задача не найдена')


@csrf_exempt
def api_task_datein_save(request):
    task = CrewTask.objects.filter(uuid=request.POST.get('task', '-1')).first()
    if task:
        if check_member_dispatcher(request.user, task.crew):
            tz = get_current_timezone()
            dt = tz.localize(datetime.strptime(request.POST.get('date_in', ''), '%Y/%m/%d %H:%M:%S'))
            task.date_in = dt
            task.save()
            TaskEvent.addEvent(request, task, u'Изменена дата подачи заявки ' + request.POST.get('date_in', ''))
            return HttpResponse('ok')
        else:
            return HttpResponse(u'Доступ запрещен')
    else:
        return HttpResponse(u'Задача не найдена')


@csrf_exempt
def api_task_service_save(request):
    task = CrewTask.objects.filter(uuid=request.POST.get('task', '-1')).first()
    if task:
        if check_member_dispatcher(request.user, task.crew):
            service = CrewService.objects.filter(id=int(request.POST.get('service', '-1'))).first()
            if service:
                task.service = service
                task.description = request.POST.get('description', '')
                task.save()
                TaskEvent.addEvent(request, task, u'В заявке изменена услуга ' + service.name)
                return HttpResponse('ok')
            else:
                return HttpResponse(u'Услуга не найден')
        else:
            return HttpResponse(u'Доступ запрещен')
    else:
        return HttpResponse(u'Задача не найдена')


@csrf_exempt
def api_crew_check_url(request):
    message = ''
    r = True
    if 'url' in request.POST:
        url = request.POST['url']
        pattern = re.compile('^([a-z_0-9]+)$')
        if not pattern.match(url):
            message = u'Адрес команды должен состоять только из латинских символов и цифр'
            r = False
        if Crew.objects.filter(url=url):
            message = u'Комманда с таким адресом уже существует'
            r = False
    else:
        r = False
    return JsonResponse({'valid': r, 'message': message})
