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
    open_date = models.DateTimeField()
    close_date = models.DateTimeField()
    opened_overnight = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Warehouse'


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
