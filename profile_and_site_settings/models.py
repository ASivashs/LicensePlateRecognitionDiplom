from django.db import models
from django.contrib.auth.models import User

from django_countries.fields import CountryField


class LicensePlateList(models.Model):
    car_model = models.CharField(verbose_name="Model", max_length=100)
    license_plate = models.CharField(verbose_name="License plate", max_length=10)
    region = CountryField(verbose_name="Region")

    def __str__(self):
        return self.license_plate

    class Meta:
        verbose_name = "License plate list"
        verbose_name_plural = "License plate lists"


class WhiteList(models.Model):
    user_name = models.CharField(verbose_name="User name", max_length=100)
    license_plate = models.CharField(verbose_name="License plate", max_length=10)

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = "White list"
        verbose_name_plural = "White lists"


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    user_white_list = models.ManyToManyField(
        WhiteList, verbose_name='User "White list"', blank=True, null=True
    )
    user_license_plate = models.ManyToManyField(
        LicensePlateList, verbose_name="User license plate", blank=True, null=True
    )
    notifications_about_new_features = models.BooleanField(
        verbose_name="Notification about new features",
        default=False,
        blank=True,
        null=True,
    )
    notifications_when_my_license_plate_on_photo = models.BooleanField(
        verbose_name="Notification when my license plate on photo",
        default=False,
        blank=True,
        null=True,
    )
    notifications_when_license_from_white_list_on_photo = models.BooleanField(
        verbose_name='Notification when license plate from "White list" on photo',
        default=False,
        blank=True,
        null=True,
    )
    notifications_when_unfamiliar_license_on_photo = models.BooleanField(
        verbose_name="Notification when unfamiliar license plate on photo",
        default=False,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.user.__str__()

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
