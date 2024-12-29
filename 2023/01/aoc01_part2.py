#
# Advent of Code 2023, day 01, part 2
#

import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [line.strip() for line in input.strip().split("\n")]


def compute_calibration_values(input):
    return [compute_calibration_value(line) for line in input]


def compute_calibration_value(line):
    first_digit = None
    last_digit = None

    for i in range(0, len(line)):
        c = get_digit_on_position(line, i)
        if c.isdigit():
            if first_digit is None:
                first_digit = last_digit = c
            else:
                last_digit = c

    return int(first_digit + last_digit)


def get_digit_on_position(line, i):
    map = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    for name, digit in map.items():
        if line[i : i + len(name)] == name:
            return digit

    return line[i]


def run_program(input):
    input = parse_input(input)
    calibration_values = compute_calibration_values(input)
    return sum(calibration_values)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input_from_first_part(self):
        input = textwrap.dedent(
            """
            1abc2
            pqr3stu8vwx
            a1b2c3d4e5f
            treb7uchet
            """
        )

        result = run_program(input)

        self.assertEqual(result, 142)

    def test_program_returns_correct_result_for_example_input_from_second_part(self):
        input = textwrap.dedent(
            """
            two1nine
            eightwothree
            abcone2threexyz
            xtwone3four
            4nineeightseven2
            zoneight234
            7pqrstsixteen
            """
        )

        result = run_program(input)

        self.assertEqual(result, 281)

    def test_program_returns_correct_result_when_digits_overlap(self):
        input = textwrap.dedent(
            """
            2sixsix264oneightm
            """
        )

        result = run_program(input)

        self.assertEqual(result, 28)
