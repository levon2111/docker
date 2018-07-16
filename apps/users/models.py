import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.models import AbstractBaseModel
from apps.docks.models import Company, Warehouse


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'user_images/' + filename


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=False):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            is_active=is_active,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_active = True
        user.role = 'admin'
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractUser, AbstractBaseModel):
    ROLE_CHOICES = (
        ('None', 'Without role'),
        ('admin', 'Super Admin'),
        ('company', 'Company Admin'),
        ('warehouse', 'Warehouse Admin'),
        ('general', 'General User'),
    )

    role = models.CharField(choices=ROLE_CHOICES, max_length=32, default='company')
    username = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    first_name = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    last_name = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    address = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    email = models.EmailField(unique=True)
    email_confirmation_token = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    reset_key = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'Users'


class AdminUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'AdminUser: {0}'.format(self.user.email)


class CompanyAdmins(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return 'CompanyAdmins: {0}'.format(self.user.email)

    class Meta:
        verbose_name_plural = 'Company Admin'


class CompanyWarehouseAdmins(AbstractBaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'CompanyWarehouseAdmin: {0}'.format(self.user.email)


class WarehouseManager(models.Model):
    admin = models.ForeignKey(CompanyWarehouseAdmins, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    def __str__(self):
        return 'WarehouseManager: {0}'.format(self.admin.user.email)

    class Meta:
        verbose_name_plural = 'Warehouse User'


class CompanyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return 'CompanyUser: {0}'.format(self.user.email)

    class Meta:
        verbose_name_plural = 'Company User'


class CompanyAdminsNotification(AbstractBaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    text = models.TextField(null=False)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Company admin Notifications'
