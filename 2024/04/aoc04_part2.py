#
# Advent of Code 2024, day 04, part 2
#

import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split("\n")]


def contains_x_mas_on_position(puzzle, i, j):
    if puzzle[i][j] != "A":
        return False
    elif i == 0 or j == 0 or i == (len(puzzle) - 1) or (j == len(puzzle[i]) - 1):
        return False
    elif {puzzle[i - 1][j - 1], puzzle[i + 1][j + 1]} != {"M", "S"}:
        return False
    elif {puzzle[i + 1][j - 1], puzzle[i - 1][j + 1]} != {"M", "S"}:
        return False
    return True


def get_x_mas_count_in_puzzle(puzzle):
    count = 0
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if contains_x_mas_on_position(puzzle, i, j):
                count += 1
    return count


def run_program(input):
    puzzle = parse_input(input)
    return get_x_mas_count_in_puzzle(puzzle)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            MMMSXXMASM
            MSAMXMSMSA
            AMXSXMAAMM
            MSAMASMSMX
            XMASAMXAMM
            XXAMMXXAMA
            SMSMSASXSS
            SAXAMASAAA
            MAMMMXMMMM
            MXMXAXMASX
            """
        )

        result = run_program(input)

        self.assertEqual(result, 9)
