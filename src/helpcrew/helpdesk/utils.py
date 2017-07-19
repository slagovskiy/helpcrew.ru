from .models import Crew, CrewUsers


def get_crews_list(user, flat=False):
    content = {}
    if flat:
        crews = Crew.objects.filter(
            id__in=CrewUsers.objects.filter(user=user).values_list('crew', flat=True)
        )
        content = crews
    else:
        crews_a = Crew.objects.filter(
            id__in=CrewUsers.objects.filter(user=user, type=CrewUsers.ADMINISTRATOR_TYPE).values_list('crew', flat=True)
        )
        crews_d = Crew.objects.filter(
            id__in=CrewUsers.objects.filter(user=user, type=CrewUsers.DISPATCHER_TYPE).values_list('crew', flat=True)
        )
        crews_o = Crew.objects.filter(
            id__in=CrewUsers.objects.filter(user=user, type=CrewUsers.OPERATOR_TYPE).values_list('crew', flat=True)
        )
        content = {
                'crews_a': crews_a,
                'crews_d': crews_d,
                'crews_o': crews_o
        }
    return content
