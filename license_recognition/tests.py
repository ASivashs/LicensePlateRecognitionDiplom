from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile

from datetime import datetime
import json

from license_plate_table.models import License_plate
from profile_and_site_settings.models import WhiteList


class LicenseRecognitionTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch("license_plate_table.views.save_photo")
    @patch("license_plate_table.views.number_finder")
    def test_view_license_recognition_upload_photo(
        self, mock_number_finder, mock_save_photo
    ):
        mock_number_finder.return_value = "ABC123"
        mock_save_photo.return_value = None

        image_mock = SimpleUploadedFile(
            name="test_image.jpg", content=b"file_content", content_type="image/jpeg"
        )

        response = self.client.post(
            reverse("view_license_recognition"),
            {"upload_photo": True, "image": image_mock},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ABC123")

    def test_view_license_recognition_add_owner(self):
        response = self.client.post(
            reverse("view_license_recognition"),
            {"add_owner": True, "lic_plate": "ABC123", "owner": "TestOwner"},
        )

        self.assertTrue(
            WhiteList.objects.filter(
                license_plate="ABC123", user_name="TestOwner"
            ).exists()
        )

    @patch("license_plate_table.views.json_save_one")
    @patch("license_plate_table.views.download_file")
    def test_view_license_recognition_save(
        self, mock_download_file, mock_json_save_one
    ):
        mock_download_file.return_value = HttpResponse(
            json.dumps({"lic_plate": "ABC123", "region": "BY", "owner": "TestOwner"}),
            content_type="application/json",
        )
        mock_json_save_one.return_value = None

        response = self.client.post(
            reverse("view_license_recognition"),
            {"save": True, "lic_plate": "ABC123", "owner": "TestOwner"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
