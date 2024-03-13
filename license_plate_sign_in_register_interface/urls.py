from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.auth_login, name='sign_in'),
    path('register/', views.register, name='register'),
]
