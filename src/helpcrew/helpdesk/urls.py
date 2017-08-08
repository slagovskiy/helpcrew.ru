from django.conf.urls import url

from .views import crew_edit, crew_edit_user_edit, crew_check_url, crew_view
from .views import api_service_list

urlpatterns = [
    url(r'^view/(?P<url>[-\w]+)/$', crew_view, name='crew_view'),
    url(r'^edit/$', crew_edit, name='crew_edit'),
    url(r'^edit/(?P<url>[-\w]+)/$', crew_edit, name='crew_edit'),
    url(r'^edit/(?P<url>[-\w]+)/u/(?P<email>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<type>[-\w]+)/$',
        crew_edit_user_edit, name='crew_edit_user_edit'),

    url(r'^api/service/list/$', api_service_list, name='api_service_list'),
    url(r'^api/service/list/(?P<crew>[-\w]+)/$', api_service_list, name='api_service_list'),

    #url(r'^api/service/price/list/$', api_service_price_list, name='api_service_price_list'),
    #url(r'^api/service/price/list/(?P<service>[-\w]+)/$', api_service_price_list, name='api_service_price_list'),

    url(r'^check/crew/url$', crew_check_url, name='crew_check_url'),
]
