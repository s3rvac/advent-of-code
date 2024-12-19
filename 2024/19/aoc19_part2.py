#
# Advent of Code 2024, day 19, part 2
#

import functools
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    raw_stripes, raw_designs = input.strip().split("\n\n")
    return raw_stripes.split(", "), raw_designs.split("\n")


def count_possible_design_combinations(design, stripes):
    usable_stripes = [stripe for stripe in stripes if stripe in design]

    @functools.cache
    def count_possible_combinations(d):
        if not d:
            return 1

        count = 0
        for stripe in usable_stripes:
            if d.startswith(stripe):
                count += count_possible_combinations(d.replace(stripe, "", 1))

        return count

    return count_possible_combinations(design)


def count_possible_designs_combinations(designs, stripes):
    return sum(
        count_possible_design_combinations(design, stripes) for design in designs
    )


def run_program(input):
    stripes, designs = parse_input(input)
    return count_possible_designs_combinations(designs, stripes)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            r, wr, b, g, bwu, rb, gb, br

            brwrr
            bggr
            gbbr
            rrbgbr
            ubwu
            bwurrg
            brgr
            bbrgwb
            """
        )

        result = run_program(input)

        self.assertEqual(result, 16)
