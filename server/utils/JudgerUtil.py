import lorun
import os
from subprocess import Popen, PIPE
from apps.record.models import CompileSrcRecord, JudgeRecord
from apps.oj.models import Programme, Choice


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
        self.compile_record_obj = record

    def judge(self):
        p_type = self.get_problem_type()
        if p_type == "1":
            src_path = self.commit_record_obj.src_saved_path
            src_dir = os.path.dirname(src_path)
            exe_path = src_dir + os.path.sep + "main"
            if not self.compile_c_src(src_path, exe_path):
                rst = {}
                rst['result'] = RESULT_STR[7]
                self.save_judge_record(rst)
                return
            tc_count = self.get_testcase_count()
            tc_dir = self.get_testcase_dir()
            rst = []
            for i in range(tc_count):
                in_file = os.path.join(tc_dir, '%d.in' % i)
                out_file = os.path.join(tc_dir, '%d.out' % i)
                simple_rst = self.run_simple(exe_path, in_file, out_file)
                simple_rst['result'] = RESULT_STR[simple_rst['result']]
                rst.append(simple_rst)
            self.save_judge_record(rst)

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

    def get_choice(self):
        p_id = self.commit_record_obj.problem_id
        choice = Choice.objects.filter(id=p_id)
        if len(choice) == 1:
            return choice[0]
        return None

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

    def get_testcase_dir(self):
        programme = self.get_programme()
        if programme:
            return programme.testcase_dir
        return ""

    def get_choice_answer(self):
        return self.commit_record_obj.answer

    def get_reference(self):
        choice = self.get_choice()
        if choice:
            return choice.reference

    def save_judge_record(self, rst):
        record = JudgeRecord(
            compile_record=self.compile_record_obj,
            result=rst
        )
        record.save()
