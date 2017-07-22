import re
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import Crew, CrewUsers
from ..userext.models import User
from .utils import get_crews_list
from .decorators import crew_member_check
from ..userext.decoretors import authenticate_check


def crew_edit(request, url=None):
    if not request.user.is_authenticated:
        return redirect(reverse('user_login'))
    if request.method=='GET':
        if url==None:
            content = {}
            return render(request, 'helpdesk/crew_edit.html', content)
        else:
            crew = Crew.objects.get(url=url)
            if crew:
                content = {'crew': crew}
                return render(request, 'helpdesk/crew_edit.html', content)
            else:
                content = {'error': u'Команда не найдена'}
                return render(request, 'helpdesk/crew_edit.html', content)
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
                content = {
                    'error': u'Ошибка сохранения',
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
    crew = Crew.objects.get(url=url)
    user = User.objects.get(email=email)
    if crew and user:
        cu = CrewUsers.objects.filter(crew=crew, user=user)
        if cu:
            cu = cu[0]
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
        if request.user.id in CrewUsers.objects.filter(crew=crew).values_list('user', flat=True):
            content = {
                'crew': crew[0],
                'crews': get_crews_list(request.user, flat=True)
            }
            return render(request, 'helpdesk/crew_view.html', content)
        else:
            return redirect(reverse('user_profile'))
    else:
        return redirect(reverse('user_profile'))


@csrf_exempt
def crew_check_url(request):
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
