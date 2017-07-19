from django import template
from ...helpdesk.utils import get_crews_list

register = template.Library()


@register.inclusion_tag('widgets/crew_list.html', takes_context=True)
def widget_crew_list(context):
    request = context['request']
    content = {
        'crews' : get_crews_list(request.user)
    }
    return content
