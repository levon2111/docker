from django.conf import settings
from rest_framework import serializers

from apps.core.utils import send_email_job_registration, generate_unique_key
from apps.docks.models import Warehouse, Company, InvitationToUserAndWarehouseAdmin, Dock
from apps.users.models import User, CompanyWarehouseAdmins, WarehouseManager


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


class WarehouseManagerGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseManager
        fields = [
            'id',
            'admin',
            'warehouse'
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


class WarehousePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = [
            'name',
            'open_date',
            'close_date',
            'opened_overnight',
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


class DockCreateSerializer(serializers.ModelSerializer):
    warehouse = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(),
        allow_empty=False,
        allow_null=False
    )

    class Meta:
        model = Dock
        fields = [
            'warehouse',
            'name',
        ]


class DockGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dock
        fields = [
            'warehouse',
            'name',
        ]


class CreateWarehouseSerializer(serializers.ModelSerializer):
    warehouse_admins = serializers.ListField(required=True)
    docks = serializers.ListField(required=True)

    def save(self, validated_data):
        warehouse = Warehouse(
            company=self.context['company'],
            name=validated_data['name'],
            open_date=validated_data['open_date'],
            close_date=validated_data['close_date'],
            opened_overnight=validated_data['opened_overnight']
        )
        warehouse.save()
        new_docks = []
        for x in validated_data['docks']:
            exists = Dock.objects.filter(warehouse=warehouse, name=x).first()
            if exists is not None:
                raise serializers.ValidationError({'detail': "Warehouse and dock name combination must be unique."})
            new_dock = Dock(warehouse=warehouse, name=x)
            new_docks.append(new_dock)

        new_managers = []
        for x in validated_data['warehouse_admins']:
            new_manager = WarehouseManager(admin=CompanyWarehouseAdmins.objects.get(pk=int(x)), warehouse=warehouse)
            new_managers.append(new_manager)

        for x in new_docks:
            x.save()
        for x in new_managers:
            x.save()

        return {'warehouse': warehouse, 'docks': new_docks, 'admins': new_managers}

    def validate(self, attrs):
        warehouse_admins_array = attrs['warehouse_admins']
        for x in warehouse_admins_array:
            existing_company_warehouse_admin = CompanyWarehouseAdmins.objects.filter(
                pk=int(x),
                company=self.context['company']
            ).first()
            if existing_company_warehouse_admin is None:
                raise serializers.ValidationError({'detail': 'Warehouse Admin Not Found'})

        warehouse_docks = attrs['docks']
        for x in warehouse_docks:
            if not x:
                raise serializers.ValidationError({'detail': 'dock name is not valid'})

        exists_combination = Warehouse.objects.filter(company=self.context['company'], name=attrs['name']).first()
        if exists_combination is not None:
            raise serializers.ValidationError({'detail': 'Warehouse company and name must be unique combination.'})
        return attrs

    class Meta:
        model = Warehouse
        fields = [
            'docks',
            'warehouse_admins',
            'name',
            'open_date',
            'close_date',
            'opened_overnight',
        ]


class DockModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, allow_null=False, allow_blank=False)
    warehouse = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(),
        allow_null=False,
        allow_empty=False,
    )
    id = serializers.ReadOnlyField()

    def validate(self, attrs):
        if attrs['warehouse'].company != self.context['company']:
            raise serializers.ValidationError({'detail': 'Current company have not that warehouse.'})

        exists = Dock.objects.filter(name=attrs['name'], warehouse=attrs['warehouse']).first()
        if exists is not None:
            raise serializers.ValidationError({'detail': 'Warehouse already have that dock.'})
        return attrs

    class Meta:
        model = Dock
        fields = [
            'id',
            'name',
            'warehouse',
        ]
