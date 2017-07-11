from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import logging

#from .toolbox.captcha import captcha_code, captcha_image
from .settings import EMAIL_SUBJECT_PREFIX, DEFAULT_FROM_EMAIL


log = logging.getLogger(__name__)


def index(request):
    content = {}
    return render(request, 'index.html', content)


def test(request):
    try:
        '''
        msg = EmailMultiAlternatives(
            '[' + EMAIL_SUBJECT_PREFIX + u'] Код подтверждения регистрации',
            render_to_string('user/email_register_text.html', {'user': request.user}),
            EMAIL_SUBJECT_PREFIX + ' <' + DEFAULT_FROM_EMAIL + '>',
            ['slagovskiy@gmail.com']
        )
        msg.bcc = [DEFAULT_FROM_EMAIL]
        msg.attach_alternative(
            render_to_string('user/email_register.html', {'user': request.user})
            , 'text/html'
        )
        msg.content_subtype = 'text/html'
        msg.send()
        '''
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
