import re
import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.core import serializers

from .models import Crew, CrewUsers, CrewService, ServicePrice
from ..userext.models import User
from .utils import get_crews_list, check_member, check_member_admin
from ..userext.decoretors import authenticate_check


def crew_edit(request, url=None):
    if not request.user.is_authenticated:
        return redirect(reverse('user_login'))
    if request.method=='GET':
        if url==None:
            content = {}
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
                c = Crew.objects.create(
                    name=name,
                    url=url,
                    user=request.user
                )
                c.save()
                if c.url=='':
                    c.url = c.slug
                    c.save()
                cu = CrewUsers.objects.create(
                    crew=c,
                    user=request.user,
                    type=CrewUsers.ADMINISTRATOR_TYPE
                )
                cu.save()
                return redirect(reverse('crew_view_redirect', kwargs={'url': c.url}))
            else:
                messages.error(request, u'Ошибка сохранения')
                content = {
                    'form': {
                        'name': name,
                        'url': url
                    }
                }
                return render(request, 'helpdesk/crew_edit.html', content)
        else:
            return redirect(reverse('crew_edit'))
    else:
        return render(request, 'helpdesk/crew_edit.html', {})


def crew_edit_user_edit(request, url=None, email=None, type=None):
    if not type:
        return redirect(reverse('crew_edit', url))
    crew = Crew.objects.filter(url=url)
    user = User.objects.filter(email=email)
    if crew and user:
        crew = crew[0]
        user = user[0]
        if not check_member_admin(request.user, crew):
            messages.error(request, u'Доступ запрещен')
        else:
            cu = CrewUsers.objects.filter(crew=crew, user=user)
            if cu:
                cu = cu[0]
                if cu.type == CrewUsers.ADMINISTRATOR_TYPE:
                    _cu = CrewUsers.objects.filter(crew=crew, type=CrewUsers.ADMINISTRATOR_TYPE)
                    if len(_cu) < 2 and str(type).lower() != 'a':
                        messages.error(request, u'Нельзя убрать последнего администратора')
                        return redirect(reverse('crew_edit', kwargs={'url': url}))
                if str(type).lower() == 'a':
                    cu.type = CrewUsers.ADMINISTRATOR_TYPE
                    cu.save()
                elif str(type).lower() == 'd':
                    cu.type = CrewUsers.DISPATCHER_TYPE
                    cu.save()
                elif str(type).lower() == 'o':
                    cu.type = CrewUsers.OPERATOR_TYPE
                    cu.save()
    return redirect(reverse('crew_edit', kwargs={'url': url}))


@authenticate_check
def crew_view(request, url=None):
    crew = Crew.objects.filter(url=url)
    if crew:
        crew = crew[0]
        if request.user.id in CrewUsers.objects.filter(crew=crew).values_list('user', flat=True):
            request.session['crew'] = crew.url
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
                        unit=request.POST.get('unit', '_')
                    )
                    serv.save()
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
                serv.save()
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
            elif str(type).lower() == 'd':
                user.type = CrewUsers.DISPATCHER_TYPE
                user.save()
            elif str(type).lower() == 'o':
                user.type = CrewUsers.OPERATOR_TYPE
                user.save()
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
            user.deleted = not user.deleted
            user.save()
            return HttpResponse('ok')
        else:
            return HttpResponse('access denied!')
    else:
        return HttpResponse('member not found')


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
