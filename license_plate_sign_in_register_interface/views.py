from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        cpassword = request.POST.get("password2")

        customer = User.objects.create_user(username, email, password)
        customer.save()
        return redirect("sign_in")
    return render(request, "license_plate_sign_in_register_interface/register.html")


def auth_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("settings")
        else:
            return redirect("login")
    return render(request, "license_plate_sign_in_register_interface/signin.html")
