from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import logging

from django.urls import reverse
from .helpdesk.models import Crew
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
    c = Crew.objects.filter(slug='82428b08-9609-11e7-92c2-00158315a310').first()
    content = {'crew': c}
    return render(request, 'helpdesk/email_invite.html', content)

#def captcha(request):
#    request.session['CAPTCHA_CODE'] = captcha_code(4)
#    return captcha_image(request.session['CAPTCHA_CODE'], 1)


#def captcha_check(request, code):
#    data = '0'
#    if request.session['CAPTCHA_CODE'] == str(code).upper():
#        return HttpResponse('1', content_type="application/javascript")
#    else:
#        return HttpResponse('0', content_type="application/javascript")
