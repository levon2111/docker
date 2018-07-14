# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'invite-user-warehouse/', views.InviteUserOrWarehouseAdminAPIView.as_view(),
        name='invite-user-warehouse'),
    url(r'accept-invitations/(?P<token>\w+)/$', views.AcceptInvitationAPIView.as_view(), name='accept-invitations'),
]
