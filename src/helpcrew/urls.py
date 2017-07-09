from django.conf.urls import url, include
from django.contrib import admin

from .media.views import media
from .vews import index, test

urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^test/$', test, name='test'),
    url(r'^u/', include('helpcrew.userext.urls')),

    url(r'^media/(?P<path>.*)$', media),
    url(r'^admin/', admin.site.urls),
]
