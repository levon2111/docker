from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from apps.core.urls import generate_url

schema_view = get_swagger_view(title='Docker API')

router = DefaultRouter()

urlpatterns = [

    url(r'^$', schema_view),
    generate_url('auth-users/', include('apps.users.urls')),
    generate_url('core/', include('apps.core.urls')),
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
