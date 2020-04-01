import _judger
import os
import filecmp
from subprocess import Popen, PIPE
from apps.record.models import CompileSrcRecord, JudgeRecord
from apps.practice.models import Programme


RESULT_STR = [
    "ACCEPT",
    "CPU_TIME_LIMIT_EXCEEDED",
    "REAL_TIME_LIMIT_EXCEEDED",
    "MEMORY_LIMIT_EXCEEDED",
    "RUNTIME_ERROR",
    "SYSTEM_ERROR",
    "WRONG_ANSWER"
]
ERROR_STR = [
    "SUCCESS",
    "INVALID_CONFIG",
    "FORK_FAILED",
    "PTHREAD_FAILED",
    "WAIT_FAILE",
    "ROOT_REQUIRED",
    "LOAD_SECCOMP_FAILED",
    "SETRLIMIT_FAILED",
    "DUP2_FAILED",
    "SETUID_FAILED",
    "EXECVE_FAILED"
]
# _judger result
# RESULT_SUCCESS = 0
# RESULT_CPU_TIME_LIMIT_EXCEEDED = 1
# RESULT_REAL_TIME_LIMIT_EXCEEDED = 2
# RESULT_MEMORY_LIMIT_EXCEEDED = 3
# RESULT_RUNTIME_ERROR = 4
# RESULT_SYSTEM_ERROR = 5
# RESULT_WRONG_ANSWER = -1
# error
# SUCCESS = 0
# INVALID_CONFIG = -1
# FORK_FAILED = -2
# PTHREAD_FAILED = -3
# WAIT_FAILED = -4
# ROOT_REQUIRED = -5
# LOAD_SECCOMP_FAILED = -6
# SETRLIMIT_FAILED = -7
# DUP2_FAILED = -8
# SETUID_FAILED = -9
# EXECVE_FAILED = -10


class JudgerUtil:
    def __init__(self, commit_record_obj):
        self.commit_record_obj = commit_record_obj
        self.compile_record_obj = None

    def compile_c_src(self, c_src_file, exe_file):
        cmd = "gcc {0} -O2 -fmax-errors=3 -o {1}".format(c_src_file, exe_file)
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
                ext=str(rst, encoding='utf-8')
            )
            return True
        self.save_compile_record(
            commit_record=self.commit_record_obj,
            exe_path=exe_file,
            success=False,
            ext=str(err, encoding='utf-8')
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
        src_path = self.commit_record_obj.src_saved_path
        src_dir = os.path.dirname(src_path)
        exe_path = src_dir + os.path.sep + "main"
        if not self.compile_c_src(src_path, exe_path):
            rst = {}
            rst['result'] = "COMPILE_ERROR"
            self.save_judge_record(rst)
            return
        tc_count = self.get_testcase_count()
        tc_dir = self.get_testcase_dir()
        rst = []
        for i in range(tc_count):
            in_file = os.path.join(tc_dir, '%d.in' % i)
            out_file = os.path.join(tc_dir, '%d.out' % i)
            simple_rst = self.run_simple(exe_path, in_file, out_file)
            if simple_rst["error"] == 0:
                simple_rst['result'] = RESULT_STR[simple_rst['result']]
            else:
                simple_rst["error"] = ERROR_STR[simple_rst["error"]]
            rst.append(simple_rst)
        self.save_judge_record(rst)

    def run_simple(self, exe_path, in_path, out_path):
        work_dir = os.path.dirname(exe_path)
        temp_out = os.path.join(work_dir, "temp.out")
        error_out = os.path.join(work_dir, "error.out")
        rst = _judger.run(
            max_cpu_time=self.get_time_limit(),
            max_real_time=self.get_time_limit() * 10,
            max_memory=self.get_memory_limit() * 1024 * 1024,
            max_output_size=_judger.UNLIMITED,
            max_process_number=200,
            max_stack=32 * 1024 * 1024,
            exe_path=exe_path,
            input_path=in_path,
            output_path=temp_out,
            error_path=error_out,
            args=[],
            env=[],
            log_path="judge.log",
            seccomp_rule_name="c_cpp",
            uid=0,
            gid=0
        )
        if not filecmp.cmp(temp_out, out_path):
            rst["result"] = -1
        return rst

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

    def save_judge_record(self, rst):
        record = JudgeRecord(
            compile_record=self.compile_record_obj,
            result=rst
        )
        record.save()
