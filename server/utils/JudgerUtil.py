import lorun
import os
from subprocess import Popen, PIPE
from apps.record.models import CompileSrcRecord, JudgeRecord


RESULT_STR = [
    'Accepted',
    'Presentation Error',
    'Time Limit Exceeded',
    'Memory Limit Exceeded',
    'Wrong Answer',
    'Runtime Error',
    'Output Limit Exceeded',
    'Compile Error',
    'System Error'
]


class JudgerUtil:
    def __init__(self, commit_record_obj):
        self.commit_record_obj = commit_record_obj
        self.compile_record_obj = None

    def compile_c_src(self, c_src_file, exe_file):
        cmd = "gcc -g {0} -o {1} -lseccomp".format(c_src_file, exe_file)
        compiling = Popen(
            cmd,
            shell=True,
            stdin=PIPE,
            stderr=PIPE,
            stdout=PIPE)
        # check result and add it into the CimpileRecord
        rst = compiling.stdout.read()
        err = compiling.stderr.read()
        if len(err) == 0:
            if len(rst) == 0:
                rst_str = "Success"
            else:
                rst_str = str(rst)
            self.save_compile_record(
                commit_record=self.commit_record_obj,
                exe_path=exe_file,
                result=rst_str
            )
            return True
        self.save_compile_record(
            commit_record=self.commit_record_obj,
            exe_path=exe_file,
            result=str(err)
        )
        return False

    def save_compile_record(self, commit_record, exe_path, result):
        record = CompileSrcRecord(
            commit_record=commit_record,
            exe_path=exe_path,
            result=result)
        record.save()
        self.commit_record_obj.status = "3"
        self.commit_record_obj.save()
        self.compile_record_obj = record

    def judge(self):
        pass

    def run_simple(self, exe_path, in_path, out_path):
        pass

    def save_judge_record():
        pass
