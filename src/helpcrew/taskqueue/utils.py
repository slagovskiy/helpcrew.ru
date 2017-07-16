from .models import Email
from ..settings import DEFAULT_FROM_EMAIL, EMAIL_SUBJECT_PREFIX


def add_email(msg_to='', msg_from=DEFAULT_FROM_EMAIL, subject='', body='', body_alternative=''):
    msg = Email.objects.create(
        msg_to=msg_to,
        msg_from=msg_from,
        msg_bcc=DEFAULT_FROM_EMAIL,
        subject='[' + EMAIL_SUBJECT_PREFIX + u'] ' + subject,
        body=body,
        body_alternative=body_alternative
    )
    msg.save()
