#
# Advent of Code 2024, day 02, part 2
#

import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [[int(n) for n in line.split(" ")] for line in input.strip().split("\n")]


def is_report_safe_in_order(report, increasing):
    for m, n in zip(report, report[1:]):
        if increasing and m <= n:
            return False
        elif not increasing and m >= n:
            return False
        elif abs(m - n) not in (1, 2, 3):
            return False
    return True


def is_report_safe_in_any_order(report):
    return (
        is_report_safe_in_order(report, increasing=True) or
        is_report_safe_in_order(report, increasing=False)
    )


def is_report_safe(report):
    # First, check if the report is safe as-is.
    if is_report_safe_in_any_order(report):
        return True

    # Second, try removing a level from the report and check if the report is
    # then safe. Try all possible levels.
    for i in range(len(report)):
        if is_report_safe_in_any_order(report[0:i] + report[i + 1:]):
            return True

    return False


def run_program(input):
    reports = parse_input(input)
    return sum(1 if is_report_safe(report) else 0 for report in reports)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            7 6 4 2 1
            1 2 7 8 9
            9 7 6 2 1
            1 3 2 4 5
            8 6 4 4 1
            1 3 6 7 9
            """
        )

        result = run_program(input)

        self.assertEqual(result, 4)
