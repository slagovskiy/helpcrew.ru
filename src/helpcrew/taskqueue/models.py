from django.db import models


class Email(models.Model):
    msg_from = models.CharField(
        max_length=255,
        default=''
    )
    msg_to = models.CharField(
        max_length=255,
        default=''
    )
    msg_bcc = models.CharField(
        max_length=255,
        default=''
    )
    subject = models.CharField(
        max_length=255,
        default=''
    )
    body = models.TextField(
        default=''
    )
    subject = models.CharField(
        max_length=255,
        default=''
    )
    added = models.DateTimeField(
        auto_now_add=True
    )
    finished = models.DateTimeField(
        null=True,
        blank=True
    )
    is_finished = models.BooleanField(
        default=False
    )
    info = models.CharField(
        max_length=255,
        default=''
    )

    def __str__(self):
        return '<Email task %s>' % self.added

    class Meta:
        ordering = ['is_finished', 'added']
        verbose_name = 'Email task'
        verbose_name_plural = 'Email tasks'
