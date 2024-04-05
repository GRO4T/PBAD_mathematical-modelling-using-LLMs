import argparse
import enum
import os
import re
import subprocess

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


def get_all_problems_from_directory(directory: str) -> list[str]:
    return list(
        map(
            lambda x: PROBLEM_DIR + x,
            natsorted(filter(lambda x: "problem" in x, os.listdir(PROBLEM_DIR))),
        )
    )


def get_problems_from_file(problems_file: str) -> list[str]:
    problems = []
    with open(problems_file, "r", encoding="utf-8") as f:
        for problem in f.readlines():
            problems.append(problem.strip())
    return problems


MODE = 105
PROBLEM_DIR = "./datasets/model_building_in_mathematical_programming/"

parser = argparse.ArgumentParser(description="Execute benchmarks for problems.")
parser.add_argument(
    "--model",
    type=str,
    required=False,
    default="gpt-3.5-turbo",
    help="Name of the LLM to use.",
)
parser.add_argument(
    "--max_try",
    type=int,
    required=False,
    default=0,
    help="Maximum retry prompts to LLM.",
)
parser.add_argument(
    "--problem_list", type=str, required=False, help="File containing list of problems."
)
args = parser.parse_args()

results = []

with open("benchmark.log", "w", encoding="utf-8") as benchmark_log:
    if args.problem_list:
        problems = get_problems_from_file(args.problem_list)
    else:
        problems = get_all_problems_from_directory(PROBLEM_DIR)
    for problem_id, problem in enumerate(problems):
        cmd = f"python3 OptiMUS/gpt4or.py --model {args.model} --maxtry {args.max_try} --mode {MODE} --verbose True --prob {problem}"
        benchmark_log.write(f">>> {cmd}\n")
        benchmark_log.flush()
        print(f"Running OptiMUS for problem: {problem}")
        optimus_output = subprocess.check_output(
            cmd, stderr=subprocess.STDOUT, shell=True
        ).decode("utf-8")

        benchmark_log.write(optimus_output)
        benchmark_log.flush()

        result = check_result(optimus_output)
        print(result)
        results.append((problem, result))

print(results)
