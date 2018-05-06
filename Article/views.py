from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from Article.forms import ArticleCategoryForm, ArticlePostForm
from Article.models import ArticleCategory, ArticlePost


@login_required(login_url="/account/login")
@csrf_exempt
def article_category(request):
    if request.method == 'POST':
        cate_name = request.POST["cate_name"]
        cates = ArticleCategory.objects.filter(user=request.user, category=cate_name)
        if cates:
            return HttpResponse(-1)
        else:
            ArticleCategory.objects.create(user=request.user, category=cate_name)
            return HttpResponse(1)
    else:
        cates = ArticleCategory.objects.filter(user=request.user)
        cate_form = ArticleCategoryForm()
        context = {
            "cates": cates,
            "cate_form": cate_form
        }
        return render(request, "Article/article_category.html", context)


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def rename_category(request):
    cate_id = request.POST["cate_id"]
    cate_name = request.POST["cate_name"]
    try:
        cate = ArticleCategory.objects.get(id=cate_id)
        cate.category = cate_name
        cate.save()
        return HttpResponse("1")
    except:
        return HttpResponse(-1)


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def delete_category(request):
    cate_id = request.POST["cate_id"]
    try:
        cate = ArticleCategory.objects.get(id=cate_id)
        cate.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("-1")


@login_required(login_url='/account/login')
@csrf_exempt
def article_post(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(False)
                new_article.author = request.user
                new_article.category = request.user.article_category.get(id=request.POST["cate_id"])
                new_article.save()
                return HttpResponse("1")
            except Exception as e:
                print(e)
                return HttpResponse("-1")
        else:
            return HttpResponse("-1")
    else:
        article_post_form = ArticlePostForm()
        article_cates = request.user.article_category.all()
        context = {
            "article_post_form": article_post_form,
            "article_cates": article_cates
        }
        return render(request, "Article/article_post.html", context)


@login_required(login_url='/account/login')
def article_list(request):
    article_list = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(article_list, 2)
    page = request.GET.get('page')
    try:
        current = paginator.page(page)
        articles = current.object_list
    except PageNotAnInteger:
        current = paginator.page(1)
        articles = current.object_list
    except EmptyPage:
        current = paginator.page(paginator.num_pages)
        articles = current.object_list
    context = {
        "articles": articles,
        "page": current
    }
    return render(request, "Article/article_list.html", context)


@login_required(login_url='/account/login')
def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    context = {
        "article": article
    }
    return render(request, "Article/article_detail.html", context)


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def article_delete(request):
    article_id = request.POST["article_id"]
    try:
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return HttpResponse("1")
    except Exception as e:
        print(e)
        return HttpResponse("-1")


@login_required(login_url='/account/login')
@csrf_exempt
def article_edit(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        try:
            article.category = request.user.article_category.get(id=request.POST["cate_id"])
            article.title = request.POST["title"]
            article.body = request.POST["body"]
            article.save()
            return HttpResponse("1")

        except Exception as e:
            print(e)
            return HttpResponse("-1")
    else:
        cates = ArticleCategory.objects.filter(user=request.user)
        article = get_object_or_404(ArticlePost, id=id)
        article_form = ArticlePostForm(initial={
            "title": article.title
        })
        article_category = article.category
        context = {
            'cates': cates,
            'article': article,
            'article_form': article_form,
            'article_category': article_category
        }
        return render(request, 'Article/article_edit.html', context)

