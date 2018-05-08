from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from Article.models import ArticlePost


def article_titles(request, username=None):
    if username:
        user = User.objects.get(username=username)
        try:
            user_profile = user.user_profile
        except:
            user_profile = None
        article_list = ArticlePost.objects.filter(author=user)
    else:
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
        'page': current_page,
    }
    if username:
        context['user'] = user
        context['usr_profile'] = user_profile
        return render(request, 'Article/author_articles.html', context)
    return render(request, 'Article/article_titles.html', context)


def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    context = {
        'article': article
    }
    return render(request, 'Article/article_detail.html', context)

@require_POST
@csrf_exempt
@login_required(login_url='/account/login')
def article_like(request):
    article_id = request.POST["id"]
    action = request.POST["action"]
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action == "1":
                article.user_like.add(request.user)
                return HttpResponse("1")
            else:
                article.user_like.remove(request.user)
                return HttpResponse("0")
        except:
            return HttpResponse("-1")

    return HttpResponse("-1")