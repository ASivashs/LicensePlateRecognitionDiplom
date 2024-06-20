from unittest.mock import patch
from django.test import TestCase, override_settings
from django.urls import reverse

from license_plate_table.models import License_plate, WhiteList


class LicensePlateTableViewTests(TestCase):
    @override_settings(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "test_db",
                "USER": "test_user",
                "PASSWORD": "test_password",
                "HOST": "localhost",
                "PORT": "",
            }
        }
    )
    def setUp(self):
        License_plate.objects.create(license_plate="ABC123")
        WhiteList.objects.create(license_plate="ABC123", user_name="TestUser")

    @patch("license_plate_table.views.License_plate.objects.all")
    def test_view_data_table(self, mock_all):
        mock_all.return_value = License_plate.objects.filter(license_plate="ABC123")

        response = self.client.get(reverse("view_data_table"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ABC123")
        self.assertContains(response, "TestUser")

    @patch("license_plate_table.views.License_plate.objects.all")
    def test_search_view(self, mock_all):
        mock_all.return_value = License_plate.objects.filter(license_plate="ABC123")

        response = self.client.get(reverse("search_view") + "?search_query=ABC123")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ABC123")
