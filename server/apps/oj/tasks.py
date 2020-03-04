from .models import Programme, Choice
from utils.FileUtil import *
from server.settings import RESOURCES_DIR
from utils.JudgerUtil import JudgerUtil
from apps.record.models import CommitCodeRecord, CommitChoiceRecord
import os
import time


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
            t=c["title"],
            d=c["detail"],
            op=options,
            mc=c["multichoice"] == 'Y',
            ref=c["reference"]
        )


def add_programme(t, d, in_desc, out_desc, in_demo, out_demo, tc_count, tc_dir, tl, ml):
    p = Programme(
        title=t,
        detail=d,
        input_desc=in_desc,
        output_desc=out_desc,
        input_demo=in_demo,
        output_demo=out_demo,
        time_limit=tl,
        memory_limit=ml,
        testcase_count=tc_count,
        testcase_dir=tc_dir
    )
    p.save()
    make_dir(os.path.join(RESOURCES_DIR, 'programme', 'commit', str(p.id)))


def save_tc_file(file_data, tc_dir):
    saved_path = os.path.join(RESOURCES_DIR,
                              'programme',
                              str(time.time()).replace('.', '') + '.zip'
                              )
    write_file(file_data, saved_path)
    make_dir(tc_dir)
    unzip_file(saved_path, tc_dir)


def programme_commit(account, p_id, code):
    commit_dir = os.path.join(RESOURCES_DIR, 'programme', 'commit', str(p_id), str(account))
    make_dir(commit_dir)
    c_src = os.path.join(commit_dir, str(time.time()).replace('.', '') + '.c')
    write_str_file(code, c_src)
    times = len(
        CommitCodeRecord.objects.filter(account=account, problem_id=p_id)
    ) + 1
    record = CommitCodeRecord(
        problem_id=p_id,
        commit_times=times,
        account=str(account),
        identity='2',
        src_content=code,
        src_saved_path=c_src
    )
    record.save()
    judger = JudgerUtil(record)
    judger.judge()


def choice_commit(account, c_id, answer):
    pass
