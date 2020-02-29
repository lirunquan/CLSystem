from .models import Programme, Choice
from utils.FileUtil import write_file, handle_choice_excel


def add_choice(t: str, d: str, op: dict, mc: bool, ref: str):
    choice = Choice(
        title=t,
        detail=d,
        options=op,
        multichoice=mc,
        reference=ref
    )
    choice.save()


def import_choice_from_excel(file_data, file_path):
    write_file(file_data, file_path)
    choices_list = handle_choice_excel(file_path)
    for c in choices_list:
        options = {
            "A": c["A"],
            "B": c["B"],
            "C": c["C"],
            "D": c["D"]
        }
        add_choice(
            c["title"],
            c["detail"],
            options,
            c["multichoice"],
            c["reference"]
        )


def add_programme():
    pass
