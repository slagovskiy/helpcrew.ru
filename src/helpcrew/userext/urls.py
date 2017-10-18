from django.conf.urls import url

from .views import user_profile, user_login, user_logout, user_register, user_activate, user_save
from .views import api_check_online

urlpatterns = [
    url(r'^$', user_profile, name='user_profile'),
    url(r'^login/$', user_login, name='user_login'),
    url(r'^logout/$', user_logout, name='user_logout'),
    url(r'^register/$', user_register, name='user_register'),
    url(r'^activate/$', user_activate, name='user_activate'),
    url(r'^save/$', user_save, name='user_save'),
    url(r'^api/check/online/$', api_check_online, name='api_check_online'),
    #url(r'^category/(?P<slug>[-\w]+)/$', blog_post_by_category, name='blog_post_by_category'),
]
