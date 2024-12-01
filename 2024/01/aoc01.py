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
    lists = [[], []]
    for line in input.strip().split("\n"):
        for i, n in enumerate(re.split(r" +", line)):
            lists[i].append(int(n))
    return lists


def find_similarity_scores_between_lists(lists):
    return [n * lists[1].count(n) for n in lists[0]]


def run_program(input):
    lists = parse_input(input)
    similarity_scores = find_similarity_scores_between_lists(lists)
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
