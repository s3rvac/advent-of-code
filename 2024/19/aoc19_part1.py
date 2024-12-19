#
# Advent of Code 2024, day 19, part 1
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


def is_possible_design(design, stripes):
    usable_stripes = [stripe for stripe in stripes if stripe in design]

    @functools.cache
    def is_possible(d):
        if not d:
            return True

        for stripe in usable_stripes:
            if d.startswith(stripe):
                if is_possible(d.replace(stripe, "", 1)):
                    return True

        return False

    return is_possible(design)


def get_possible_designs(designs, stripes):
    return [design for design in designs if is_possible_design(design, stripes)]


def run_program(input):
    stripes, designs = parse_input(input)
    possible_designs = get_possible_designs(designs, stripes)
    return len(possible_designs)


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

        self.assertEqual(result, 6)
