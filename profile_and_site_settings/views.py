from django.shortcuts import render
from django.views import generic

from profile_and_site_settings.models import Profile, WhiteList, LicensePlateList
from profile_and_site_settings.forms import ProfileForm


class SettingsView(generic.View):
    profile_form = ProfileForm
    template_name = "profile_and_site_settings/settings.html"

    def get(self, request):
        form = self.profile_form()
        plate_list_data = LicensePlateList.objects.all()
        white_list_data = WhiteList.objects.all()
        return render(request, self.template_name, {
            "form": form,
            "plate_list": plate_list_data,
            "white_list": white_list_data,
        })

    def post(self, request):
        form = self.profile_form(request.POST)
        if 'delete_license_plate' in request.POST:
            delete_license_plate_list_data = list(LicensePlateList.objects.all())[-1]
            license_plate_list_data = LicensePlateList.objects.filter(license_plate=delete_license_plate_list_data)
            license_plate_list_data.delete()
        if 'delete_white_list' in request.POST:
            delete_white_list_data = list(WhiteList.objects.all())[-1]
            for item in WhiteList.objects.all():
                print(item)
            white_list_data = WhiteList.objects.filter(user_name=delete_white_list_data)
            white_list_data.delete()
        if 'profile_save' in request.POST:
            profile_email = request.POST['email_profile']
            profile_username = request.POST['username_profile']
            profile_password = request.POST['password_profile']
            profile_password_submit = request.POST['confirm_password_profile']
            profile_data = Profile.user.objects.create(
                email=profile_email,
                username=profile_username,
                password=profile_password,
            )
        if 'add_license_plate' in request.POST:
            license_plate_model = request.POST['model_license_plates']
            license_plate_license_plates = request.POST['license_plate_license_plates']
            license_plate_region = request.POST['region_license_plates']
            license_plate_list_data = LicensePlateList.objects.create(
                car_model=license_plate_model,
                license_plate=license_plate_license_plates,
                region=license_plate_region,
            )
        if 'white_list' in request.POST:
            white_list_user_name = request.POST['user_name_white_list']
            white_list_license_plate = request.POST['license_plate_white_list']
            white_list_data = WhiteList.objects.create(
                user_name=white_list_user_name,
                license_plate=white_list_license_plate,
            )
        license_plate_list_data = LicensePlateList.objects.all()
        white_list_data = WhiteList.objects.all()
        return render(request, self.template_name, {
            "form": form,
            "plate_list": license_plate_list_data,
            "white_list": white_list_data,
        })
