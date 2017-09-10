from django.conf.urls import url

from .views import crew_edit, api_crew_check_url, crew_view
from .views import task_new, task_save, task_info
from .views import api_crew_edit
from .views import api_user_list, api_user_edit, api_user_delete, api_user_invite, api_user_add
from .views import api_service_list, api_service_edit, api_service_delete
from .views import api_priority_list, api_priority_edit, api_priority_delete
from .views import api_service_price_edit, api_service_price_list
from .views import api_event_list

urlpatterns = [
    url(r'^view/(?P<url>[-\w]+)/$', crew_view, name='crew_view'),
    url(r'^edit/$', crew_edit, name='crew_edit'),
    url(r'^edit/(?P<url>[-\w]+)/$', crew_edit, name='crew_edit'),

    url(r'^(?P<url>[-\w]+)/task/new/$', task_new, name='task_new'),
    url(r'^task/save/$', task_save, name='task_save'),
    url(r'^task/info/(?P<uuid>[-\w]+)/$', task_info, name='task_info'),

    url(r'^api/crew/edit/$', api_crew_edit, name='api_crew_edit'),
    url(r'^api/crew/edit/(?P<crew>[-\w]+)/$', api_crew_edit, name='api_crew_edit'),

    url(r'^api/user/list/$', api_user_list, name='api_user_list'),
    url(r'^api/user/list/(?P<crew>[-\w]+)/$', api_user_list, name='api_user_list'),
    url(r'^api/user/edit/$', api_user_edit, name='api_user_edit'),
    url(r'^api/user/edit/(?P<member>[-\w]+)/(?P<type>[-\w]+)/$', api_user_edit, name='api_user_edit'),
    url(r'^api/user/delete/$', api_user_delete, name='api_user_delete'),
    url(r'^api/user/delete/(?P<member>[-\w]+)/$', api_user_delete, name='api_user_delete'),
    url(r'^api/user/invite/$', api_user_invite, name='api_user_invite'),
    url(r'^api/user/add/$', api_user_add, name='api_user_add'),
    url(r'^api/user/add/(?P<email>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<type>[-\w]+)/$', api_user_add, name='api_user_add'),

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

    url(r'^api/priority/list/$', api_priority_list, name='api_priority_list'),
    url(r'^api/priority/list/(?P<crew>[-\w]+)/$', api_priority_list, name='api_priority_list'),
    url(r'^api/priority/edit/$', api_priority_edit, name='api_priority_edit'),
    url(r'^api/priority/edit/(?P<priority>[-\w]+)/$', api_priority_edit, name='api_priority_edit'),
    url(r'^api/priority/delete/$', api_priority_delete, name='api_priority_delete'),
    url(r'^api/priority/delete/(?P<priority>[-\w]+)/?$', api_priority_delete, name='api_priority_delete'),

    url(r'^api/event/list/(?P<crew>[-\w]+)/$', api_event_list, name='api_event_list'),
    url(r'^api/event/list/(?P<crew>[-\w]+)/(?P<limit>[-\w]+)/$', api_event_list, name='api_event_list'),

    url(r'^api/crew/check/url/$', api_crew_check_url, name='api_crew_check_url'),
]
