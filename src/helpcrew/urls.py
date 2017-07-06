from django.conf.urls import url
from django.contrib import admin
from .media.views import media

urlpatterns = [

    url(r'^media/(?P<path>.*)$', media),
    url(r'^admin/', admin.site.urls),
]
