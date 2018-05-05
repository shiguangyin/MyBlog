from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from Article.forms import ArticleCategoryForm
from Article.models import ArticleCategory


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
