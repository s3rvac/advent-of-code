#
# Advent of Code 2023, day 14, part 1
#

import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split("\n")]


def tilt_platform_to_north(platform):
    # Iteratively move stones until the platform stops changing.
    platform_changed = True
    while platform_changed:
        platform_changed = False
        for i in range(len(platform)):
            for j in range(len(platform[i])):
                if i - 1 >= 0 and platform[i][j] == "O" and platform[i - 1][j] == ".":
                    platform[i][j] = "."
                    platform[i - 1][j] = "O"
                    platform_changed = True


def get_total_load_for_platform(platform):
    return sum(
        row.count("O") * load_per_rock
        for row, load_per_rock in zip(platform, range(len(platform), 0, -1))
    )


def run_program(input):
    platform = parse_input(input)
    tilt_platform_to_north(platform)
    return get_total_load_for_platform(platform)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            O....#....
            O.OO#....#
            .....##...
            OO.#O....O
            .O.....O#.
            O.#..O.#.#
            ..O..#O..O
            .......O..
            #....###..
            #OO..#....
            """
        )

        result = run_program(input)

        self.assertEqual(result, 136)
