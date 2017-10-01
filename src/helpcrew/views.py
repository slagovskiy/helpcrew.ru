from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import logging

from django.urls import reverse
from .helpdesk.models import Crew, CrewTask
from .helpdesk.utils import check_member

log = logging.getLogger(__name__)


def index(request):
    content = {}
    return render(request, 'index.html', content)


def go_crew(request, url=None):
    if request.user.is_anonymous:
        return redirect(reverse('task_new', kwargs={'url': url}))
    else:
        crew = Crew.objects.filter(url=url).first()
        if crew:
            if check_member(request.user, crew):
                return redirect(reverse('crew_view', kwargs={'url': url}))
            else:
                return redirect(reverse('task_new', kwargs={'url': url}))
        else:
            messages.error(request, u'Команда не найдена')
            return redirect(reverse('home'))


def test(request):
    task = CrewTask.objects.filter(uuid='3d82581e-a602-11e7-8361-00158315a310').first()
    content = {
        'task': task,
        'title': u'Заявка отправлена в работу'
    }
    return render(request, 'helpdesk/email_task_info.html', content)

#def captcha(request):
#    request.session['CAPTCHA_CODE'] = captcha_code(4)
#    return captcha_image(request.session['CAPTCHA_CODE'], 1)


#def captcha_check(request, code):
#    data = '0'
#    if request.session['CAPTCHA_CODE'] == str(code).upper():
#        return HttpResponse('1', content_type="application/javascript")
#    else:
#        return HttpResponse('0', content_type="application/javascript")
