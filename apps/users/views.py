from django.http import JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import User
from apps.users.serializers import (
    ForgotPasswordSerializer, ConfirmAccountSerializer, ResetPasswordSerializer, SignUpSerializer)


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
