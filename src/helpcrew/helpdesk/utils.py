from .models import Crew, CrewUsers, CrewTask


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


def statusLikeText(status):
    str = ''
    if status == CrewTask.TASK_STATUS_PAUSED:
        str = 'Приостановлена'
    elif status == CrewTask.TASK_STATUS_CANCELED:
        str = 'Отменена'
    elif status == CrewTask.TASK_STATUS_FINISHED:
        str = 'Завершена'
    elif status == CrewTask.TASK_STATUS_CLOSED:
        str = 'Закрыта'
    elif status == CrewTask.TASK_STATUS_IN_WORK:
        str = 'В работе'
    elif status == CrewTask.TASK_STATUS_WAITING:
        str = 'Ожидает'
    elif status == CrewTask.TASK_STATUS_NEW:
        str = 'Новая'
    return str


def __first_check(user=None):
    if user.is_anonymous:
        return False
    elif not user.is_checked:
        return False
    else:
        return True


def check_member(user=None, crew=None):
    if not __first_check(user):
        return False
    cu = CrewUsers.objects.filter(crew=crew, user=user)
    if cu:
        return True
    else:
        return False


def check_member_admin(user=None, crew=None):
    if not __first_check(user):
        return False
    cu = CrewUsers.objects.filter(crew=crew, user=user)
    if cu:
        cu = cu[0]
        if cu.type == CrewUsers.ADMINISTRATOR_TYPE:
            return True
        else:
            return False
    else:
        return False


def check_member_dispatcher(user=None, crew=None):
    if not __first_check(user):
        return False
    cu = CrewUsers.objects.filter(crew=crew, user=user)
    if cu:
        cu = cu[0]
        if cu.type == CrewUsers.DISPATCHER_TYPE or cu.type == CrewUsers.ADMINISTRATOR_TYPE:
            return True
        else:
            return False
    else:
        return False
