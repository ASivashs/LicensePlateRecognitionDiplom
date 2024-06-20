from django import forms

from profile_and_site_settings.models import Profile, LicensePlateList, WhiteList


class ProfileForm(forms.Form):
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="User name", max_length=30)
    password = forms.PasswordInput()
    confirm_password = forms.PasswordInput()


class LicensePlateForm(forms.Form):
    pass


class WhiteListForm(forms.Form):
    pass
