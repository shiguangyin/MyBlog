from django.shortcuts import render, get_object_or_404

# Create your views here.
from Blog.models import BlogArticle


def index(request):
    context = {}
    blogs = BlogArticle.objects.all()
    context["blogs"] = blogs
    return render(request, "Blog/index.html", context)


def blog_article(request, article_id):
    context = {}
    # article = BlogArticle.objects.get(id=article_id)
    article = get_object_or_404(BlogArticle, id=article_id)
    publish = article.publish
    context["article"] = article
    return render(request, "Blog/article_detail.html", context)
