import pandas as pd
import json


def df_to_json(df):
    return json.loads(df.to_json(orient="records", force_ascii=False))


def handle_batch_choice_excel(excel_path):
    dataframe = pd.read_excel(excel_path, sheet_name=0)
    dataframe.columns = ["title", "detail", "A", "B", "C", "D", "multichoice", "reference"]
    return df_to_json(dataframe)
