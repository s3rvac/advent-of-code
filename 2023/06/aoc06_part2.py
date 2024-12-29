#
# Advent of Code 2023, day 06, part 2
#

import re
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    lines = input.strip().split("\n")

    m = re.fullmatch(r"Time:\s+(.+)", lines[0])
    time = int(re.sub(r"\s+", "", m.group(1)))

    m = re.fullmatch(r"Distance:\s+(.+)", lines[1])
    record_distance = int(re.sub(r"\s+", "", m.group(1)))

    return time, record_distance


def compute_number_of_ways_to_beat_record(time, record_distance):
    ways_to_beat_record = 0
    for n in range(1, time):
        distance = n * (time - n)
        if distance > record_distance:
            ways_to_beat_record += 1
    return ways_to_beat_record


def run_program(input):
    time, record_distance = parse_input(input)
    return compute_number_of_ways_to_beat_record(time, record_distance)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            Time:      7  15   30
            Distance:  9  40  200
            """
        )

        result = run_program(input)

        self.assertEqual(result, 71503)
