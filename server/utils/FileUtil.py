import pandas as pd
import json
import zipfile
import shutil
import os
from subprocess import Popen, PIPE
from django.http import FileResponse


def df_to_json(df):
    return json.loads(df.to_json(orient="records", force_ascii=False))


def handle_excel(excel_path, cols):
    dataframe = pd.read_excel(excel_path, sheet_name=0)
    dataframe.columns = cols
    return df_to_json(dataframe)


def handle_choice_excel(excel_path):
    data = handle_excel(
        excel_path,
        ["title", "detail", "A", "B", "C", "D", "multichoice", "reference"]
    )
    return data


def handle_class_excel(excel_path):
    data = handle_excel(excel_path,
                        ["year", "major", "number"]
                        )
    return data


def handle_teacher_excel(excel_path):
    data = handle_excel(excel_path,
                        ["account", "name"]
                        )
    return data


def handle_student_excel(excel_path):
    data = handle_excel(excel_path,
                        ["year", "major", "number", "account", "name"]
                        )
    return data


def write_file(data, path):
    with open(path, 'wb') as f:
        for i in data.chunks():
            f.write(i)


def write_str_file(string, path):
    with open(path, 'w') as f:
        f.write(string)


def unzip_file(zip_file, unzip_dir):
    fz = zipfile.ZipFile(zip_file, 'r')
    fz.extractall(unzip_dir)


def make_dir(dir_name):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
        os.mkdir(dir_name)
    else:
        os.mkdir(dir_name)


def remove_file(filename):
    os.remove(filename)


def make_zip(src_dir, out_zip):
    zf = zipfile.ZipFile(out_zip, "w", zipfile.zlib.DEFLATED)
    for file in os.listdir(src_dir):
        filepath = os.path.join(src_dir, file)
        zf.write(filepath, file)
    zf.close()


def dos2unix(path):
    cmd = "dos2unix -o -k " + path
    run = Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE)
    print(run.stderr.read())


def dos2unix_dir(dir_name):
    for p in os.listdir(dir_name):
        dos2unix(os.path.join(dir_name, p))


def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
    with open(file_name, 'rb') as f:
        f.seek(offset, os.SEEK_SET)
        remain = length
        while True:
            len_bytes = chunk_size if remain is None else min(remain, chunk_size)
            file_data = f.read(len_bytes)
            if not file_data:
                break
            if remain:
                remain -= len(file_data)
            yield file_data


def download_response(path):
    f = open(path, 'rb')
    resp = FileResponse(f)
    resp["Content-Type"] = "application/octet-stream"
    filename = path.split(os.path.sep)[-1]
    disp = 'attachment;filename="' + filename + '"'
    resp["Content-Disposition"] = disp
    return resp
