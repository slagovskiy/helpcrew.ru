import json
from django.db import transaction
from django.db.models import Max
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Table, Field, Index, Record
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
        if table:
            if check_member_admin(request.user, table.crew):
                table.name = request.POST.get('name', '_')
                table.save()
                CrewEvent.addEvent(request, table.crew, u'Изменен справочник ' + table.name)
                return HttpResponse('ok')
            else:
                return HttpResponse('access denied!')
        else:
            return HttpResponse('table not found!')


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
            return HttpResponse('table not found!')
    else:
        return HttpResponse('access denied!')


@csrf_exempt
def api_field_list(request, table=None):
    table = Table.objects.filter(id=table).first()
    if table:
        if not check_member(request.user, table.crew):
            return JsonResponse({
                'message': u'access denied!',
                'data': ''
            })
        data = serializers.serialize('json', table.field_set.all().order_by('order'))
        return JsonResponse({
            'message': '',
            'table': table.id,
            'data': json.loads(data)
        })
    else:
        return JsonResponse({
            'message': u'Справочник не найден',
            'model': ''
        })


@csrf_exempt
def api_field_edit(request, field=None):
    if request.method == 'GET':
        field = Field.objects.filter(id=field).first()
        if field:
            if not check_member_admin(request.user, field.table.crew):
                return JsonResponse({
                    'message': u'access denied!',
                    'data': ''
                })
            else:
                data = serializers.serialize('json', [field,])
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
        if field == '0':
            table = Table.objects.filter(id=request.POST.get('table', '0')).first()
            if table:
                if check_member_admin(request.user, table.crew):
                    field = Field.objects.create(
                        table=table,
                        name=request.POST.get('name', '_'),
                        type=request.POST.get('type', Field.TYPE_STRING),
                        order=request.POST.get('order', 10),
                    )
                    field.save()
                    CrewEvent.addEvent(request, table.crew, u'Добавлено новое поле ' + field.name +
                                       ' в справочник ' + table.name)
                    return HttpResponse('ok')
                else:
                    return HttpResponse('access denied!')
            else:
                return HttpResponse('table not found!')
        field = Field.objects.filter(id=field).first()
        if field:
            if check_member_admin(request.user, field.table.crew):
                field.name = request.POST.get('name', '_')
                field.type = request.POST.get('type', Field.TYPE_STRING)
                field.order = request.POST.get('order', 10)
                field.save()
                CrewEvent.addEvent(request, field.table.crew, u'Изменено ' + field.name +
                                   ' в справочнике ' + field.table.name)
                return HttpResponse('ok')
            else:
                return HttpResponse('access denied!')
        else:
            return HttpResponse('field not found!')


@csrf_exempt
def api_field_delete(request, field=None):
    field = Field.objects.filter(id=field).first()
    if field:
        if check_member_admin(request.user, field.table.crew):
            field.deleted = not field.deleted
            field.save()
            if field.deleted:
                CrewEvent.addEvent(request, field.table.crew, u'Поле ' + field.name +
                                   ' в справочнике ' + field.table.name + ' помечено удаленным')
            else:
                CrewEvent.addEvent(request, field.table.crew, u'Поле ' + field.name +
                                   ' в справочнике ' + field.table.name + ' восстановлено')
            return HttpResponse('ok')
        else:
            return HttpResponse('access denied!')
    else:
        return HttpResponse('field not found!')


def api_record_list(request, table=None):
    table = Table.objects.filter(id=table).first()
    if table:
        if check_member(request.user, table.crew):
            flds = Field.objects.filter(table=table, deleted=False)
            indxs = Index.objects.filter(table=table, deleted=False)
            records = Record.objects.select_related('index', 'field').filter(index__table=table).order_by('index__num')
            data = [{
                'index_id': rec.index.id,
                'index_num': rec.index.num,
                'index_deleted': rec.index.deleted,
                'field_id': rec.field.id,
                'field_name': rec.field.name,
                'field_type': rec.field.type,
                'field_order': rec.field.order,
                'record_value': rec.value
            } for rec in records]
            found = False
            _data = []
            _header = []
            for field in flds:
                _header.append({
                    'field': field.id,
                    'value': field.name
                })
            for index in indxs:
                _records = []
                for field in flds:
                    val = ''
                    found = False
                    for row in data:
                        if row['index_id'] == index.id and row['field_id'] == field.id:
                            val = row['record_value']
                            found = True
                            break
                    _records.append({
                        'field': field.name,
                        'value': val
                    })
                _data.append({
                    'row': index.num,
                    'records': _records
                })
            return JsonResponse({
                'message': '',
                'table': table.id,
                'data': _data,
                'header': _header
            })
        else:
            return HttpResponse('access denied!')
    else:
        return HttpResponse('table not found!')


@csrf_exempt
@transaction.atomic
def api_record_save(request, table=None):
    table = Table.objects.filter(id=table).first()
    if table:
        if check_member(request.user, table.crew):
            index_num = Index.objects.filter(table=table).aggregate(Max('num'))
            if index_num['num__max']:
                index_num = index_num['num__max'] + 1
            else:
                index_num = 1
            index = Index.objects.create(
                table=table,
                num=index_num
            )
            index.save()
            for fld in request.POST:
                if fld[0:5] == 'field':
                    field = Field.objects.filter(id=int(fld[6:])).first()
                    if field:
                        record = Record.objects.create(
                            index=index,
                            field=field,
                            value=request.POST[fld]
                        )
                        record.save()
                    else:
                        raise NameError('Field not found')
            CrewEvent.addEvent(request, table.crew, 'Добавлена новая запись в справочник ' + table.name)
            return HttpResponse('ok')
        else:
            return HttpResponse('access denied!')
    else:
        return HttpResponse('table not found!')
