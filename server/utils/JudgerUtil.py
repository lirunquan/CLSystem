import lorun
import os
from subprocess import Popen, PIPE
from apps.record.models import CompileSrcRecord, JudgeRecord
from apps.oj.models import Programme


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
        p_type = self.get_problem_type()
        if p_type == "1":
            src_path = self.commit_record_obj.src_saved_path
            src_dir = os.path.dirname(src_path)
            exe_path = src_dir + os.path.sep + "main"
            if not self.compile_c_src(src_path, exe_path):
                return

    def run_simple(self, exe_path, in_path, out_path):
        work_dir = os.path.dirname(exe_path)
        with open(work_dir + "/temp.out", "w") as ftemp:
            with open(in_path, "r") as fin:
                run_config = {
                    'args': ['./' + str(exe_path)],
                    "fd_in": fin.fileno(),
                    "fd_out": ftemp.fileno(),
                    "timelimit": self.get_time_limit(),
                    "memorylimit": self.get_memory_limit()
                }
                rst = lorun.run(run_config)
                if rst["result"] == 0:
                    with open(out_path) as fout:
                        check_rst = lorun.check(fout.fileno(), ftemp.fileno())
                        os.remove(work_dir + "/temp.out")
                        if check_rst != 0:
                            return {"result": check_rst}
                return rst

    def get_problem_type(self):
        return self.commit_record_obj.problem_type

    def get_programme(self):
        p_id = self.commit_record_obj.problem_id
        programme = Programme.objects.filter(id=p_id)
        if len(programme) == 1:
            return programme[0]
        return None

    def get_time_limit(self):
        programme = self.get_programme()
        if programme:
            return programme.time_limit
        return 1000

    def get_memory_limit(self):
        programme = self.get_programme()
        if programme:
            return programme.memory_limit
        return 20000

    def get_testcase_count(self):
        programme = self.get_programme()
        if programme:
            return programme.testcase_count
        return 0

    def get_testcase_path(self):
        programme = self.get_programme()
        if programme:
            return programme.testcase_path
        return ""

    def save_judge_record(self, tc_count, tc_path, rst):
        record = JudgeRecord(
            compile_record=self.compile_record_obj,
            testcase_count=tc_count,
            testcase_path=tc_path,
            result=rst
        )
        record.save()
