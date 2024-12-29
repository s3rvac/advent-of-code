#
# Advent of Code 2023, day 04, part 1
#

import re
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [parse_card(line) for line in input.strip().split("\n")]


def parse_card(line):
    def parse_numbers(raw_numbers):
        return {int(n) for n in re.split(r"\s+", raw_numbers.strip())}

    m = re.fullmatch(r"Card +(\d+): (.*) \| (.*)", line)
    assert m is not None
    return {
        "id": int(m.group(1)),
        "winning_numbers": parse_numbers(m.group(2)),
        "own_numbers": parse_numbers(m.group(3)),
    }


def get_winning_points_for_cards(cards):
    return sum(map(get_winning_points_for_card, cards))


def get_winning_points_for_card(card):
    matches = len(card["own_numbers"] & card["winning_numbers"])
    return 0 if matches == 0 else 2 ** (matches - 1)


def run_program(input):
    cards = parse_input(input)
    return get_winning_points_for_cards(cards)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
            Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
            Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
            Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
            Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
            Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
            """
        )

        result = run_program(input)

        self.assertEqual(result, 13)
