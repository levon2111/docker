import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from apps.core.utils import generate_unique_key, send_email_job_registration
from apps.docks.models import InvitationToUserAndWarehouseAdmin, Warehouse
from apps.docks.serializers import CompanyGetSerializer
from apps.users.models import User, CompanyWarehouseAdmins, CompanyUser, WarehouseManager
from apps.users.validators import check_valid_password


def base64_to_image(base64_string):
    format, imgstr = base64_string.split(';base64,')
    ext = format.split('/')[-1]

    base64_string = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)  # You can save this as file instance.
    return base64_string


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'address',
            'role',
        ]


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    @staticmethod
    def send_mail(validated_data):
        user = User.objects.get(email=validated_data['email'])
        user.reset_key = generate_unique_key(user.email)

        send_email_job_registration(
            'Docker',
            user.email,
            'reset_password',
            {
                'reset_key': user.reset_key,
                'name': user.first_name
            },
            'Reset your password',
        )
        user.save()

    def validate(self, data):
        self.check_email(data['email'])

        return data

    @staticmethod
    def check_email(value):
        user = User.objects.filter(email=value)

        if not user.exists():
            raise serializers.ValidationError('This email address does not exist.')

        if not user.filter(is_active=True).exists():
            raise serializers.ValidationError('Your account is inactive.')

        return value


class ConfirmAccountSerializer(serializers.Serializer):
    token = serializers.CharField()

    @staticmethod
    def confirm(validated_data):
        user = User.objects.get(email_confirmation_token=validated_data['token'])
        user.is_active = True
        user.email_confirmation_token = None
        user.save()

    def validate(self, data):
        if not User.objects.filter(email_confirmation_token=data['token']).exists():
            raise serializers.ValidationError('Invalid token.')

        return data


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    repeat_password = serializers.CharField()

    def reset(self, validated_data):
        user = User.objects.get(reset_key=self.context['reset_key'])
        user.set_password(validated_data['password'])
        user.reset_key = None
        user.save()

    def validate(self, data):
        check_valid_password(data)
        self.check_valid_token()

        return data

    def check_valid_token(self):
        if not User.objects.filter(reset_key=self.context['reset_key']).exists():
            raise serializers.ValidationError('Token is not valid.')


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    repeat_password = serializers.CharField()

    @staticmethod
    def save_user(validated_data):
        invitation = InvitationToUserAndWarehouseAdmin.objects.filter(email=validated_data['email']).first()
        if invitation is not None:
            user = User(email=validated_data['email'])
            user.set_password(validated_data['password'])
            user.first_name = invitation.first_name
            user.last_name = invitation.last_name
            user.is_staff = False
            user.is_active = True
            user.role = invitation.role
            user.email_confirmation_token = generate_unique_key(user.email)
            user.save()
            if user.role == 'general':
                company_general_user = CompanyUser(user=user, company=invitation.company)
                company_general_user.save()
            elif user.role == 'warehouse':
                warehouse_admin = CompanyWarehouseAdmins(user=user, company=invitation.company)
                warehouse_admin.save()
            InvitationToUserAndWarehouseAdmin.objects.filter(email=validated_data['email']).delete()
        else:
            raise serializers.ValidationError({'detail': 'Invalid email'})

    def validate(self, data):
        check_valid_password(data)
        self.check_valid_email(data['email'])

        return data

    @staticmethod
    def check_valid_email(value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError({'detail': 'This email address already exists.'})

        return value


class WarehouseAdminGetSerializer(serializers.ModelSerializer):
    user = UserGetSerializer()
    company = CompanyGetSerializer(read_only=True)

    class Meta:
        model = CompanyWarehouseAdmins
        fields = [
            'id',
            'user',
            'company',
        ]


class WarehouseManagerSerializer(serializers.ModelSerializer):
    admin = serializers.PrimaryKeyRelatedField(
        queryset=CompanyWarehouseAdmins.objects.all(),
        allow_null=False,
        allow_empty=False,
    )
    warehouse = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(),
        allow_null=False,
        allow_empty=False,
    )
    id = serializers.ReadOnlyField()

    def validate(self, attrs):
        manager = WarehouseManager.objects.filter(admin=attrs['admin'], warehouse=attrs['warehouse']).first()
        if manager is not None:
            raise serializers.ValidationError({'detail': 'The admin and warehouse combination already exist.'})
        return attrs

    class Meta:
        model = WarehouseManager
        fields = [
            'id',
            'admin',
            'warehouse',
        ]
