from django import forms

from Article.models import ArticleCategory


class ArticleCategoryForm(forms.ModelForm):
    class Meta:
        model = ArticleCategory
        fields = ("category", )