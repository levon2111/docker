from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from apps.docks.filters import WarehouseFilter, BookedDockFilter
from apps.docks.models import Warehouse, InvitationToUserAndWarehouseAdmin, Dock, Company, BookedDock
from apps.docks.serializers import WarehouseGetSerializer, InviteUserOrWarehouseAdminSerializer, CompanyGetSerializer, \
    CreateWarehouseSerializer, WarehousePostSerializer, DockModelSerializer, CompanySerializer, \
    BookedDockCreateSerializer, BookedDockGetSerializer
from apps.users.models import CompanyAdmins, CompanyWarehouseAdmins, CompanyUser


def get_user_company(user):
    role = user.role
    if role == 'company':
        company = CompanyAdmins.objects.filter(user=user).first()
        return company.company if company is not None else None
    elif role == 'warehouse':
        company = CompanyWarehouseAdmins.objects.filter(user=user).first()
        return company.company if company is not None else None
    elif role == 'general':
        company = CompanyUser.objects.filter(user=user).first()
        return company.company if company is not None else None


class CompanyWarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    permission_classes = [IsAuthenticated, ]
    http_method_names = ('get', 'delete', 'put', 'patch',)
    serializer_class = WarehousePostSerializer
    filter_class = WarehouseFilter
    search_fields = ('name',)
    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES)

    def get_queryset(self):
        company = get_user_company(self.request.user)
        return Warehouse.objects.filter(company=company)

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'GET':
            serializer_class = WarehouseGetSerializer
        else:
            serializer_class = WarehousePostSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class InviteUserOrWarehouseAdminAPIView(APIView):
    serializer_class = InviteUserOrWarehouseAdminSerializer

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request):
        company = get_user_company(request.user)
        if company is not None:
            serializer = self.serializer_class(data=request.data, context={'company': company})

            if serializer.is_valid():
                serializer.send_mail(serializer.data)
                return JsonResponse(
                    {
                        'result': 'success',
                    },
                    status=status.HTTP_201_CREATED,
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Company not found'}, status=status.HTTP_400_BAD_REQUEST)


class AcceptInvitationAPIView(APIView):
    def post(self, request, token):
        invitation = InvitationToUserAndWarehouseAdmin.objects.filter(token=token).first()
        if invitation is not None:
            return JsonResponse(
                {
                    'message': 'Valid Token',
                    'email': invitation.email,
                    'first_name': invitation.first_name,
                    'last_name': invitation.last_name,
                    'role': invitation.role,
                    'company': CompanyGetSerializer(invitation.company).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response({'detail': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class CreateWarehouseAPIView(APIView):
    serializer_class = CreateWarehouseSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request):
        company = get_user_company(request.user)
        if company is not None:
            serializer = self.serializer_class(data=request.data, context={'company': company})
            if serializer.is_valid():
                new_warehouse = serializer.save(serializer.data)
                return JsonResponse(
                    {
                        'result': WarehouseGetSerializer(new_warehouse['warehouse']).data,
                    },
                    status=status.HTTP_201_CREATED,
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Company not found'}, status=status.HTTP_400_BAD_REQUEST)


class DockModelViewSet(viewsets.ModelViewSet):
    queryset = Dock.objects.all()
    serializer_class = DockModelSerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = ('post', 'get', 'put', 'patch', 'delete')

    def get_serializer_context(self):
        context = super(DockModelViewSet, self).get_serializer_context()
        context.update({
            "company": get_user_company(self.request.user)
        })
        return context

    def get_queryset(self):
        company = get_user_company(self.request.user)
        return Dock.objects.filter(warehouse__company=company)


class CompanyModelViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ('get', 'put', 'patch')


class BookedDockViewSet(viewsets.ModelViewSet):
    queryset = BookedDock.objects.all()
    serializer_class = BookedDockCreateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ('get', 'post', 'delete', 'put', 'patch')
    filter_class = BookedDockFilter

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'GET':
            serializer_class = BookedDockGetSerializer
        else:
            serializer_class = BookedDockCreateSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_queryset(self):
        company = get_user_company(self.request.user)
        if company is not None:
            return BookedDock.objects.filter(dock__warehouse__company=company)
        return BookedDock.objects.all()
