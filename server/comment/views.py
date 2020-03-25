from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Comment
import datetime
# Create your views here.


@require_http_methods(['POST'])
def create(request):
    content = request.POST.get("content")
    writer = request.session.get("account")
    comment = Comment(
        content=content,
        writer=writer
    )
    comment.save()
    return JsonResponse({"msg": "done"})


def index(request):
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    comment_list = Comment.objects.all()
    new_add = get_new_add()
    return render(
        request,
        'comment/index.html',
        {
            "comment_page": get_page(comment_list, page),
            "new_count": len(new_add),
            "len": len(comment_list)
        }
    )


def get_new_add():
    now = datetime.datetime.now()
    this_week_start = now - datetime.timedelta(days=now.weekday())
    this_week_end = now + datetime.timedelta(days=6 - now.weekday())
    comment_list = Comment.objects.filter(
        leave_time__lte=this_week_end,
        leave_time__gte=this_week_start
    )
    return comment_list


def get_page(obj_list, page):
    paginator = Paginator(obj_list, 10)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except InvalidPage:
        pass
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page
