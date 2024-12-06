#
# Advent of Code 2024, day 05, part 1
#

import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    def parse_rule(raw_rule):
        m, n = raw_rule.split("|")
        return int(m), int(n)

    def parse_update(raw_update):
        return [int(n) for n in raw_update.split(",")]

    raw_rules, raw_updates = input.strip().split("\n\n")
    rules = [parse_rule(line) for line in raw_rules.split("\n")]
    updates = [parse_update(line) for line in raw_updates.split("\n")]
    return rules, updates


def is_correctly_ordered_update(rules, update):
    for before, after in rules:
        if before in update and after in update:
            if update.index(before) > update.index(after):
                return False
    return True


def get_correctly_ordered_updates(rules, updates):
    return [update for update in updates if is_correctly_ordered_update(rules, update)]


def get_middle_page_numbers(updates):
    return [update[len(update) // 2] for update in updates]


def run_program(input):
    rules, updates = parse_input(input)
    correct_updates = get_correctly_ordered_updates(rules, updates)
    return sum(get_middle_page_numbers(correct_updates))


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            47|53
            97|13
            97|61
            97|47
            75|29
            61|13
            75|53
            29|13
            97|29
            53|29
            61|53
            97|53
            61|29
            47|13
            75|47
            97|75
            47|61
            75|61
            47|29
            75|13
            53|13

            75,47,61,53,29
            97,61,53,29,13
            75,29,13
            75,97,47,61,53
            61,13,29
            97,13,75,29,47
            """
        )

        result = run_program(input)

        self.assertEqual(result, 143)
