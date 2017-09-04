import json
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Table
from ..helpdesk.utils import check_member, check_member_admin
from ..helpdesk.models import Crew, CrewEvent


@csrf_exempt
def api_table_list(request, crew=None):
    crew = Crew.objects.filter(slug=crew).first()
    if crew:
        if not check_member(request.user, crew):
            return JsonResponse({
                'message': u'access denied!',
                'data': ''
            })
        data = serializers.serialize('json', crew.table_set.all().order_by('deleted', 'name'))
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
def api_table_edit(request, table=None):
    if request.method == 'GET':
        table = Table.objects.filter(id=table).first()
        if not check_member_admin(request.user, table.crew):
            return JsonResponse({
                'message': u'access denied!',
                'data': ''
            })
        if table:
            data = serializers.serialize('json', [table,])
            return JsonResponse({
                'message': '',
                'data': json.loads(data)
            })
        else:
            return JsonResponse({
                'message': u'Справочник не найден',
                'data': ''
            })
    if request.method == 'POST':
        if table == '0':
            crew = Crew.objects.filter(id=request.POST.get('crew', '0')).first()
            if crew:
                if check_member_admin(request.user, crew):
                    table = Table.objects.create(
                        crew=crew,
                        name=request.POST.get('name', '_'),
                    )
                    table.save()
                    CrewEvent.addEvent(request, table.crew, u'Добавлен новый справочник ' + table.name)
                    return HttpResponse('ok')
                else:
                    return HttpResponse('access denied!')
            else:
                return HttpResponse('crew not found!')
        table = Table.objects.filter(id=table).first()
        if check_member_admin(request.user, table.crew):
            if table:
                table.name = request.POST.get('name', '_')
                table.save()
                CrewEvent.addEvent(request, table.crew, u'Изменен приоритет ' + table.name)
                return HttpResponse('ok')
            else:
                return HttpResponse('service not found!')
        else:
            return HttpResponse('access denied!')


@csrf_exempt
def api_table_delete(request, table=None):
    table = Table.objects.filter(id=table).first()
    if check_member_admin(request.user, table.crew):
        if table:
            table.deleted = not table.deleted
            table.save()
            if table.deleted:
                CrewEvent.addEvent(request, table.crew, u'Справочник ' + table.name + ' помечен удаленным')
            else:
                CrewEvent.addEvent(request, table.crew, u'Справочник ' + table.name + ' восстановлен')
            return HttpResponse('ok')
        else:
            return HttpResponse('service not found!')
    else:
        return HttpResponse('access denied!')
