from django.db import models
from django.urls import reverse

from profile_and_site_settings.models import WhiteList


class License_plate(models.Model):
    license_plate = models.CharField("License plate", max_length=40, null=True)
    region = models.CharField("Region", max_length=20, null=True, blank=True)
    date_time = models.DateTimeField("Date and time", null=False)
    user_name = models.CharField("User name", max_length=50, null=True, blank=True)
    field_name = models.ImageField("Image", upload_to='license_plate_table/static/images', height_field=None,
                                   width_field=None, max_length=100)
    source = models.CharField("Source", max_length=30, null=False)

    def __str__(self):
        return self.license_plate

    @staticmethod
    def get_absolute_url():
        return reverse('license_plate_data')
