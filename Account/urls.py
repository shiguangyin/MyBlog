from django.urls import path
from django.contrib.auth import views as auth_views
from Account import views

app_name = "Account"
password_change_extra = {
    "template_name": "Account/password_change.html",
    "post_change_redirect": "/account/password_change_done"
}

change_done_extra = {
    "template_name": "Account/password_change_done.html"
}

password_reset_extra = {
    "template_name": "Account/password_reset_form.html",
    "email_template_name": "Account/password_reset_email.html",
    "post_reset_redirect": "/account/password_reset_done",
    "subject_template_name": "Account/password_reset_subject.txt"
}

password_reset_done = {
    "template_name": "Account/password_reset_done.html"
}

password_reset_confirm = {
    "template_name": "Account/password_reset_confirm.html",
    "post_reset_redirect": "account/password_reset_complete"
}

password_reset_complete = {
    "template_name": "Account/password_reset_complete.html"
}

urlpatterns = [
    # path("login", views.user_login, name="user_login")
    path("login", auth_views.login, {"template_name": "Account/login.html"}, name="user_login"),
    path("logout", auth_views.logout, {"template_name": "Account/logout.html"}, name="user_logout"),
    path("register", views.register, name="register"),
    path("password_change", auth_views.password_change, password_change_extra, name="password_change"),
    path("password_change_done", auth_views.password_change_done, change_done_extra, name="password_change_done"),
    path("password_reset", auth_views.password_reset, password_reset_extra, name="password_reset"),
    path("password_reset_done", auth_views.password_reset_done, password_reset_done, name="password_reset_done"),
    path("password_reset_confirm/<uidb64>/<token>/", auth_views.password_reset_confirm, password_reset_confirm,
         name="password_reset_confirm"),
    path("password_reset_complete", auth_views.password_reset_complete, password_reset_complete,
         name="password_reset_complete"),
    path("self_profile", views.self_profile, name="self_profile"),
    path("edit_self_profile", views.edit_self_profile, name="edit_self_profile"),
    path("image_crop", views.image_crop, name="image_crop")
]
