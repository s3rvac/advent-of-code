#
# Advent of Code 2024, day 12, part 1
#

import textwrap
import unittest


NEIGHBOR_DIRECTIONS = [(0, 1), (0, -1), (-1, 0), (1, 0)]


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split("\n")]


def compute_region_perimeter(region):
    perimeter = 0
    for i, j in region:
        for ix, jx in NEIGHBOR_DIRECTIONS:
            if (i + ix, j + jx) not in region:
                perimeter += 1
    return perimeter


def compute_price_for_region(region):
    region_area = len(region)
    return region_area * compute_region_perimeter(region)


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

        self.assertEqual(result, 140)

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

        self.assertEqual(result, 772)

    def test_program_returns_correct_result_for_example_input3(self):
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

        self.assertEqual(result, 1930)
