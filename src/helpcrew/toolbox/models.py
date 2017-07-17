from django.db import models


class Global(models.Model):
    slug = models.SlugField(
        unique=True
    )
    value = models.CharField(
        max_length=255,
        default=''
    )

    def __str__(self):
        return '<Global %s>' % self.slug

    @staticmethod
    def get(slug=None):
        if slug is None:
            return None
        else:
            g = Global.objects.filter(slug=slug).first()
            if g is None:
                return ''
            else:
                return g.value

    @staticmethod
    def set(slug=None, value=''):
        if slug is None:
            return False
        else:
            g = Global.objects.filter(slug=slug).first()
            if g is None:
                g = Global.objects.create(
                    slug=slug,
                    value=value
                )
                g.save()
                return True
            else:
                g.value = value
                g.save()
                return True

    @staticmethod
    def exist(slug=None):
        if slug is None:
            return False
        else:
            if Global.objects.filter(slug=slug).first() is None:
                return False
            else:
                return True

    @staticmethod
    def add_not_exist(slug=None, value=''):
        if not Global.exist(slug):
            Global.objects.create(
                slug=slug,
                value=value
            ).save()

    class Meta:
        ordering = ['slug']
        verbose_name = 'Global'
        verbose_name_plural = 'Globals'
