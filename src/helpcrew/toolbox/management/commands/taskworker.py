import os
import time
import sys
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.core.management.base import BaseCommand

from helpcrew.taskqueue.models import Email
from helpcrew.settings import WORKER_PID


class Command(BaseCommand):
    help = 'sending ping to search server'

    def handle(self, **options):
        is_running = False
        try:
            print('[' + str(datetime.now()) + '] starting...')
            if os.path.exists(WORKER_PID):
                pid = open(WORKER_PID)
                s = pid.readline()
                if len(s) > 0:
                    t = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
                    d = (datetime.now() - t).seconds
                    print('[' + str(datetime.now()) + '] last worker activity ' + str(d) + 'seconds ago')
                    if d < 60:
                        is_running = True
                pid.close()
            if is_running:
                print('[' + str(datetime.now()) + '] second instance stoped')
                return
            print('[' + str(datetime.now()) + '] open pid file')
            pid = open(WORKER_PID, 'w')
            while(True):
                pid.seek(0)
                pid.truncate()
                pid.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                pid.flush()
                print('[' + str(datetime.now()) + '] get new tasks')
                msgs = Email.objects.filter(is_finished=False)
                for msg in msgs:
                    #try:
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
                        msg.info = 'ok'
                    #except:
                    #    msg.info = sys.exc_info()[0]
                    #finally:
                    #    msg.finished = timezone.now()
                    #    msg.is_finished = True
                        msg.save()
                print('[' + str(datetime.now()) + '] waiting...')
                time.sleep(10)
        except:
            print('[' + str(datetime.now()) + '] ' + sys.exc_info()[0])
