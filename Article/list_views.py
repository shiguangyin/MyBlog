from django.shortcuts import render, get_object_or_404
from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger
from Article.models import ArticlePost


def article_titles(request):
    article_list = ArticlePost.objects.all()
    paginator = Paginator(article_list, 2)
    page_num = request.GET.get("page")
    try:
        current_page = paginator.page(page_num)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    context = {
        'articles': articles,
        'page': current_page
    }
    return render(request, 'Article/article_titles.html', context)


def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    context = {
        'article': article
    }
    return render(request, 'Article/article_detail.html', context)