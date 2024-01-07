#
# Advent of Code 2023, day 13
#

import textwrap
import unittest


def read_input():
    with open('input.txt', encoding='utf-8') as f:
        return f.read()


def parse_input(input):
    return [pattern.split('\n') for pattern in input.strip().split('\n\n')]


def summarize_patterns(patterns):
    return sum(fix_smudge_and_evaluate_pattern(pattern) for pattern in patterns)


def fix_smudge_and_evaluate_pattern(pattern):
    # Horizontal reflection.
    if count := fix_smudge_and_evaluate_pattern_horizontally(pattern):
        return count * 100

    # Vertical reflection. Can be computed by using the horizontal algorithm
    # over a transposed pattern.
    transposed_pattern = transpose_pattern(pattern)
    return fix_smudge_and_evaluate_pattern_horizontally(transposed_pattern)


def transpose_pattern(pattern):
    # https://en.wikipedia.org/wiki/Transpose
    return [''.join(row) for row in zip(*pattern)]


def fix_smudge_and_evaluate_pattern_horizontally(pattern):
    # The gist behind the implementation is that we try to do the split after
    # every row and check whether it is possible to find a reflection while
    # fixing a single smudge.
    def can_be_split_after_row_while_fixing_smudge(i):
        smudge_fixed = False
        for row1, row2 in zip(reversed(pattern[: i + 1]), pattern[i + 1 :]):
            if row1 == row2:
                continue
            elif not smudge_fixed and hamming_distance(row1, row2) == 1:
                smudge_fixed = True
            else:
                return False

        return smudge_fixed

    for i in range(len(pattern) - 1):
        if can_be_split_after_row_while_fixing_smudge(i):
            return i + 1

    return None


def hamming_distance(s1, s2):
    # The Hamming distance between two equally long strings is the number of
    # positions at which the corresponding characters are different
    # (https://en.wikipedia.org/wiki/Hamming_distance).
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def run_program(input):
    patterns = parse_input(input)
    return summarize_patterns(patterns)


if __name__ == '__main__':
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

        self.assertEqual(result, 400)
