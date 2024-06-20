from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_license_recognition, name="license_recognition"),
]
