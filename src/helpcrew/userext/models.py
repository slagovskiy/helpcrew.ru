from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db import models
import uuid
import os

from ..settings import SERVER


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Not a valid email address!')

        user = self.model(
            email=UserManager.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    def avatar_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(str(uuid.uuid1()), ext)
        return os.path.join(os.path.join('avatar', instance.email), filename)

    uuid = models.CharField(
        'UUID',
        max_length=255,
        default=''
    )
    email = models.EmailField(
        'Email',
        max_length=255,
        unique=True,
        db_index=True
    )
    avatar = models.ImageField(
        'Avatar',
        blank=True,
        null=True,
        upload_to=avatar_path
    )
    firstname = models.CharField(
        'First name',
        default='',
        max_length=40,
        null=True,
        blank=True
    )
    lastname = models.CharField(
        'Last name',
        default='',
        max_length=40,
        null=True,
        blank=True
    )
    register_date = models.DateField(
        'Register',
        auto_now_add=True,
    )
    is_active = models.BooleanField(
        'is active',
        default=True
    )
    is_admin = models.BooleanField(
        'is admin',
        default=False
    )
    is_checked = models.BooleanField(
        'is checked',
        default=False
    )

    interface_wide_screen = models.BooleanField(
        'wide screen support',
        default=False
    )

    def avatar_preview(self):
        if self.avatar:
            return '<img src="%s?h=100" border="0"/>' % self.avatar.url
        else:
            return ''

    avatar_preview.short_description = 'Avatar preview'
    avatar_preview.allow_tags = True

    def url(self):
        return SERVER + self.avatar.url

    def get_full_name(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid1()
        super(User, self).save(*args, **kwargs)

    @property
    def is_staff(self):
        return self.is_admin

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def name(self):
        if self.firstname or self.lastname:
            return '%s %s' % (self.firstname, self.lastname)
        else:
            return self.email

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
