from django.urls import path
from django.contrib.auth import views as auth_views
from Account import views

app_name = "Account"
urlpatterns = [
    # path("login", views.user_login, name="user_login")
    path("login", auth_views.login, {"template_name": "Account/login.html"}, name="user_login"),
    path("logout", auth_views.logout, {"template_name": "Account/logout.html"}, name="user_logout"),
    path("register", views.register, name="register")
]
