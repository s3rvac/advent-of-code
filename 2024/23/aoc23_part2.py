#
# Advent of Code 2024, day 23, part 2
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


def find_largest_set_of_interconnected_computers(connections):
    neighbors = collections.defaultdict(set)
    for pc1, pc2 in connections:
        neighbors[pc1].add(pc2)
        neighbors[pc2].add(pc1)

    def are_all_connected(computers):
        computers = set(computers)
        for c in computers:
            if not computers.issubset({c} | neighbors[c]):
                return False
        return True

    def compute_largest_interconnected_set_for(c):
        # Try all combinations of computers, starting from the largest possible
        # size and going lower until all the computers are interconnected.
        all = [c, *neighbors[c]]
        for size in range(len(all) - 1, 0, -1):
            for computers in itertools.combinations(all, size):
                if are_all_connected(computers):
                    return computers
        return [c]

    sets = [compute_largest_interconnected_set_for(c) for c in neighbors]
    largest_sets = sorted(sets, reverse=True, key=len)
    return largest_sets[0]


def get_password_for_computers(computers):
    return ",".join(sorted(computers))


def run_program(input):
    connections = parse_input(input)
    computers = find_largest_set_of_interconnected_computers(connections)
    return get_password_for_computers(computers)


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

        self.assertEqual(result, "co,de,ka,ta")
