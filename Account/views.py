from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from Account.forms import LoginForm, RegistrationForm, UserProfileForm, UserForm, UserInfoForm
from Account.models import UserProfile, UserInfo


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
        user_profile_from = UserProfileForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            new_user_profile = user_profile_from.save(False)
            new_user_profile.user = new_user
            new_user_profile.save()
            new_user_info = UserInfo.objects.create(user=new_user)
            new_user_info.save()
            return redirect(reverse('Account:user_login'))
        else:
            return HttpResponse("Register failed!!!")
    elif request.method == "GET":
        form = RegistrationForm()
        user_profile_from = UserProfileForm()
        context = {"form": form, "user_profile_form": user_profile_from}
        return render(request, "Account/register.html", context)


@login_required(login_url="/account/login/")
def self_profile(request):
    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user)
    user_info = UserInfo.objects.get(user=user)
    context = {
        "user": user,
        "user_profile": user_profile,
        "user_info": user_info
    }
    img = user_profile.avatar
    print(img)
    return render(request, "Account/self_profile.html", context)


@login_required(login_url="/account/login")
def edit_self_profile(request):
    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user)
    user_info = UserInfo.objects.get(user=user)
    if request.method == "POST":
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)
        user_info_form = UserInfoForm(request.POST)
        if user_form.is_valid() and user_profile_form.is_valid() and user_info_form.is_valid():
            user_cd = user_form.cleaned_data
            user_profile_cd = user_profile_form.cleaned_data
            user_info_cd = user_info_form.cleaned_data

            user.email = user_cd["email"]
            user_profile.birthday = user_profile_cd["birthday"]
            user_profile.phone = user_profile_cd["phone"]
            user_info.school = user_info_cd["school"]
            user_info.address = user_info_cd["address"]
            user_info.aboutme = user_info_cd["aboutme"]

            user.save()
            user_profile.save()
            user_info.save()
        return HttpResponseRedirect("/account/self_profile")
    elif request.method == "GET":
        user_form = UserForm(instance=request.user)
        user_profile_form = UserProfileForm(initial={
            "birthday": user_profile.birthday,
            "phone": user_profile.phone
        })
        user_info_form = UserInfoForm(initial={
            "school": user_info.school,
            "address": user_info.address,
            "aboutme": user_info.aboutme
        })
        context = {
            "user_form": user_form,
            "user_profile_form": user_profile_form,
            "user_info_form": user_info_form
        }
        return render(request, "Account/edit_self_profile.html", context)


@login_required(login_url="/account/login")
def image_crop(request):
    if request.method == "POST":
        img = request.POST["img"]
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.avatar = img
        user_profile.save()
        return HttpResponse("1")

    elif request.method == "GET":
        return render(request, "Account/image_crop.html")
