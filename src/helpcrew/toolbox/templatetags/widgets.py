from django import template
from ...helpdesk.models import Crew, CrewUsers

register = template.Library()


@register.inclusion_tag('widgets/crew_list.html', takes_context=True)
def widget_crew_list(context):
    request = context['request']
    crews_a = Crew.objects.filter(
        id__in=CrewUsers.objects.filter(user=request.user, type=CrewUsers.ADMINISTRATOR_TYPE).values_list('crew', flat=True)
        )
    crews_d = Crew.objects.filter(
        id__in=CrewUsers.objects.filter(user=request.user, type=CrewUsers.DISPATCHER_TYPE).values_list('crew', flat=True)
    )
    crews_o = Crew.objects.filter(
        id__in=CrewUsers.objects.filter(user=request.user, type=CrewUsers.OPERATOR_TYPE).values_list('crew', flat=True)
    )
    content = {
        'crews':
            {
                'crews_a': crews_a,
                'crews_d': crews_d,
                'crews_o': crews_o
            }
    }
    return content
