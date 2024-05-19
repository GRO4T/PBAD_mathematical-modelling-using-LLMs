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
    BENCHMARK_ERROR = 3


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
            lambda x: directory + x,
            natsorted(filter(lambda x: "problem" in x, os.listdir(directory))),
        )
    )


def get_problems_from_file(problems_file: str) -> list[str]:
    problems = []
    with open(problems_file, "r", encoding="utf-8") as f:
        for problem in f.readlines():
            problems.append(problem.strip())
    return problems


def get_problem_type(problem: str) -> str:
    with open(os.path.join(problem, "description.txt"), "r") as description_file:
        description_content = description_file.read()

    problem_type_pattern = r"PROBLEM TYPE: (LP or MILP|LP|MIP|MILP)"
    problem_type_match = re.search(problem_type_pattern, description_content)

    if not problem_type_match:
        raise Exception("Problem type not found in description.txt")

    return problem_type_match.group(1).strip()


MODE = 104
PROBLEM_DIRS = [
    "./datasets/introduction_to_linear_optimization/",
    "./datasets/lectures_in_lp_modeling/",
    "./datasets/model_building_in_mathematical_programming/",
]

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
    default=2,
    help="Maximum retry prompts to LLM.",
)
parser.add_argument(
    "--problem_list", type=str, required=False, help="File containing list of problems."
)
parser.add_argument(
    "--solver", type=str, required=False, help="Solver to use", default="gurobi"
)
args = parser.parse_args()

results = []

with open("benchmark.log", "w", encoding="utf-8") as benchmark_log:
    if args.problem_list:
        problems = get_problems_from_file(args.problem_list)
    else:
        problems = []
        for problem_dir in PROBLEM_DIRS:
            problems.extend(get_all_problems_from_directory(problem_dir))

    for problem_id, problem in enumerate(problems):
        cmd = f"python3 OptiMUS/gpt4or.py --model {args.model} --solver {args.solver} --maxtry {args.max_try} --mode {MODE} --verbose True --prob {problem}"
        benchmark_log.write(f">>> {cmd}\n")
        benchmark_log.flush()
        print(f"Running OptiMUS for problem: {problem}")
        try:
            optimus_output = subprocess.check_output(
                cmd, stderr=subprocess.STDOUT, shell=True
            ).decode("utf-8")
        except subprocess.CalledProcessError as e:
            print(f"Error running OptiMUS for problem {problem}: {e}")
            results.append((problem, Result.BENCHMARK_ERROR))
            continue

        benchmark_log.write(optimus_output)
        benchmark_log.flush()

        result = check_result(optimus_output)
        problem_type = get_problem_type(problem)
        print(f"{problem_type} {result}")
        results.append((problem, result))

print(results)
