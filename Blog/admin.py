from django.contrib import admin

# Register your models here.

from .models import BlogArticle


@admin.register(BlogArticle)
class BlogArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "publish", "author")
    list_filter = ("publish", "author")
    search_fields = ("title", "body")
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ["publish", "author"]


# admin.site.register(BlogArticle, BlogArticleAdmin)
