import os
import time
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from helpcrew.taskqueue.models import Email
from helpcrew.settings import WORKER_PID
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'sending ping to search server'

    def handle(self, **options):
        is_running = False
        try:
            if os.path.exists(WORKER_PID):
                pid = open(WORKER_PID)
                s = pid.readline()
                if len(s) > 0:
                    t = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
                    if (datetime.now() - t).seconds < 60:
                        is_running = True
                pid.close()
            if is_running:
                return
            pid = open(WORKER_PID, 'w')
            while(True):
                pid.seek(0)
                pid.truncate()
                pid.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                pid.flush()
                msgs = Email.objects.filter(is_finished=False)
                for msg in msgs:
                    try:
                        _msg = EmailMultiAlternatives()
                        _msg.subject = msg.subject
                        _msg.from_email = msg.msg_from
                        _msg.to = [msg.msg_to]
                        _msg.bcc = [msg.msg_bcc]
                        _msg.body = msg.body
                        _msg.attach_alternative(msg.body_alternative, 'text/html')
                        _msg.content_subtype = 'text/html'
                        _msg.send()
                        print('[' + str(datetime.now()) + '] email to ' + msg.msg_to + ' - ok')
                    except ValueError:
                        print(ValueError)
                print('[' + str(datetime.now()) + '] waiting...')
                time.sleep(10)
        except:
            pass
        finally:
            if not is_running:
                os.remove(WORKER_PID)
