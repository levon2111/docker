from django.conf import settings
from rest_framework import serializers

from apps.core.utils import send_email_job_registration, generate_unique_key
from apps.docks.models import Warehouse, Company, InvitationToUserAndWarehouseAdmin
from apps.users.models import User


class CompanyGetSerializer(serializers.ModelSerializer):
    def get_image_url(self, obj):
        return None if obj.image is None else settings.BASE_URL + obj.image.url

    image = serializers.SerializerMethodField(method_name='get_image_url')

    class Meta:
        model = Company
        fields = [
            'id',
            'name',
            'image',
        ]


class WarehouseGetSerializer(serializers.ModelSerializer):
    docks_count = serializers.ReadOnlyField(source='get_dock_count')
    company = CompanyGetSerializer(read_only=True)

    class Meta:
        model = Warehouse
        fields = [
            'id',
            'company',
            'name',
            'open_date',
            'close_date',
            'opened_overnight',
            'docks_count',
        ]


class InviteUserOrWarehouseAdminSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    last_name = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    role = serializers.CharField(required=True, allow_blank=False, allow_null=False)

    def send_mail(self, validated_data):
        invited = InvitationToUserAndWarehouseAdmin(
            token=generate_unique_key(validated_data['email']),
            role=validated_data['role'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            company=self.context['company'],
        )
        send_email_job_registration(
            'Docker',
            invited.email,
            'invite_user_warehouse_admin',
            {
                'token': invited.token,
                'name': invited.get_full_name()
            },
            'Docker Scheduler Invitation',
        )
        invited.save()

    def validate(self, data):
        self.check_email(data['email'])
        if data['role'] not in ['warehouse', 'general']:
            raise serializers.ValidationError({'detail': 'Role should be "warehouse" or "general'})
        return data

    @staticmethod
    def check_email(value):
        user = User.objects.filter(email=value).first()
        if user is not None:
            raise serializers.ValidationError('This email address is already exist.')

        return value
