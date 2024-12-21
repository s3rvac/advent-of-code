#
# Advent of Code 2024, day 21, part 1
#

import functools
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return input.strip().splitlines()


def numeric_keypresses_for(fr, to):
    # A manually crafted mapping of buttons on the numeric keypad that have to
    # be pressed to get the fewest button presses on the directional keyboard.
    # For example, when we need to press ">", ">", and "^", it we should press
    # them in order ">>^" instead of ">^>" as the latter order would result in
    # more keypresses on the directional keyboard (indeed, if we are already on
    # a key, we just need to press "A" on the keypad down the line).
    #
    # +---+---+---+
    # | 7 | 8 | 9 |
    # +---+---+---+
    # | 4 | 5 | 6 |
    # +---+---+---+
    # | 1 | 2 | 3 |
    # +---+---+---+
    #     | 0 | A |
    #     +---+---+
    match fr, to:
        case "A", "0":
            return "<A"
        case "A", "1":
            return "^<<A"
        case "A", "2":
            return "<^A"
        case "A", "3":
            return "^A"
        case "A", "4":
            return "^^<<A"
        case "A", "5":
            return "^^<A"
        case "A", "6":
            return "^^A"
        case "A", "7":
            return "^^^<<A"
        case "A", "8":
            return "^^^<A"
        case "A", "9":
            return "^^^A"
        case "0", "A":
            return ">A"
        case "0", "1":
            return "^<A"
        case "0", "2":
            return "^A"
        case "0", "3":
            return "^>A"
        case "0", "4":
            return "^^<A"
        case "0", "5":
            return "^^A"
        case "0", "6":
            return "^^>A"
        case "0", "7":
            return "^^^<A"
        case "0", "8":
            return "^^^A"
        case "0", "9":
            return "^^^>A"
        case "1", "A":
            return ">>vA"
        case "1", "0":
            return ">vA"
        case "1", "2":
            return ">A"
        case "1", "3":
            return ">>A"
        case "1", "4":
            return "^A"
        case "1", "5":
            return ">^A"
        case "1", "6":
            return ">>^A"
        case "1", "7":
            return "^^A"
        case "1", "8":
            return "^^>A"
        case "1", "9":
            return "^^>>A"
        case "2", "A":
            return "v>A"
        case "2", "0":
            return "vA"
        case "2", "1":
            return "<A"
        case "2", "3":
            return ">A"
        case "2", "4":
            return "<^A"
        case "2", "5":
            return "^A"
        case "2", "6":
            return "^>A"
        case "2", "7":
            return "^^<A"
        case "2", "8":
            return "^^A"
        case "2", "9":
            return ">^^A"
        case "3", "A":
            return "vA"
        case "3", "0":
            return "<vA"
        case "3", "1":
            return "<<A"
        case "3", "2":
            return "<A"
        case "3", "4":
            return "<<^A"
        case "3", "5":
            return "^<A"
        case "3", "6":
            return "^A"
        case "3", "7":
            return "<<^^A"
        case "3", "8":
            return "<^^A"
        case "3", "9":
            return "^^A"
        case "4", "A":
            return ">>vvA"
        case "4", "0":
            return ">vvA"
        case "4", "1":
            return "vA"
        case "4", "2":
            return "v>A"
        case "4", "3":
            return "v>>A"
        case "4", "5":
            return ">A"
        case "4", "6":
            return ">>A"
        case "4", "7":
            return "^A"
        case "4", "8":
            return "^>A"
        case "4", "9":
            return "^>>A"
        case "5", "A":
            return "vv>A"
        case "5", "0":
            return "vvA"
        case "5", "1":
            return "v<A"
        case "5", "2":
            return "vA"
        case "5", "3":
            return "v>A"
        case "5", "4":
            return "<A"
        case "5", "6":
            return ">A"
        case "5", "7":
            return "^<A"
        case "5", "8":
            return "^A"
        case "5", "9":
            return "^>A"
        case "6", "A":
            return "vvA"
        case "6", "0":
            return "vv<A"
        case "6", "1":
            return "v<<A"
        case "6", "2":
            return "v<A"
        case "6", "3":
            return "vA"
        case "6", "4":
            return "<<A"
        case "6", "5":
            return "<A"
        case "6", "7":
            return "^<<A"
        case "6", "8":
            return "^<A"
        case "6", "9":
            return "^A"
        case "7", "A":
            return ">>vvvA"
        case "7", "0":
            return ">vvvA"
        case "7", "1":
            return "vvA"
        case "7", "2":
            return "vv>A"
        case "7", "3":
            return "vv>>A"
        case "7", "4":
            return "vA"
        case "7", "5":
            return "v>A"
        case "7", "6":
            return "v>>A"
        case "7", "8":
            return ">A"
        case "7", "9":
            return ">>A"
        case "8", "A":
            return "vvv>A"
        case "8", "0":
            return "vvvA"
        case "8", "1":
            return "vv<A"
        case "8", "2":
            return "vvA"
        case "8", "3":
            return "vv>A"
        case "8", "4":
            return "v<A"
        case "8", "5":
            return "vA"
        case "8", "6":
            return "v>A"
        case "8", "7":
            return "<A"
        case "8", "9":
            return ">A"
        case "9", "A":
            return "vvvA"
        case "9", "0":
            return "vvv<A"
        case "9", "1":
            return "vv<<A"
        case "9", "2":
            return "vv<A"
        case "9", "3":
            return "vvA"
        case "9", "4":
            return "v<<A"
        case "9", "5":
            return "v<A"
        case "9", "6":
            return "vA"
        case "9", "7":
            return "<<A"
        case "9", "8":
            return "<A"
        case _:
            return "A"


