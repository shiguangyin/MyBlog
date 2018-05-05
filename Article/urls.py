from django.urls import path
from . import views

app_name = "Article"
urlpatterns = [
    path("category", views.article_category, name="article_category"),
    path("category_rename", views.rename_category, name="category_rename"),
    path("category_delete", views.delete_category, name="category_delete")
]
