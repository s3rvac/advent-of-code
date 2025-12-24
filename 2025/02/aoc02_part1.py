#
# Advent of Code 2025, day 02, part 1
#

import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [tuple(map(int, r.split("-"))) for r in input.strip().split(",")]


def gen_invalid_ids(ranges):
    # An invalid ID is made only of a sequence of digits repeated twice.
    def is_invalid_id(id):
        p1, p2 = split_in_two(str(id))
        return p1 == p2

    for min, max in ranges:
        for id in range(min, max + 1):
            if is_invalid_id(id):
                yield id


def split_in_two(s):
    return s[: len(s) // 2], s[len(s) // 2 :]


def run_program(input):
    ranges = parse_input(input)
    invalid_ids = gen_invalid_ids(ranges)
    return sum(invalid_ids)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
            """
        )

        result = run_program(input)

        self.assertEqual(result, 1227775554)
