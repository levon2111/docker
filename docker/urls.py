from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from apps.core.urls import generate_url
from apps.docks.views import CompanyWarehouseViewSet, CreateWarehouseAPIView, DockModelViewSet, \
    InviteUserOrWarehouseAdminAPIView, AcceptInvitationAPIView, CompanyModelViewSet, BookedDockViewSet, \
    RequestedBookedDockChangesAPIView, WarehouseAdminNotificationsViewSet, RequestedBookedDockChangesModelViewSet, \
    GetWarehouseAdminNotificationsAPIView, CompanyUserNotificationsModelViewSet
from apps.users.views import WarehouseManagerViewSet, CompanyWarehouseAdminViewSet, GetCompanyUsersAPIView, \
    CompanyUserViewSet, UserViewSet, CompanyAdminsNotificationViewSet

schema_view = get_swagger_view(title='Docker API')

router = DefaultRouter()
router.register(r'warehouse', CompanyWarehouseViewSet, base_name='warehouse')
router.register(r'warehouse-manager', WarehouseManagerViewSet, base_name='warehouse-manager')
router.register(r'company-warehouse-admin', CompanyWarehouseAdminViewSet, base_name='company-warehouse-admin')
router.register(r'company-user', CompanyUserViewSet, base_name='company-user')
router.register(r'dock', DockModelViewSet, base_name='dock')
router.register(r'users', UserViewSet, base_name='users')
router.register(r'company', CompanyModelViewSet, base_name='company')
router.register(r'booked-dock', BookedDockViewSet, base_name='booked-dock')
router.register(r'company-admin-notification', CompanyAdminsNotificationViewSet, base_name='company-admin-notification')
router.register(r'company-user-notification', CompanyUserNotificationsModelViewSet,
                base_name='company-user-notification')
router.register(r'update-booked-dock-change', RequestedBookedDockChangesModelViewSet,
                base_name='update-booked-dock-change')
router.register(r'warehouse-admin-notification', WarehouseAdminNotificationsViewSet,
                base_name='warehouse-admin-notification')

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
    url(r'get-company-all-users/', GetCompanyUsersAPIView.as_view(), name='get-company-all-users'),
    url(r'get-warehouse-admin-notifications/', GetWarehouseAdminNotificationsAPIView.as_view(),
        name='get-warehouse-admin-notifications'),
    url(r'booked-dock-change/', RequestedBookedDockChangesAPIView.as_view(), name='booked-dock-change'),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
