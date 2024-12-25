#
# Advent of Code 2024, day 25, parts 1 & 2
#

import itertools
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [
        "".join(lines) for lines in input.strip().split("\n\n")
    ]


def count_non_overlapping_objects(objects):
    def are_non_overlapping(o1, o2):
        for i in range(len(o1)):
            if o1[i] == "#" and o2[i] == "#":
                return False
        return True

    locks = filter(lambda o: o[0] == "#", objects)
    keys = filter(lambda o: o[0] == ".", objects)
    return sum(
        1 if are_non_overlapping(o1, o2) else 0
        for o1, o2 in itertools.product(locks, keys)
    )


def run_program(input):
    objects = parse_input(input)
    return count_non_overlapping_objects(objects)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            #####
            .####
            .####
            .####
            .#.#.
            .#...
            .....

            #####
            ##.##
            .#.##
            ...##
            ...#.
            ...#.
            .....

            .....
            #....
            #....
            #...#
            #.#.#
            #.###
            #####

            .....
            .....
            #.#..
            ###..
            ###.#
            ###.#
            #####

            .....
            .....
            .....
            #....
            #.#..
            #.#.#
            #####
            """
        )

        result = run_program(input)

        self.assertEqual(result, 3)
