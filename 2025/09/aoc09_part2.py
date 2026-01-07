#
# Advent of Code 2025, day 09, part 2
#
# Requirements:
#
#     pip install shapely==2.1.2
#

import itertools
import textwrap
import unittest

import shapely


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [tuple(map(int, line.split(","))) for line in input.strip().split()]


def get_area_of_largest_rectangle(red_tiles):
    # Simplify the computation by utilizing the `shapely` package, creating a
    # polygon from the red tiles (= corners of the polygon), and then computing
    # the maximal area of a rectangle that fits within the red-tile-given
    # polygon whilst trying all red tile pairs.
    whole_area = shapely.Polygon(red_tiles)

    def compute_area(c1, c2):
        length = abs(c1[0] - c2[0]) + 1
        width = abs(c1[1] - c2[1]) + 1
        return length * width

    def is_rectangle_formed_only_by_green_or_red_tiles(c1, c2):
        rectangle = shapely.Polygon(
            [
                c1,
                (c1[0], c2[1]),
                c2,
                (c2[0], c1[1]),
            ]
        )
        return shapely.within(rectangle, whole_area)

    return max(
        compute_area(c1, c2)
        for c1, c2 in itertools.combinations(red_tiles, 2)
        if is_rectangle_formed_only_by_green_or_red_tiles(c1, c2)
    )


def run_program(input):
    red_tiles = parse_input(input)
    return get_area_of_largest_rectangle(red_tiles)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            7,1
            11,1
            11,7
            9,7
            9,5
            2,5
            2,3
            7,3
            """
        )

        result = run_program(input)

        self.assertEqual(result, 24)
