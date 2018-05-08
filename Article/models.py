from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from slugify import slugify


class ArticleCategory(models.Model):
    user = models.ForeignKey(User, related_name="article_category", on_delete=models.CASCADE)
    category = models.CharField(max_length=200)
    created_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.category


class ArticlePost(models.Model):
    author = models.ForeignKey(User, related_name="article", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    category = models.ForeignKey(ArticleCategory, related_name="article_post", on_delete=models.CASCADE)
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    user_like = models.ManyToManyField(User, related_name="article_like", blank=True)

    class Meta:
        ordering = ("title", )
        index_together = (("id", "slug"),)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(force_insert, force_update, using, update_fields)

    def get_abs_url(self):
        return reverse("Article:article_detail", args=[self.id, self.slug])

    def get_list_detail_url(self):
        return reverse('Article:article_list_detail', args=[self.id, self.slug])

class Comment(models.Model):
    article = models.ForeignKey(ArticlePost, related_name="comment", on_delete=models.CASCADE)
    commentator = models.CharField(max_length=90)
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_time', )

    def __str__(self):
        return f"Comment by {self.commentator} on {self.article}"

