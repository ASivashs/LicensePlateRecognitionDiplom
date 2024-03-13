from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.view_data_table, name="license_plate_table"),
    path('license_plate_search/', views.search_view, name='license_plate_search_view')
]