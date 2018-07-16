import uuid

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

    user = models.IntegerField(null=False, blank=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    po_number = models.CharField(max_length=255, null=False, blank=False)
    truck_number = models.CharField(max_length=255, null=False, blank=False)

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
    user = models.IntegerField(null=False, blank=False)

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def __str__(self):
        return '%s %s  Role: %s' % (self.first_name, self.last_name, self.role)

    class Meta:
        verbose_name_plural = 'Invitation To User And Warehouse Admin'


class RequestedBookedDockChanges(AbstractBaseModel):
    booked_dock = models.ForeignKey(BookedDock, on_delete=models.CASCADE)

    dock_from = models.ForeignKey(Dock, related_name="from_dock", on_delete=models.CASCADE, null=True, blank=True)
    dock_to = models.ForeignKey(Dock, related_name="to_dock", on_delete=models.CASCADE, null=True, blank=True)

    new_start_date = models.DateTimeField(null=True, blank=True)
    new_end_date = models.DateTimeField(null=True, blank=True)

    old_start_date = models.DateTimeField(null=True, blank=True)
    old_end_date = models.DateTimeField(null=True, blank=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return "Requested Book changes: ID  %s" % self.pk

    class Meta:
        verbose_name_plural = 'Requested Book changes'


class WarehouseAdminNotifications(AbstractBaseModel):
    user = models.IntegerField(null=False, blank=False)
    text = models.TextField(null=False)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Warehouse Admin Notifications'


class CompanyUserNotifications(AbstractBaseModel):
    user = models.IntegerField(null=False, blank=False)
    text = models.TextField(null=False)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Company User Notifications'
