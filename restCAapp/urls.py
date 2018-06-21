from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserViewSet
from .views import BearerAuthToken

urlpatterns = format_suffix_patterns([
    url(r'^users/$',
        UserViewSet.as_view({
                'post': 'create',
                'get': 'list'
            }),
        name='user-list'),

    url(r'^users/(?P<pk>[0-9]+)/$',
        UserViewSet.as_view({
                'get': 'retrieve',
                'patch': 'update'
            }),
        name='user-detail'),
    url(r'^token/', BearerAuthToken.as_view())
])