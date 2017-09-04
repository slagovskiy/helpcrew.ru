from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView

from .settings import DEBUG
from .media.views import media
from .views import index, test, go_crew


urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^test/$', test, name='test'),
    url(r'^u/', include('helpcrew.userext.urls')),
    url(r'^p/(?P<url>[-\w]+)/$', go_crew, name='crew_view_redirect'),
    url(r'^c/', include('helpcrew.helpdesk.urls')),
    url(r'^t/', include('helpcrew.dyntable.urls')),

    url(r'^media/(?P<path>.*)$', media),
    url(r'^admin/', admin.site.urls),
]

if DEBUG:
    import debug_toolbar
    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