def dir_keypresses_for(fr, to):
    # A manually crafted mapping of buttons on the directional keypad that have
    # to be pressed to get the fewest button presses down the line.
    # A similar reasoning to the one provided for the numeric keypad holds here
    # as well.
    #
    #     +---+---+
    #     | ^ | A |
    # +---+---+---+
    # | < | v | > |
    # +---+---+---+
    match fr, to:
        case "A", "^":
            return "<A"
        case "A", "<":
            return "v<<A"
        case "A", "v":
            return "<vA"
        case "A", ">":
            return "vA"
        case "^", "A":
            return ">A"
        case "^", "<":
            return "v<A"
        case "^", "v":
            return "vA"
        case "^", ">":
            return "v>A"
        case "<", "A":
            return ">>^A"
        case "<", "^":
            return ">^A"
        case "<", "v":
            return ">A"
        case "<", ">":
            return ">>A"
        case "v", "A":
            return "^>A"
        case "v", "^":
            return "^A"
        case "v", "<":
            return "<A"
        case "v", ">":
            return ">A"
        case ">", "A":
            return "^A"
        case ">", "^":
            return "<^A"
        case ">", "<":
            return "<<A"
        case ">", "v":
            return "<A"
        case _:
            return "A"


def compute_fewest_button_presses(code, dir_keypad_count):
    # Computes the fewest number of button presses for the given code and
    # number of directional keypads.
    #
    # We do the computation recursively via the divide-and-conquer algorithm as
    # each robot always ends up on the "A" button. We also utilize caching to
    # speed up the computation (already computed button presses can be reused
    # in the future).

    @functools.cache
    def fewest_keypad_presses(to_press, depth, keypresses_func):
        if depth == 0:
            return len(to_press)

        fewest_presses = 0
        current = "A"
        for target in to_press:
            presses = keypresses_func(current, target)
            current = target
            fewest_presses += fewest_keypad_presses(
                presses, depth - 1, dir_keypresses_for
            )
        return fewest_presses

    return fewest_keypad_presses(code, dir_keypad_count, numeric_keypresses_for)


def compute_complexity_of_fewest_button_presses(code, dir_keypad_count):
    presses = compute_fewest_button_presses(code, dir_keypad_count)
    return presses * int(code.rstrip("A"))


def run_program(input, dir_keypad_count=2 + 1):
    codes = parse_input(input)
    return sum(
        compute_complexity_of_fewest_button_presses(code, dir_keypad_count)
        for code in codes
    )


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        self.assertEqual(run_program("029A"), 1972)
        self.assertEqual(run_program("980A"), 58800)
        self.assertEqual(run_program("179A"), 12172)
        self.assertEqual(run_program("456A"), 29184)
        self.assertEqual(run_program("379A"), 24256)
