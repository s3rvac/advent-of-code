#
# Advent of Code 2025, day 11, part 2
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
    # The paths have to visit both `dac` and `fft` (in any order):
    @functools.cache
    def get_number_of_paths(current_device, dac_visited, fft_visited):
        if current_device == to_device:
            return 1 if dac_visited and fft_visited else 0
        elif current_device == "dac":
            dac_visited = True
        elif current_device == "fft":
            fft_visited = True
        return sum(
            get_number_of_paths(next, dac_visited, fft_visited)
            for next in devices[current_device]
        )

    return get_number_of_paths(from_device, dac_visited=False, fft_visited=False)


def run_program(input):
    devices = parse_input(input)
    return get_number_of_paths_from_to(devices, from_device="svr", to_device="out")


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            svr: aaa bbb
            aaa: fft
            fft: ccc
            bbb: tty
            tty: ccc
            ccc: ddd eee
            ddd: hub
            hub: fff
            eee: dac
            dac: fff
            fff: ggg hhh
            ggg: out
            hhh: out
            """
        )

        result = run_program(input)

        self.assertEqual(result, 2)
