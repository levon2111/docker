from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from apps.users.filters import WarehouseAdminFilter, WarehouseManagerFilter
from apps.users.models import User, CompanyWarehouseAdmins, CompanyAdmins, CompanyUser, WarehouseManager, \
    CompanyAdminsNotification
from apps.users.serializers import (
    ForgotPasswordSerializer, ConfirmAccountSerializer, ResetPasswordSerializer, SignUpSerializer,
    WarehouseAdminGetSerializer, WarehouseManagerSerializer, GetCompanyAllUserSerializer, WarehouseAdminPostSerilizer,
    CompanyUserPostSerializer, CompanyUserGetSerializer, UserPostSerializer, ChangePasswordSerializer,
    CompanyAdminsNotificationPostSerializer)


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


class Login(ObtainAuthToken):
    def get_serializer(self):
        return self.serializer_class()

    def post(self, request, *args, **kwargs):
        """
        ---
        serializer: AuthTokenSerializer
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        if not serializer.is_valid():
            return Response({
                'error': serializer.errors['non_field_errors'][0]
            }, status=status.HTTP_412_PRECONDITION_FAILED)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'id': user.pk,
            'address': user.address,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'role': user.role,
            'username': user.username,
            'token': token.key,
        })


class ForgotPasswordAPIView(APIView):
    serializer_class = ForgotPasswordSerializer

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request):
        """
        ---
        request_serializer: ForgotPasswordSerializer
        """

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.send_mail(serializer.data)
            return JsonResponse(
                {
                    'result': 'success',
                },
                status=status.HTTP_200_OK,
            )
        error = serializer.errors
        if serializer.errors and hasattr(serializer.errors, 'non_field_errors'):
            error = {
                "email": serializer.errors['non_field_errors'][0]
            }

        return Response(error, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(APIView):
    serializer_class = ResetPasswordSerializer

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request, reset_key):
        """
        ---
        request_serializer: ResetPasswordSerializer
        """

        context = {
            'request': request,
            'reset_key': reset_key,
        }
        user = User.objects.get(reset_key=context['reset_key'])
        serializer = self.serializer_class(data=request.data, context=context)
        if serializer.is_valid():
            serializer.reset(serializer.data)
            return JsonResponse(
                {
                    'email': user.email,
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmAccountAPIView(APIView):
    serializer_class = ConfirmAccountSerializer

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request):
        """
        ---
        request_serializer: ConfirmAccountSerializer
        """

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.confirm(serializer.data)
            return JsonResponse(
                {
                    'result': 'success',
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpAPIView(APIView):
    serializer_class = SignUpSerializer

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save_user(serializer.data)
            return JsonResponse(
                {
                    'result': 'success',
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyWarehouseAdminViewSet(viewsets.ModelViewSet):
    queryset = CompanyWarehouseAdmins.objects.all()
    permission_classes = [IsAuthenticated, ]
    http_method_names = ('get',)
    serializer_class = WarehouseAdminPostSerilizer
    filter_class = WarehouseAdminFilter
    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES)

    def get_queryset(self):
        company = get_user_company(self.request.user)
        if company is not None:
            return CompanyWarehouseAdmins.objects.filter(company=company)
        return CompanyWarehouseAdmins.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'GET':
            serializer_class = WarehouseAdminGetSerializer
        else:
            serializer_class = WarehouseAdminPostSerilizer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class WarehouseManagerViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        company = get_user_company(self.request.user)
        return WarehouseManager.objects.filter(admin__company=company)

    queryset = WarehouseManager.objects.all()
    serializer_class = WarehouseManagerSerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = ('post', 'delete', 'get',)
    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES)
    filter_class = WarehouseManagerFilter


class GetCompanyUsersAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        company = get_user_company(self.request.user)
        warehouse_admins = CompanyWarehouseAdmins.objects.filter(company=company)
        company_users = CompanyUser.objects.filter(company=company)
        response = GetCompanyAllUserSerializer({'warehouse_admins': warehouse_admins, 'company_users': company_users})
        print(warehouse_admins, company_users)
        return Response(response.data, status=status.HTTP_200_OK)


class CompanyUserViewSet(viewsets.ModelViewSet):
    queryset = CompanyUser.objects.all()
    permission_classes = [IsAuthenticated, ]
    http_method_names = ('get',)
    serializer_class = CompanyUserPostSerializer
    # filter_class = WarehouseAdminFilter
    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES)

    def get_queryset(self):
        company = get_user_company(self.request.user)
        if company is not None:
            return CompanyUser.objects.filter(company=company)
        return CompanyUser.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'GET':
            serializer_class = CompanyUserGetSerializer
        else:
            serializer_class = CompanyUserPostSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, ]
    http_method_names = ('delete', 'put', 'patch', 'get',)
    serializer_class = UserPostSerializer
    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES)

    @action(methods=['patch'], detail=True, permission_classes=[],
            serializer_class=ChangePasswordSerializer)
    def change_password(self, request, pk=None):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data['new_password'])
            user.save()
            return Response("Success.", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyAdminsNotificationViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        company = get_user_company(self.request.user)
        if company is not None:
            return CompanyAdminsNotification.objects.filter(company=company, seen=False)
        return CompanyAdminsNotification.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'GET':
            serializer_class = CompanyAdminsNotificationPostSerializer
        else:
            serializer_class = CompanyAdminsNotificationPostSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    queryset = CompanyAdminsNotification.objects.all()
    permission_classes = [IsAuthenticated, ]
    http_method_names = ('put', 'patch', 'get',)
    serializer_class = CompanyAdminsNotificationPostSerializer
    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES)
