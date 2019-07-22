from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from .settings import DEBUG
from .media.views import media
from .views import index, test, go_crew


from .userext.api import APIUser, APIChangePassword, APIUploadAvatar, APIUserRegister, APIUserRestore


urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^test/$', test, name='test'),
    url(r'^u/', include('helpcrew.userext.urls')),
    url(r'^p/(?P<url>[-\w]+)/$', go_crew, name='crew_view_redirect'),
    url(r'^c/', include('helpcrew.helpdesk.urls')),
    url(r'^t/', include('helpcrew.dyntable.urls')),

    url(r'^media/(?P<path>.*)$', media),
    url(r'^admin/', admin.site.urls),

    # JWT auth
    url(r'^api/v1/auth/obtain_token/', obtain_jwt_token),
    url(r'^api/v1/auth/refresh_token/', refresh_jwt_token),

    # The rest of the endpoints
    #url(r'^api/v1/', include('project.api', namespace='apiv1')),

    url('^api/v1/user/password/', APIChangePassword.as_view()),
    url('^api/v1/user/restore/', APIUserRestore.as_view()),
    url('^api/v1/user/register/', APIUserRegister.as_view()),
    url('^api/v1/user/avatar/', APIUploadAvatar.as_view()),
    url('^api/v1/user/', APIUser.as_view()),
]

if DEBUG:
    import debug_toolbar
    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
