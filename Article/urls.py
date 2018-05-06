from django.urls import path

from Article import list_views
from . import views

app_name = "Article"
urlpatterns = [
    path("category", views.article_category, name="article_category"),
    path("category_rename", views.rename_category, name="category_rename"),
    path("category_delete", views.delete_category, name="category_delete"),
    path("post", views.article_post, name="article_post"),
    path("list", views.article_list, name="article_list"),
    path("detail/<id>/<slug>", views.article_detail, name="article_detail"),
    path("delete", views.article_delete, name="article_delete"),
    path("edit/<id>", views.article_edit, name="article_edit"),
    path("article_list/<id>/<slug>", list_views.article_detail, name="article_list_detail"),
    path("", list_views.article_titles, name="article_titles")
]
