from django.http import HttpResponse
from django.shortcuts import render, redirect
import logging

from django.urls import reverse

log = logging.getLogger(__name__)


def index(request):
    content = {}
    return render(request, 'index.html', content)


def go_crew(request, url=None):
    return redirect(reverse('crew_view', kwargs={'url': url}))


def test(request):

    return HttpResponse('test!')

#def captcha(request):
#    request.session['CAPTCHA_CODE'] = captcha_code(4)
#    return captcha_image(request.session['CAPTCHA_CODE'], 1)


#def captcha_check(request, code):
#    data = '0'
#    if request.session['CAPTCHA_CODE'] == str(code).upper():
#        return HttpResponse('1', content_type="application/javascript")
#    else:
#        return HttpResponse('0', content_type="application/javascript")
