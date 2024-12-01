#
# Advent of Code 2024, day 01
#

import re
import textwrap
import unittest


def read_input():
    with open("input.txt", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    left_list, right_list = [], []
    for line in input.strip().split("\n"):
        l, r = re.split(r" +", line)
        left_list.append(int(l))
        right_list.append(int(r))
    return left_list, right_list


def find_similarity_scores_between_lists(left_list, right_list):
    return [n * right_list.count(n) for n in left_list]


def run_program(input):
    left_list, right_list = parse_input(input)
    similarity_scores = find_similarity_scores_between_lists(left_list, right_list)
    return sum(similarity_scores)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            3   4
            4   3
            2   5
            1   3
            3   9
            3   3
            """
        )

        result = run_program(input)

        self.assertEqual(result, 31)
