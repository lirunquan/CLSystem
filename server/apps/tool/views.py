from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from utils.FileUtil import write_str_file, remove_file
from server.settings import RESOURCES_DIR
from subprocess import Popen, PIPE
import json
import os
import time
# Create your views here.


def online_run(request):
    return render(request, 'tool/online_run.html')


@require_http_methods(['POST'])
def run(request):
    data = json.loads(request.body)
    ret = {}
    code = data["code"]
    input_str = data["input"]
    now = str(time.time()).replace('.', '')
    src_temp = os.path.join(
        RESOURCES_DIR,
        'tools',
        "src_" + now + ".c"
    )
    write_str_file(code, src_temp)
    input_temp = os.path.join(
        RESOURCES_DIR,
        'tools',
        "temp_" + now + ".txt"
    )
    write_str_file(input_str, input_temp)
    exe = os.path.join(
        RESOURCES_DIR,
        'tools',
        "main_" + now
    )
    compile_cmd = "gcc {0} -o {1}".format(src_temp, exe)
    compiling = Popen(
        compile_cmd,
        shell=True,
        stdin=PIPE,
        stderr=PIPE,
        stdout=PIPE
    )
    err = compiling.stderr.read()
    if len(err) != 0:
        ret["msg"] = "error"
        ret["error"] = str(err, encoding='utf-8')
        ret["output"] = ""
        remove_file(input_temp)
        remove_file(src_temp)
        return JsonResponse(ret)
    run_cmd = "{0} < {1}".format(exe, input_temp)
    run_exe = Popen(
        run_cmd,
        shell=True,
        stdin=PIPE,
        stderr=PIPE,
        stdout=PIPE
    )
    err = run_exe.stderr.read()
    output = run_exe.stdout.read()
    if len(err) == 0:
        ret["msg"] = "done"
        ret["output"] = str(output, encoding='utf-8')
        ret["error"] = str(err, encoding='utf-8')
        remove_file(src_temp)
        remove_file(input_temp)
        remove_file(exe)
        return JsonResponse(ret)
    return JsonResponse({"msg": "failed"})
