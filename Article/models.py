from django.contrib.auth.models import User
from django.db import models


class ArticleCategory(models.Model):
    user = models.ForeignKey(User, related_name="article_category", on_delete=models.CASCADE)
    category = models.CharField(max_length=200)
    created_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.category
