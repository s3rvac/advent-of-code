#
# Advent of Code 2023, day 13, part 1
#

import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [pattern.split("\n") for pattern in input.strip().split("\n\n")]


def evaluate_pattern(pattern):
    # Horizontal reflection.
    if count := evaluate_pattern_horizontally(pattern):
        return count * 100

    # Vertical reflection. Can be computed by using the horizontal algorithm
    # over a transposed pattern.
    transposed_pattern = transpose_pattern(pattern)
    return evaluate_pattern_horizontally(transposed_pattern)


def transpose_pattern(pattern):
    # https://en.wikipedia.org/wiki/Transpose
    return ["".join(row) for row in zip(*pattern)]


def evaluate_pattern_horizontally(pattern):
    # Try to do the split after every row and check whether it is possible to
    # find a reflection.
    def can_be_split_after_row(i):
        return all(
            row1 == row2
            for row1, row2 in zip(reversed(pattern[: i + 1]), pattern[i + 1 :])
        )

    for i in range(len(pattern) - 1):
        if can_be_split_after_row(i):
            return i + 1

    return 0


def run_program(input):
    patterns = parse_input(input)
    return sum(map(evaluate_pattern, patterns))


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            #.##..##.
            ..#.##.#.
            ##......#
            ##......#
            ..#.##.#.
            ..##..##.
            #.#.##.#.

            #...##..#
            #....#..#
            ..##..###
            #####.##.
            #####.##.
            ..##..###
            #....#..#
            """
        )

        result = run_program(input)

        self.assertEqual(result, 405)
