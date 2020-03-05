import _judger
import os
from subprocess import Popen, PIPE
from apps.record.models import CompileSrcRecord, JudgeRecord
from apps.oj.models import Programme, Choice


RESULT_STR = [
    "ACCEPT",
    "CPU_TIME_LIMIT_EXCEEDED",
    "REAL_TIME_LIMIT_EXCEEDED",
    "MEMORY_LIMIT_EXCEEDED",
    "RUNTIME_ERROR",
    "SYSTEM_ERROR",
    "WRONG_ANSWER"
]
# _judger
# RESULT_SUCCESS = 0
# RESULT_CPU_TIME_LIMIT_EXCEEDED = 1
# RESULT_REAL_TIME_LIMIT_EXCEEDED = 2
# RESULT_MEMORY_LIMIT_EXCEEDED = 3
# RESULT_RUNTIME_ERROR = 4
# RESULT_SYSTEM_ERROR = 5
# RESULT_WRONG_ANSWER = -1


class JudgerUtil:
    def __init__(self, commit_record_obj):
        self.commit_record_obj = commit_record_obj
        self.compile_record_obj = None

    def compile_c_src(self, c_src_file, exe_file):
        cmd = "gcc {0} -o {1}".format(c_src_file, exe_file)
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
            self.save_compile_record(
                commit_record=self.commit_record_obj,
                exe_path=exe_file,
                success=True,
                ext=str(rst)
            )
            return True
        self.save_compile_record(
            commit_record=self.commit_record_obj,
            exe_path=exe_file,
            success=False,
            ext=str(err)
        )
        return False

    def save_compile_record(self, commit_record, exe_path, success, ext):
        record = CompileSrcRecord(
            commit_record=commit_record,
            exe_path=exe_path,
            success=success,
            ext=ext
        )
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
        rst = _judger.run(
            max_cpu_time=self.get_time_limit(),
            max_real_time=self.get_time_limit() * 10,
            max_memory=self.get_memory_limit() * 1024 * 1024,
            max_output_size=_judger.UNLIMITED,
            max_process_number=200,
            max_stack=32 * 1024 * 1024,
            exe_path=exe_path,
            input_path=in_path,
            output_path=out_path,
            error_path=out_path,
            args=[],
            env=[],
            log_path="judge.log",
            seccomp_rule_name="c_cpp",
            uid=0,
            gid=0
        )
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
        return 256

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
