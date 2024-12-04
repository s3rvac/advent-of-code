#
# Advent of Code 2024, day 04, part 1
#

import textwrap
import unittest


# All eight possible directions in which a word can appear.
PUZZLE_DIRECTIONS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split("\n")]


def get_coords_for_word_in_puzzle_on_position_in_direction(
    word, puzzle, i, j, dir_i, dir_j
):
    def is_inside_puzzle(i, j):
        return 0 <= i < len(puzzle) and 0 <= j < len(puzzle[i])

    coords = []
    for c in word:
        if not is_inside_puzzle(i, j) or puzzle[i][j] != c:
            return []
        coords.append((i, j))
        i += dir_i
        j += dir_j
    return coords


def get_coords_for_word_in_puzzle_on_position(word, puzzle, i, j):
    found_word_coords = []
    for dir_i, dir_j in PUZZLE_DIRECTIONS:
        if coords := get_coords_for_word_in_puzzle_on_position_in_direction(
            word, puzzle, i, j, dir_i, dir_j
        ):
            found_word_coords.append(coords)
    return found_word_coords


def get_word_count_in_puzzle(word, puzzle):
    # Use a set to exclude duplicate coordinates.
    found_word_coords = set()
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j] != word[0]:
                continue
            coords = get_coords_for_word_in_puzzle_on_position(word, puzzle, i, j)
            found_word_coords.update({tuple(sorted(coords)) for coords in coords})
    return len(found_word_coords)


def run_program(input):
    puzzle = parse_input(input)
    return get_word_count_in_puzzle(word="XMAS", puzzle=puzzle)


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

        self.assertEqual(result, 18)
