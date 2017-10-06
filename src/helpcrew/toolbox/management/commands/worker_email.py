import os
import time
import sys
import logging
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.core.management.base import BaseCommand
from html2text import html2text

from ....taskqueue.models import Email
from ....settings import WORKER_PID


class Command(BaseCommand):
    help = 'sending ping to search server'

    def handle(self, **options):
        logger = logging.getLogger('helpcrew.worker_email')
        is_running = False
        logger.info('\n[' + str(datetime.now()) + '] starting...')
        print('[' + str(datetime.now()) + '] starting...')
        if os.path.exists(WORKER_PID):
            pid = open(WORKER_PID)
            s = pid.readline()
            if len(s) > 0:
                t = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
                d = (datetime.now() - t).seconds
                logger.info('[' + str(datetime.now()) + '] last worker activity ' + str(d) + 'seconds ago')
                print('[' + str(datetime.now()) + '] last worker activity ' + str(d) + 'seconds ago')
                if d < 60:
                    is_running = True
            pid.close()
        if is_running:
            logger.info('[' + str(datetime.now()) + '] second instance stoped')
            print('[' + str(datetime.now()) + '] second instance stoped')
            return
        logger.info('[' + str(datetime.now()) + '] open pid file')
        print('[' + str(datetime.now()) + '] open pid file')
        pid = open(WORKER_PID, 'w')
        while(True):
            pid.seek(0)
            pid.truncate()
            pid.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            pid.flush()
            logger.info('[' + str(datetime.now()) + '] get new tasks')
            print('[' + str(datetime.now()) + '] get new tasks')
            msgs = Email.objects.filter(is_finished=False)
            for msg in msgs:
                try:
                    _msg = EmailMultiAlternatives()
                    _msg.subject = msg.subject
                    _msg.from_email = msg.msg_from
                    _msg.to = [msg.msg_to]
                    _msg.bcc = [msg.msg_bcc]
                    _msg.body = html2text(msg.body)
                    _msg.attach_alternative(msg.body, 'text/html')
                    _msg.content_subtype = 'text/html'
                    _msg.send()
                    logger.info('[' + str(datetime.now()) + '] email to ' + msg.msg_to + ' - ok')
                    print('[' + str(datetime.now()) + '] email to ' + msg.msg_to + ' - ok')
                    msg.info = 'ok'
                except:
                    msg.info = sys.exc_info()[0]
                finally:
                    msg.finished = timezone.now()
                    msg.is_finished = True
                    msg.save()
            logger.info('[' + str(datetime.now()) + '] waiting...')
            print('[' + str(datetime.now()) + '] waiting...')
            time.sleep(10)
