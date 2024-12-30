#
# Advent of Code 2023, day 02, part 1
#

import re
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    def parse_line(line):
        m = re.fullmatch(r"Game (\d+): (.+)", line)
        assert m is not None
        return {
            "id": int(m.group(1)),
            "sets": parse_sets(m.group(2)),
        }

    def parse_sets(raw_sets):
        return [parse_set(raw_set) for raw_set in raw_sets.split("; ")]

    def parse_set(raw_set):
        set = []
        for part in raw_set.split(", "):
            m = re.fullmatch(r"(\d+) (.+)", part)
            assert m is not None
            set.append((m.group(2), int(m.group(1))))
        return set

    return [parse_line(line) for line in input.strip().split("\n")]


def get_ids_of_possible_games(games):
    ids = []
    for game in games:
        if is_possible_game(game):
            ids.append(game["id"])
    return ids


def is_possible_game(game):
    for set in game["sets"]:
        available_cubes = {"red": 12, "green": 13, "blue": 14}
        for color, count in set:
            available_cubes[color] -= count
        if min(available_cubes.values()) < 0:
            return False
    return True


def run_program(input):
    games = parse_input(input)
    return sum(get_ids_of_possible_games(games))


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
            Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
            Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
            Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
            Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
            """
        )

        result = run_program(input)

        self.assertEqual(result, 8)
