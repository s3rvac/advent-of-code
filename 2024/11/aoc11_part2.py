#
# Advent of Code 2024, day 11, part 2
#

import collections
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return collections.Counter({int(n): 1 for n in input.strip().split()})


def blink(stones):
    new_stones = collections.Counter()
    for stone, count in stones.items():
        if stone == 0:
            new_stones[1] += count
        elif len(str(stone)) % 2 == 0:
            s = str(stone)
            n = len(s) // 2
            new_stones[int(s[n:])] += count
            new_stones[int(s[:n])] += count
        else:
            new_stones[stone * 2024] += count
    return new_stones


def run_program(input):
    stones = parse_input(input)
    for _ in range(75):
        stones = blink(stones)
    return sum(stones.values())


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            125 17
            """
        )

        result = run_program(input)

        self.assertEqual(result, 65601038650482)
