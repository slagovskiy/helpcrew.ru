from django.conf.urls import url

from .views import crew_edit, crew_edit_user_edit, api_crew_check_url, crew_view
from .views import api_user_list
from .views import api_service_list, api_service_edit, api_service_delete
from .views import api_service_price_edit, api_service_price_list

urlpatterns = [
    url(r'^view/(?P<url>[-\w]+)/$', crew_view, name='crew_view'),
    url(r'^edit/$', crew_edit, name='crew_edit'),
    url(r'^edit/(?P<url>[-\w]+)/$', crew_edit, name='crew_edit'),
    url(r'^edit/(?P<url>[-\w]+)/u/(?P<email>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<type>[-\w]+)/$',
        crew_edit_user_edit, name='crew_edit_user_edit'),

    url(r'^api/user/list/$', api_user_list, name='api_user_list'),
    url(r'^api/user/list/(?P<crew>[-\w]+)/$', api_user_list, name='api_user_list'),
    url(r'^api/service/list/$', api_service_list, name='api_service_list'),
    url(r'^api/service/list/(?P<crew>[-\w]+)/$', api_service_list, name='api_service_list'),
    url(r'^api/service/edit/$', api_service_edit, name='api_service_edit'),
    url(r'^api/service/edit/(?P<service>[-\w]+)/$', api_service_edit, name='api_service_edit'),
    url(r'^api/service/delete/$', api_service_delete, name='api_service_delete'),
    url(r'^api/service/delete/(?P<service>[-\w]+)/?$', api_service_delete, name='api_service_delete'),

    url(r'^api/service/price/edit/$', api_service_price_edit, name='api_service_price_edit'),
    url(r'^api/service/price/edit/(?P<price>[-\w]+)/$', api_service_price_edit, name='api_service_price_edit'),
    url(r'^api/service/price/list/$', api_service_price_list, name='api_service_price_list'),
    url(r'^api/service/price/list/(?P<service>[-\w]+)/$', api_service_price_list, name='api_service_price_list'),

    url(r'^api/crew/check/url/$', api_crew_check_url, name='api_crew_check_url'),
]
