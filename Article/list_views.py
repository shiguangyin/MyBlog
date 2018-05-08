from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from Article.forms import CommentForm
from Article.models import ArticlePost
import redis
from MyBlog import settings

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

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
    total_views = r.incr(f"article:{article.id}:views")
    r.zincrby("article_ranking", article.id, 1)
    article_ranking = r.zrange("article_ranking", 0, -1, desc=True)[:10]
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))
    comments = article.comment.all()
    context = {
        'article': article,
        'total_views': total_views,
        "most_viewed": most_viewed,
        'comments':comments
    }

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(False)
            comment.article = article
            comment.save()
    else:
        comment_form = CommentForm()
        context['comment_form'] = comment_form

    return render(request, 'Article/article_list_detail.html', context)


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