import uuid
from django import template

from ...helpdesk.utils import check_member_admin, check_member_dispatcher, check_member
from ...helpdesk.models import CrewTask
from ...settings import SITE_URL, UPLOAD_URL

register = template.Library()


@register.simple_tag()
def site_url():
    return SITE_URL


@register.simple_tag()
def upload_url():
    return UPLOAD_URL


@register.filter
def date_from_now(val):
    u = str(uuid.uuid4())
    return '<span id="date_%s" title="%s"><script>moment.locale(\'ru\');$("#date_%s").html(moment("%s").fromNow());\n</script></span>' % (u, val, u, val)


@register.filter
def substring(val, count):
    return val[0:count]


@register.filter
def task_status(val):
    if int(val) == CrewTask.TASK_STATUS_NEW:
        return 'Новая'
    elif int(val) == CrewTask.TASK_STATUS_WAITING:
        return 'В ожидании'
    elif int(val) == CrewTask.TASK_STATUS_IN_WORK:
        return 'В работе'
    elif int(val) == CrewTask.TASK_STATUS_CLOSED:
        return 'Закрыта'
    elif int(val) == CrewTask.TASK_STATUS_FINISHED:
        return 'Завершена'
    elif int(val) == CrewTask.TASK_STATUS_CANCELED:
        return 'Отменена'
    elif int(val) == CrewTask.TASK_STATUS_PAUSED:
        return 'Приостановлена'


@register.simple_tag(takes_context=True)
def chk_member_admin(context, crew):
    request = context['request']
    return check_member_admin(request.user, crew)


@register.simple_tag(takes_context=True)
def chk_member_dispatcher(context, crew):
    request = context['request']
    return check_member_dispatcher(request.user, crew)


@register.simple_tag(takes_context=True)
def chk_member(context, crew):
    request = context['request']
    return check_member(request.user, crew)


@register.filter
def escapebr(val=''):
    return str(val) \
        .replace('&', '&amp;') \
        .replace('\'', '&#39;') \
        .replace('"', ' &quot;') \
        .replace('<', '&lt;') \
        .replace('>', '&gt;') \
        .replace('\n', '<br>')


@register.filter
def jsmultiline(val=''):
    return str(val) \
        .replace('\r\n', '\\n\\')
