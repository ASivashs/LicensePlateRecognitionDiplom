from django.contrib import admin

from profile_and_site_settings.models import Profile, LicensePlateList, WhiteList


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "User settings",
            {
                "fields": [
                    "user",
                ]
            },
        ),
        ("License plate lists", {"fields": ["user_white_list", "user_license_plate"]}),
        (
            "Notifications",
            {
                "fields": [
                    "notifications_about_new_features",
                    "notifications_when_my_license_plate_on_photo",
                    "notifications_when_license_from_white_list_on_photo",
                    "notifications_when_unfamiliar_license_on_photo",
                ]
            },
        ),
    ]


@admin.register(LicensePlateList)
class UserLicensePlateListAdmin(admin.ModelAdmin):
    pass


@admin.register(WhiteList)
class UserWhiteListAdmin(admin.ModelAdmin):
    pass
