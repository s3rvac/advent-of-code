#
# Advent of Code 2024, day 08, part 1
#

import collections
import dataclasses
import itertools
import math
import textwrap
import unittest


@dataclasses.dataclass
class Map:
    antennas_per_frequency: dict
    width: int
    height: int

    def antenna_combinations_for_frequency(self, frequency):
        return itertools.combinations(self.antennas_per_frequency[frequency], 2)

    def all_points_except(self, x1, y1, x2, y2):
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) not in ((x1, y1), (x2, y2)):
                    yield x, y


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    lines = input.strip().split("\n")
    map = Map(
        collections.defaultdict(list),
        width=len(lines),
        height=len(lines[0]),
    )
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c != ".":
                map.antennas_per_frequency[c].append((i, j))
    return map


def points_are_on_same_line(x1, y1, x2, y2, x3, y3):
    # Returns true if points 1, 2, and 3 are on the same line (i.e. are
    # collinear). We do this by checking that the slope between point 1 and
    # point 2 matches the one of point 1 and point 3.
    return (y1 - y2) * (x1 - x3) == (y1 - y3) * (x1 - x2)


def distance(x1, y1, x2, y2):
    # Returns the distance between points 1 and 2.
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))


def points_have_same_distance(x1, y1, x2, y2, x3, y3):
    # Returns true if the distance between points 1 and 2 is the same as either
    # the distance between 1 and 3 or 2 and 3.
    dst_1_2 = distance(x1, y1, x2, y2)
    dst_1_3 = distance(x1, y1, x3, y3)
    dst_2_3 = distance(x2, y2, x3, y3)
    return math.isclose(dst_1_2, dst_1_3) or math.isclose(dst_1_2, dst_2_3)


def count_antinodes(map):
    antinodes = set()
    for frequency in map.antennas_per_frequency:
        for (x1, y1), (x2, y2) in map.antenna_combinations_for_frequency(frequency):
            for x3, y3 in map.all_points_except(x1, y1, x2, y2):
                if points_are_on_same_line(x1, y1, x2, y2, x3, y3):
                    if points_have_same_distance(x1, y1, x2, y2, x3, y3):
                        antinodes.add((x3, y3))
    return len(antinodes)


def run_program(input):
    map = parse_input(input)
    return count_antinodes(map)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            ............
            ........0...
            .....0......
            .......0....
            ....0.......
            ......A.....
            ............
            ............
            ........A...
            .........A..
            ............
            ............
            """
        )

        result = run_program(input)

        self.assertEqual(result, 14)