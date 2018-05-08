from django import forms

from Article.models import ArticleCategory, ArticlePost, Comment


class ArticleCategoryForm(forms.ModelForm):
    class Meta:
        model = ArticleCategory
        fields = ("category", )


class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ('title', 'body')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('commentator', 'body')