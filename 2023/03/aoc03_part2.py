#
# Advent of Code 2023, day 03, part 2
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


def get_gear_ratios_in_engine(engine):
    gear_ratios = []
    for i in range(len(engine)):
        for j in range(len(engine[i])):
            if engine[i][j] == "*":
                part_numbers = get_part_numbers_adjacent_to_position(engine, i, j)
                if len(part_numbers) == 2:
                    gear_ratios.append(part_numbers[0] * part_numbers[1])
    return gear_ratios


def get_part_numbers_adjacent_to_position(engine, i, j):
    part_numbers = set()
    for ix, jx in ADJACENT_DIRECTIONS:
        if engine[i + ix][j + jx].isdigit():
            part_numbers.add(get_number_on_position(engine, i + ix, j + jx))
    return list(part_numbers)


def get_number_on_position(engine, i, j):
    while engine[i][j].isdigit():
        j -= 1

    m = re.match(r"^(\d+)", engine[i][j + 1 :])
    assert m is not None
    return int(m.group(1))


def run_program(input):
    engine = parse_input(input)
    return sum(get_gear_ratios_in_engine(engine))


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

        self.assertEqual(result, 467835)
