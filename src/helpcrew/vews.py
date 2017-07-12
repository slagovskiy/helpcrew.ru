from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import logging

#from .toolbox.captcha import captcha_code, captcha_image
from .settings import EMAIL_SUBJECT_PREFIX, DEFAULT_FROM_EMAIL, EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER


log = logging.getLogger(__name__)


def index(request):
    content = {}
    return render(request, 'index.html', content)


def test(request):
    '''
    msg = EmailMultiAlternatives(
        EMAIL_SUBJECT_PREFIX + u' Код подтверждения регистрации',
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


    from email.mime.multipart import MIMEMultipart

message = MIMEMultipart('alternative')
message['From'] = 'Sender Name <sender@server>'
message['To'] = 'Receiver Name <receiver@server>'
message['Cc'] = 'Receiver2 Name <receiver2@server>'
message['Subject'] = 'Any subject'

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
message.attach(part1)
message.attach(part2)
    '''
    import smtplib
    from email.mime.text import MIMEText

    title = 'My title'
    msg_content = '<h2>{title} > <font color="green">OK</font></h2>\n'.format(title=title)
    message = MIMEText(msg_content, 'html')

    message['From'] = 'Sender Name <noreply@helpcrew.ru>'
    message['To'] = 'odyssey.2033@gmail.com'
    message['Subject'] = 'Any subject'

    msg_full = message.as_string()

    server = smtplib.SMTP_SSL(EMAIL_HOST + ':' + str(EMAIL_PORT))
    server.starttls()
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    server.sendmail(message['From'],
                    [message['To']],
                    msg_full)
    server.quit()
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
