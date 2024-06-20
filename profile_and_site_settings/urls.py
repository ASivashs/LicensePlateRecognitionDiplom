from django.urls import path

from profile_and_site_settings.views import SettingsView


urlpatterns = [
    path("", SettingsView.as_view(), name="profile_settings"),
]
