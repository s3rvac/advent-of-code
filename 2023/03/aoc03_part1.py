#
# Advent of Code 2023, day 03, part 1
#

import re
import textwrap
import unittest


ADJACENT_DIRECTIONS = [
    (-1, -1),
    (-1, 0),
    (-1, +1),
    (0, -1),
    (0, +1),
    (+1, -1),
    (+1, 0),
    (+1, +1),
]


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return list(input.strip().split("\n"))


def get_part_numbers(engine):
    part_numbers = []
    for i in range(len(engine)):
        for j in range(len(engine[i])):
            if engine[i][j] not in ".1234567890":
                part_numbers.extend(get_part_numbers_adjacent_to_position(engine, i, j))
    return part_numbers


def get_part_numbers_adjacent_to_position(engine, i, j):
    part_numbers = set()
    for ix, jx in ADJACENT_DIRECTIONS:
        if engine[i + ix][j + jx].isdigit():
            part_numbers.add(get_number_on_position(engine, i + ix, j + jx))
    return part_numbers


def get_number_on_position(engine, i, j):
    while engine[i][j].isdigit():
        j -= 1

    m = re.match(r"^(\d+)", engine[i][j + 1 :])
    assert m is not None
    return int(m.group(1))


def run_program(input):
    engine = parse_input(input)
    return sum(get_part_numbers(engine))


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            467..114..
            ...*......
            ..35..633.
            ......#...
            617*......
            .....+.58.
            ..592.....
            ......755.
            ...$.*....
            .664.598..
            """
        )

        result = run_program(input)

        self.assertEqual(result, 4361)
