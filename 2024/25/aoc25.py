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
    locks = []
    keys = []

    for raw_object in input.strip().split("\n\n"):
        object = [list(line) for line in raw_object.split("\n")]
        if object[0][0] == "#":
            locks.append(object)
        else:
            keys.append(object)

    return locks, keys


def count_lock_key_pairs_that_fit_together(locks, keys):
    def do_they_fit_together(lock, key):
        for i in range(len(lock)):
            for j in range(len(lock[i])):
                if lock[i][j] == "#" and key[i][j] == "#":
                    return False
        return True

    return sum(
        1 if do_they_fit_together(lock, key) else 0
        for lock, key in itertools.product(locks, keys)
    )


def run_program(input):
    locks, keys = parse_input(input)
    return count_lock_key_pairs_that_fit_together(locks, keys)


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
