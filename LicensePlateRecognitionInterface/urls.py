"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('license_plate_sign_in_register_interface.urls'), name="sign_in_page"),
    path('history_page/', include('license_plate_table.urls'), name='history_page'),
    path('settings/', include('profile_and_site_settings.urls'), name='settings'),
    path('license_recognition/', include('license_recognition.urls'), name='license_reg'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
