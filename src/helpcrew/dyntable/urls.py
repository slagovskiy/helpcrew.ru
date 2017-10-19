from django.conf.urls import url

from .views import api_table_list, api_table_edit, api_table_delete, api_record_import
from .views import api_field_list, api_field_edit, api_field_delete
from .views import api_record_save, api_record_list, api_index_data, api_record_delete

urlpatterns = [
    url(r'^api/table/list/$', api_table_list, name='api_table_list'),
    url(r'^api/table/list/(?P<crew>[-\w]+)/$', api_table_list, name='api_table_list'),
    url(r'^api/table/edit/$', api_table_edit, name='api_table_edit'),
    url(r'^api/table/edit/(?P<table>[-\w]+)/$', api_table_edit, name='api_table_edit'),
    url(r'^api/table/delete/$', api_table_delete, name='api_table_delete'),
    url(r'^api/table/delete/(?P<table>[-\w]+)/?$', api_table_delete, name='api_table_delete'),

    url(r'^api/field/list/$', api_field_list, name='api_field_list'),
    url(r'^api/field/list/(?P<table>[-\w]+)/$', api_field_list, name='api_field_list'),
    url(r'^api/field/edit/$', api_field_edit, name='api_field_edit'),
    url(r'^api/field/edit/(?P<field>[-\w]+)/$', api_field_edit, name='api_field_edit'),
    url(r'^api/field/delete/$', api_field_delete, name='api_field_delete'),
    url(r'^api/field/delete/(?P<field>[-\w]+)/?$', api_field_delete, name='api_field_delete'),

    url(r'^api/record/save/$', api_record_save, name='api_record_save'),
    url(r'^api/record/save/(?P<table>[-\w]+)/?$', api_record_save, name='api_record_save'),
    url(r'^api/record/import/$', api_record_import, name='api_record_import'),
    url(r'^api/record/import/(?P<table>[-\w]+)/$', api_record_import, name='api_record_import'),
    url(r'^api/record/list/$', api_record_list, name='api_record_list'),
    url(r'^api/record/list/(?P<table>[-\w]+)/?$', api_record_list, name='api_record_list'),
    url(r'^api/index/data/$', api_index_data, name='api_index_data'),
    url(r'^api/index/data/(?P<table>[-\w]+)/(?P<index>[-\w]+)/?$', api_index_data, name='api_index_data'),
    url(r'^api/record/delete/$', api_record_delete, name='api_record_delete'),
    url(r'^api/record/delete/(?P<table>[-\w]+)/(?P<index>[-\w]+)/?$', api_record_delete, name='api_record_delete'),
]
