import uuid

from django.core.exceptions import NON_FIELD_ERRORS
from django.db import models

from apps.core.models import AbstractBaseModel


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'company_logo/' + filename


class Company(AbstractBaseModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    image = models.ImageField(
        upload_to=get_file_path,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Company'


class Warehouse(AbstractBaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)
    open_date = models.TimeField()
    close_date = models.TimeField()
    opened_overnight = models.BooleanField(default=False)

    @property
    def get_dock_count(self):
        return Dock.objects.filter(warehouse=self.id).count()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Warehouse'
        unique_together = (("company", "name"),)


class Dock(AbstractBaseModel):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Dock'


class BookedDock(AbstractBaseModel):
    dock = models.ForeignKey(Dock, on_delete=models.CASCADE)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.dock.name

    class Meta:
        verbose_name_plural = 'Booked Dock'


class InvitationToUserAndWarehouseAdmin(AbstractBaseModel):
    ROLE_CHOICES = (
        ('warehouse', 'Warehouse Admin'),
        ('general', 'General User'),
    )

    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    token = models.TextField(null=False, blank=False)
    role = models.CharField(choices=ROLE_CHOICES, max_length=32, default='company')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def __str__(self):
        return '%s %s  Role: %s' % (self.first_name, self.last_name, self.role)

    class Meta:
        verbose_name_plural = 'Invitation To User And Warehouse Admin'
