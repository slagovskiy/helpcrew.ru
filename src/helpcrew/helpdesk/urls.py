from django.conf.urls import url

from .views import crew_edit, crew_check_url, crew_view

urlpatterns = [
    url(r'^view/(?P<url>[-\w]+)/$', crew_view, name='crew_view'),
    url(r'^edit/$', crew_edit, name='crew_edit'),
    url(r'^edit/(?P<url>[-\w]+)/$', crew_edit, name='crew_edit'),

    url(r'^check/crew/url$', crew_check_url, name='crew_check_url'),
]
