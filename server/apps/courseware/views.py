from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.http import require_http_methods
from wsgiref.util import FileWrapper
from server.settings import RESOURCES_DIR, BASE_DIR
from utils.FileUtil import *
from .models import Courseware
import os
import mimetypes
import re
import time
# Create your views here.


def index(request):
    courseware_list = Courseware.objects.all().order_by("ordinal")
    if len(courseware_list) == 0:
        return render(
            request,
            'courseware/index.html',
            {"len": 0}
        )
    num = courseware_list[0].ordinal
    if request.GET.get("ord"):
        num = int(request.GET.get("ord"))
    courseware_to_show = Courseware.objects.filter(ordinal=num)
    if len(courseware_to_show) != 1:
        return HttpResponse(status=404)
    return render(
        request,
        'courseware/index.html',
        {
            "courseware_list": courseware_list,
            "len": len(courseware_list),
            "show_cw": courseware_to_show[0]
        }
    )


def create(request):
    if request.method == 'GET':
        c_all = Courseware.objects.all()
        ordinal = c_all[len(c_all) - 1].ordinal + 1 \
            if len(c_all) > 0 \
            else 1
        return render(request, 'courseware/create.html', {"ordinal": ordinal})
    if request.method == 'POST':
        ordinal = request.POST.get("ordinal")
        title = request.POST.get("title")
        courseware_type = request.POST.get("file_type")
        couseware_file = request.FILES["cw_file"]
        filename = str(couseware_file.name)
        stuffix = os.path.splitext(filename)[-1]
        saved_dir = os.path.join(RESOURCES_DIR, 'courseware', str(ordinal))
        make_dir(saved_dir)
        courseware_path = os.path.join(
            saved_dir,
            str(ordinal) + stuffix
        )
        write_file(couseware_file, courseware_path)
        show_path = courseware_path.replace(RESOURCES_DIR, '/resources')
        cw = Courseware(
            title=title,
            ordinal=ordinal,
            file_type=courseware_type,
            file_path=courseware_path,
            show_path=show_path
        )
        cw.save()
        return redirect('/courseware/index')


@require_http_methods(['POST'])
def modify(request, c_id):
    cw = Courseware.objects.filter(id=c_id)
    if len(cw) == 1:
        if request.POST.get("operation") == "remove":
            remove_file(cw[0].file_path)
            os.rmdir(
                os.path.join(
                    RESOURCES_DIR,
                    'courseware',
                    str(cw[0].ordinal)
                )
            )
            cw.delete()
            return JsonResponse({"msg": "done"})
        c_path = cw[0].file_path
        f_type = cw[0].file_type
        s_path = cw[0].show_path
        if request.POST.get("file_type"):
            f_type = request.POST.get("file_type")
        if request.FILES.get("cw_file"):
            courseware_file = request.FILES["cw_file"]
            make_dir(os.path.dirname(cw[0].file_path))
            stuffix = os.path.splitext(courseware_file.name)[-1]
            tick = time.strftime("%y%m%d%H%M%S", time.localtime())
            ordinal = cw[0].ordinal
            saved_path = os.path.join(
                RESOURCES_DIR,
                'courseware',
                str(cw[0].ordinal),
                str(ordinal) + tick + stuffix
            )
            write_file(courseware_file, saved_path)
            c_path = saved_path
            s_path = c_path.replace(RESOURCES_DIR, '/resources')
        ret = cw.update(
            title=request.POST.get("title"),
            file_type=f_type,
            file_path=c_path,
            show_path=s_path
        )
        if ret == 1:
            return redirect("/courseware/index")
    return JsonResponse({"msg": "failed"})


def detail(request, c_id):
    cw = Courseware.objects.filter(id=c_id)
    if len(cw) == 1:
        return render(
            request,
            "courseware/detail.html",
            {"courseware": cw[0]}
        )
    return HttpResponse(status=404)


@require_http_methods(['GET'])
def stream(request):
    http_range = request.META.get("HTTP_RANGE", '').strip()
    range_re = re.compile(r"bytes\s*=\s*(\d+)\s*-\s*(\d*)", re.I)
    range_match = range_re.match(http_range)
    file_path = BASE_DIR + request.GET.get("path")
    if not os.path.isfile(file_path):
        return HttpResponse(status=404)
    file_size = os.path.getsize(file_path)
    content_type, encoding = mimetypes.guess_type(file_path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        start_byte, end_byte = range_match.groups()
        start_byte = int(start_byte) if start_byte else 0
        end_byte = start_byte + 1024 * 1024 * 10
        if end_byte >= file_size:
            end_byte = file_size - 1
        stream_length = end_byte - start_byte + 1
        resp = StreamingHttpResponse(
            file_iterator(
                file_path,
                offset=start_byte,
                length=stream_length
            ),
            status=206,
            content_type=content_type
        )
        resp['Content-Length'] = str(stream_length)
        resp['Content-Range'] = \
            'bytes {0}-{1}/{2}'.format(
                start_byte,
                end_byte,
                file_size
        )
    else:
        resp = StreamingHttpResponse(
            FileWrapper(
                open(file_path, "rb"),
                content_type=content_type
            )
        )
        resp['Content-Length'] = str(file_size)
    resp['Accept-Ranges'] = "bytes"
    return resp


@require_http_methods(['GET'])
def download(request):
    path = request.GET.get("path")
    return download_response(path)
