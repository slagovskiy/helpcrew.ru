import uuid
from django import template

from ...helpdesk.utils import check_member_admin, check_member_dispatcher, check_member

register = template.Library()


@register.filter
def date_from_now(val):
    u = str(uuid.uuid4())
    return '<span id="date_' + u + '"><script>moment.locale(\'ru\');$("#date_' + u + '").html(moment("%s").fromNow());\n</script></span>' % val


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
