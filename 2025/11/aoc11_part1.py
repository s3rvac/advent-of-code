#
# Advent of Code 2025, day 11, part 1
#

import functools
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    devices = {}
    for line in input.strip().split("\n"):
        input, outputs = line.split(": ")
        devices[input] = outputs.split(" ")
    return devices


def get_number_of_paths_from_to(devices, from_device, to_device):
    @functools.cache
    def get_number_of_paths(current_device):
        if current_device == to_device:
            return 1
        return sum(get_number_of_paths(next) for next in devices[current_device])

    return get_number_of_paths(from_device)


def run_program(input):
    devices = parse_input(input)
    return get_number_of_paths_from_to(devices, from_device="you", to_device="out")


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            aaa: you hhh
            you: bbb ccc
            bbb: ddd eee
            ccc: ddd eee fff
            ddd: ggg
            eee: out
            fff: out
            ggg: out
            hhh: ccc fff iii
            iii: out
            """
        )

        result = run_program(input)

        self.assertEqual(result, 5)
