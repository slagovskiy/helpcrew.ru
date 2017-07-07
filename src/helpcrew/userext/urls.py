from django.conf.urls import url

from .views import user_profile, user_login, user_logout, user_register

urlpatterns = [
    url(r'^$', user_profile, name='user_profile'),
    url(r'^login/$', user_login, name='user_login'),
    url(r'^logout/$', user_logout, name='user_logout'),
    url(r'^register/$', user_register, name='user_register'),
    #url(r'^category/(?P<slug>[-\w]+)/$', blog_post_by_category, name='blog_post_by_category'),
]
