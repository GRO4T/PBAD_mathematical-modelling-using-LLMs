import re
import os
import subprocess
import enum

from natsort import natsorted


class Result(enum.Enum):
    OK = 0
    SYNTAX_ERROR = 1
    LOGIC_ERROR = 2


def check_result(optimus_output: str) -> Result:
    status_ok_regex = r"Status: *\[0, [0-9]+\]"
    status_syntax_error_regex = r"Status: *\[1, [0-9]+\]"
    status_logic_error_regex = r"Status: *\[2, [0-9]+\]"

    if re.search(status_ok_regex, optimus_output):
        return Result.OK
    if re.search(status_syntax_error_regex, optimus_output):
        return Result.SYNTAX_ERROR
    if re.search(status_logic_error_regex, optimus_output):
        return Result.LOGIC_ERROR


MODEL = "gpt-3.5-turbo"
MAX_TRY = 1
MODE = 105
PROBLEM_DIR = "./datasets/introduction_to_linear_optimization/"

results = []

with open("benchmark.log", "w") as benchmark_log:
    for problem_id, problem in enumerate(natsorted(os.listdir(PROBLEM_DIR))):
        if problem_id > 5:
            break

        cmd = f"python3 OptiMUS/gpt4or.py --model {MODEL} --maxtry {MAX_TRY} --mode {MODE} --verbose True --prob {PROBLEM_DIR}{problem}"
        print(f"Running OptiMUS for problem: {PROBLEM_DIR}{problem}")
        optimus_output = subprocess.check_output(
            cmd, stderr=subprocess.STDOUT, shell=True
        ).decode("utf-8")

        benchmark_log.write(optimus_output)
        benchmark_log.flush()

        result = check_result(optimus_output)
        print(result)
        results.append((PROBLEM_DIR + problem, result))

print(results)
