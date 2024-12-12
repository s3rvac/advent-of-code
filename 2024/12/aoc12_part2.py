#
# Advent of Code 2024, day 12, part 2
#

import textwrap
import unittest


NEIGHBOR_DIRECTIONS = [(0, 1), (0, -1), (-1, 0), (1, 0)]


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split("\n")]


def compute_side_count_in_region(region):
    # Instead of computing the number of sides directly, we compute the number
    # of corners in the region, which is the same as the number of sides.
    #
    # In the diagram below, `#` denotes the current plot, `N` denotes a
    # neighbor, and `C` denotes a corner.
    corner_count = 0
    for i, j in region:
        # Introduce a few abbreviations for the presence of neighbors to make
        # the code clearer.
        #
        # T = top, R = right, B = bottom, L = left
        T = (i - 1, j) in region
        R = (i, j + 1) in region
        B = (i + 1, j) in region
        L = (i, j - 1) in region
        # TR = top right, BR = bottom right, BL = bottom left, TL = top left
        TR = (i - 1, j + 1) in region
        BR = (i + 1, j + 1) in region
        BL = (i + 1, j - 1) in region
        TL = (i - 1, j - 1) in region

        # No neighbors -> 4 corners:
        #
        #  C C
        #   #
        #  C C
        #
        if not T and not R and not B and not L:
            corner_count += 4

        # One neighbor -> 2 corners:
        #
        #   N   C    C C    C
        #   #    #N   #   N#
        #  C C  C     N     C
        #
        if T and not R and not B and not L:
            corner_count += 2
        if R and not B and not L and not T:
            corner_count += 2
        if B and not L and not T and not R:
            corner_count += 2
        if L and not T and not R and not B:
            corner_count += 2

        # Two neighbors, 1 "outer" corner:
        #
        #  C      C   N    N
        #   #N  N#    #N  N#
        #   N    N   C      C
        #
        if B and R and not T and not L:
            corner_count += 1
        if B and L and not T and not R:
            corner_count += 1
        if T and R and not B and not L:
            corner_count += 1
        if T and L and not B and not R:
            corner_count += 1

        # Two neighbors, 1 "inner" corner:
        #
        #  NC      CN
        #  #N  #N  N#  N#
        #      NC      CN
        #
        if R and T and not TR:
            corner_count += 1
        if R and B and not BR:
            corner_count += 1
        if L and T and not TL:
            corner_count += 1
        if L and B and not BL:
            corner_count += 1
    return corner_count


def compute_price_for_region(region):
    region_area = len(region)
    return region_area * compute_side_count_in_region(region)


def is_plot_inside_garden(i, j, garden):
    return 0 <= i < len(garden) and 0 <= j < len(garden[i])


def get_region_for_plot(i, j, garden):
    # Use depth-first search to get all the regions for the given plot.
    # Breadth-first search would work as well.
    region = {(i, j)}
    to_visit = [(i, j)]
    while to_visit:
        i, j = to_visit.pop()
        for ix, jx in NEIGHBOR_DIRECTIONS:
            new_i, new_j = i + ix, j + jx
            if (
                is_plot_inside_garden(new_i, new_j, garden)
                and garden[i][j] == garden[new_i][new_j]
                and (new_i, new_j) not in region
            ):
                region.add((new_i, new_j))
                to_visit.append((new_i, new_j))
    return region


def split_garden_into_regions(garden):
    regions = []
    checked_plots = set()
    for i in range(len(garden)):
        for j in range(len(garden[i])):
            if (i, j) not in checked_plots:
                region = get_region_for_plot(i, j, garden)
                regions.append(region)
                checked_plots |= region
    return regions


def run_program(input):
    garden = parse_input(input)
    regions = split_garden_into_regions(garden)
    return sum(map(compute_price_for_region, regions))


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input1(self):
        input = textwrap.dedent(
            """
            AAAA
            BBCD
            BBCC
            EEEC
            """
        )

        result = run_program(input)

        self.assertEqual(result, 80)

    def test_program_returns_correct_result_for_example_input2(self):
        input = textwrap.dedent(
            """
            OOOOO
            OXOXO
            OOOOO
            OXOXO
            OOOOO
            """
        )

        result = run_program(input)

        self.assertEqual(result, 436)

    def test_program_returns_correct_result_for_example_input3(self):
        input = textwrap.dedent(
            """
            EEEEE
            EXXXX
            EEEEE
            EXXXX
            EEEEE
            """
        )

        result = run_program(input)

        self.assertEqual(result, 236)

    def test_program_returns_correct_result_for_example_input4(self):
        input = textwrap.dedent(
            """
            AAAAAA
            AAABBA
            AAABBA
            ABBAAA
            ABBAAA
            AAAAAA
            """
        )

        result = run_program(input)

        self.assertEqual(result, 368)

    def test_program_returns_correct_result_for_example_input5(self):
        input = textwrap.dedent(
            """
            RRRRIICCFF
            RRRRIICCCF
            VVRRRCCFFF
            VVRCCCJFFF
            VVVVCJJCFE
            VVIVCCJJEE
            VVIIICJJEE
            MIIIIIJJEE
            MIIISIJEEE
            MMMISSJEEE
            """
        )

        result = run_program(input)

        self.assertEqual(result, 1206)
