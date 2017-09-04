import re
import json
from django.utils import timezone
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.core import serializers

from .models import Crew, CrewUsers, CrewService, ServicePrice, TaskPriority, CrewEvent, CrewTask, TaskEvent, TaskFiles
from ..userext.models import User
from .utils import get_crews_list, check_member, check_member_admin
from ..userext.decoretors import authenticate_check


def crew_edit(request, url=None):
    if not request.user.is_authenticated:
        return redirect(reverse('user_login'))
    if request.method == 'GET':
        if url==None:
            content = {'action': request.GET.get('action', '')}
            return render(request, 'helpdesk/crew_edit.html', content)
        else:
            crew = Crew.objects.filter(url=url)
            if crew and check_member(request.user, crew[0]):
                content = {'crew': crew[0]}
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
        else:
            return render(request, 'helpdesk/crew_edit.html', {})


@authenticate_check
def crew_view(request, url=None):
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


def task_new(request, url=None):
    crew = Crew.objects.filter(url=url).first()
    if crew:
        content = {
            'crew': crew
        }
        if check_member(request.user, crew):
            pass
        else:
            return render(request, 'helpdesk/task_new.html', content)
    else:
        messages.error(request, u'Команда не найдена')
        return redirect(reverse('home'))


def task_save(request):
    crew = Crew.objects.filter(slug=request.POST.get('crew', '')).first()
    if crew:
        service = CrewService.objects.filter(id=int(request.POST.get('service', '-1'))).first()
        status = CrewTask.TASK_STATUS_NEW
        priority = TaskPriority.objects.filter(id=int(request.POST.get('priority', '-1'))).first()
        description = request.POST.get('description', '')
        task_type = CrewTask.TASK_TYPE_NORMAL
        contact_name = request.POST.get('name', '')
        contact_email = request.POST.get('email', '')
        if not service:
            task_type = CrewTask.TASK_TYPE_INCIDENT
        observer = None
        if not request.user.is_anonymous:
            observer = request.user

        task = CrewTask.objects.create(
            crew=crew,
            type=task_type,
            status=status,
            service=service,
            description=description,
            priority=priority,
            date_in=timezone.now(),
            contact_name=contact_name,
            contact_email=contact_email,
            observer=observer
        )
        task.save()

        messages.error(request, u'Заявка успешно сохранена')

        CrewEvent.addEvent(request, crew, u'Добавлена новая заявка ' + str(task.uuid))
        TaskEvent.addEvent(request, task, u'Добавлена новая заявка ' + str(task.uuid))

        if service and service.auto_wait_status:
            task.status = CrewTask.TASK_STATUS_WAITING
            task.save()
            TaskEvent.addEvent((request, task, u'Заявка автоматически переведена в статус "В ожидании"'))

        if service and task.type == CrewTask.TASK_TYPE_SUBSCRIBE:
            task.status = CrewTask.TASK_STATUS_IN_WORK
            task.save()
            TaskEvent.addEvent((request, task, u'Подписка автоматически переведена в статус "В работе"'))

        if observer and not check_member(request.user, crew):
            cu = CrewUsers.objects.create(
                crew=crew,
                user=observer,
                type=CrewUsers.OBSERVER_TYPE
            )
            cu.save()
            CrewEvent.addEvent(request, crew, u'В команду добавлен наблюдатель ' + observer.email)
            return redirect(reverse('crew_view', kwargs={'url': crew.url}))
        else:
            messages.error(request, u'Заявка успешно сохранена')
            return redirect(reverse('task_info', kwargs={'uuid': str(task.uuid)}))
    else:
        messages.error(request, u'Команда не найдена')
        return redirect(reverse('home'))


def task_info(request, uuid=None):
    task = CrewTask.objects.filter(uuid=uuid).first()
    if task:
        content = {
            'task': task
        }
        return render(request, 'helpdesk/task_info.html', content)
    else:
        messages.error(request, u'Заявка не найдена')
        return redirect(reverse('home'))


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
                crew.work_start_time = request.POST.get('work_start_time', '9')
                crew.work_stop_time = request.POST.get('work_stop_time', '18')
                crew.launch_start_time = request.POST.get('launch_start_time', '12')
                crew.launch_stop_time = request.POST.get('launch_stop_time', '13')
                crew.holidays = request.POST.get('holidays', '')
                crew.work_day_0 = request.POST.get('work_day_0', False)
                crew.work_day_1 = request.POST.get('work_day_1', False)
                crew.work_day_2 = request.POST.get('work_day_2', False)
                crew.work_day_3 = request.POST.get('work_day_3', False)
                crew.work_day_4 = request.POST.get('work_day_4', False)
                crew.work_day_5 = request.POST.get('work_day_5', False)
                crew.work_day_6 = request.POST.get('work_day_6', False)
                crew.save()
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
def api_user_invaite(request, email=None):
    return HttpResponse('ok')


@csrf_exempt
def api_user_add(request, email=None, type=None):
    return HttpResponse('ok')


@csrf_exempt
def api_priority_list(request, crew=None):
    crew = Crew.objects.filter(slug=crew).first()
    if crew:
        data = serializers.serialize('json', crew.taskpriority_set.all().order_by('deleted', 'name'))
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
    crew = Crew.objects.filter(slug=crew).first()
    if crew:
        if check_member_admin(request.user, crew):
            list = []
            for item in CrewEvent.objects.select_related('user', 'crew').filter(crew=crew).order_by('-date')[0:int(limit)]:
                list.append(
                    {
                        'id': item.id,
                        'crew_id': item.crew.id,
                        'date': item.date.strftime('%Y/%m/%d %H:%M:%S'),
                        'ip': item.ip,
                        'host': item.host,
                        'user_agent': item.user_agent,
                        'message': item.message,
                        'user_firstname': item.user.firstname,
                        'user_lastname': item.user.lastname,
                        'user_email': item.user.email,
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
