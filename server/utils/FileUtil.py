import pandas as pd
import json
import zipfile
import shutil
import os


def df_to_json(df):
    return json.loads(df.to_json(orient="records", force_ascii=False))


def handle_excel(excel_path, cols):
    dataframe = pd.read_excel(excel_path, sheet_name=0)
    dataframe.columns = cols
    return df_to_json(dataframe)


def handle_choice_excel(excel_path):
    data = handle_excel(excel_path,
                        ["title", "detail", "A", "B", "C", "D", "multichoice", "reference"]
                        )
    return data


def handle_user_excel(excel_path):
    data = handle_excel(excel_path,
                        ["account", "name"]
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
