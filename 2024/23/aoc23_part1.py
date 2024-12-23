#
# Advent of Code 2024, day 23, part 1
#

import collections
import itertools
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [tuple(line.split("-")) for line in input.strip().split("\n")]


def find_sets_of_three_connected_computers(connections):
    neighbors = collections.defaultdict(set)
    for c1, c2 in connections:
        neighbors[c1].add(c2)
        neighbors[c2].add(c1)

    def are_all_connected(computers):
        c1, c2, c3 = computers
        return (
            c2 in neighbors[c1]
            and c3 in neighbors[c1]
            and c2 in neighbors[c3]
            and c1 in neighbors[c3]
            and c1 in neighbors[c2]
            and c3 in neighbors[c2]
        )

    # Check all combinations of three computers whether they are all connected
    # together.
    return list(filter(are_all_connected, itertools.combinations(neighbors, 3)))


def get_sets_containing_computer_starting_with(sets, letter):
    def at_least_one_starts_with_letter(computers):
        for c in computers:
            if c.startswith(letter):
                return True
        return False

    return list(filter(at_least_one_starts_with_letter, sets))


def run_program(input):
    connections = parse_input(input)
    sets = find_sets_of_three_connected_computers(connections)
    sets = get_sets_containing_computer_starting_with(sets, letter="t")
    return len(sets)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            kh-tc
            qp-kh
            de-cg
            ka-co
            yn-aq
            qp-ub
            cg-tb
            vc-aq
            tb-ka
            wh-tc
            yn-cg
            kh-ub
            ta-co
            de-co
            tc-td
            tb-wq
            wh-td
            ta-ka
            td-qp
            aq-cg
            wq-ub
            ub-vc
            de-ta
            wq-aq
            wq-vc
            wh-yn
            ka-de
            kh-ta
            co-tc
            wh-qp
            tb-vc
            td-yn
            """
        )

        result = run_program(input)

        self.assertEqual(result, 7)
