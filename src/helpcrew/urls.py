from django.conf.urls import url
from django.contrib import admin

from .media.views import media
from .vews import index

urlpatterns = [
    url(r'^$', index, name='home'),

    url(r'^media/(?P<path>.*)$', media),
    url(r'^admin/', admin.site.urls),
]
