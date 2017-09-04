from django.conf.urls import url

from .views import api_table_list, api_table_edit, api_table_delete

urlpatterns = [
    url(r'^api/table/list/$', api_table_list, name='api_table_list'),
    url(r'^api/table/list/(?P<crew>[-\w]+)/$', api_table_list, name='api_table_list'),
    url(r'^api/table/edit/$', api_table_edit, name='api_table_edit'),
    url(r'^api/table/edit/(?P<table>[-\w]+)/$', api_table_edit, name='api_table_edit'),
    url(r'^api/table/delete/$', api_table_delete, name='api_table_delete'),
    url(r'^api/table/delete/(?P<table>[-\w]+)/?$', api_table_delete, name='api_table_delete'),
]
