from django.urls import path

from Blog import views

urlpatterns = [
    path("article/<int:article_id>", views.blog_article),
    path("", views.index)
]