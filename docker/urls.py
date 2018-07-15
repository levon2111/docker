from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from apps.core.urls import generate_url
from apps.docks.views import CompanyWarehouseViewSet, CreateWarehouseAPIView, DockModelViewSet, \
    InviteUserOrWarehouseAdminAPIView, AcceptInvitationAPIView
from apps.users.views import WarehouseManagerViewSet, CompanyWarehouseAdminViewSet, GetCompanyUsersAPIView

schema_view = get_swagger_view(title='Docker API')

router = DefaultRouter()
router.register(r'warehouse', CompanyWarehouseViewSet, base_name='warehouse')
router.register(r'warehouse-manager', WarehouseManagerViewSet, base_name='warehouse-manager')
router.register(r'company-warehouse-admin', CompanyWarehouseAdminViewSet, base_name='company-warehouse-admin')
router.register(r'dock', DockModelViewSet, base_name='dock')

urlpatterns = [
    url(r'^$', schema_view),
    generate_url('auth-users/', include('apps.users.urls')),
    generate_url('core/', include('apps.core.urls')),
    generate_url('dock/', include('apps.docks.urls')),
    url(r'^', include(router.urls)),
    url(r'create-warehouse/', CreateWarehouseAPIView.as_view(), name='create-warehouse'),
    url(r'invite-user-warehouse/', InviteUserOrWarehouseAdminAPIView.as_view(),
        name='invite-user-warehouse'),
    url(r'accept-invitations/(?P<token>\w+)/$', AcceptInvitationAPIView.as_view(), name='accept-invitations'),
    url(r'get-company-users/', GetCompanyUsersAPIView.as_view(), name='get-company-users'),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
