from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from Account.forms import LoginForm, RegistrationForm


def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cleaned_data = login_form.cleaned_data
            user = authenticate(username=cleaned_data["username"], password=cleaned_data["password"])
            # 登录成功
            if user:
                login(request, user)
                return HttpResponse("Login Success")
            else:
                return HttpResponse("Login Failed")
        else:
            return HttpResponse("invalid login")

    elif request.method == "GET":
        login_form = LoginForm()
        return render(request, "Account/login.html", {"form": login_form})


def register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            return HttpResponse("Register success!")
        else:
            return HttpResponse("Register failed!!!")
    elif request.method == "GET":
        form = RegistrationForm()
        return render(request, "Account/register.html", {"form": form})
