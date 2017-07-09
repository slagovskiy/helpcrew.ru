from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
import logging

#from .toolbox.captcha import captcha_code, captcha_image
from .settings import EMAIL_SUBJECT_PREFIX, DEFAULT_FROM_EMAIL


log = logging.getLogger(__name__)


def index(request):
    content = {}
    return render(request, 'index.html', content)


def test(request):
    try:
        subject = u'Test тест'
        from_email = EMAIL_SUBJECT_PREFIX + ' <' + DEFAULT_FROM_EMAIL + '>'
        to = 'slagovskiy@gmail.com'
        text_content = u'test test тест тест'
        html_content = u'<div>test test</div>\n<div>тест тест</div>'
        msg = EmailMultiAlternatives()
        msg.subject = subject
        msg.body = text_content
        msg.from_email = from_email
        msg.to = [to]
        msg.bcc = [from_email]
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except:
        log.exception('test error')
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
