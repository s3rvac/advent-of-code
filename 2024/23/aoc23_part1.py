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


def find_sets_of_three_connected_computers_with_at_least_one_starting_with_letter(
    connections, target_letter
):
    neighbors = collections.defaultdict(set)
    for c1, c2 in connections:
        neighbors[c1].add(c2)
        neighbors[c2].add(c1)

    def are_all_connected(c1, c2, c3):
        return (
            c2 in neighbors[c1]
            and c3 in neighbors[c1]
            and c2 in neighbors[c3]
            and c1 in neighbors[c3]
            and c1 in neighbors[c2]
            and c3 in neighbors[c2]
        )

    # For each computer whose name starts with the target letter, try all
    # combinations of its neighbors to see if they form three interconnected
    # computers.
    sets = set()
    for c1, other in [
        (c, other) for c, other in neighbors.items() if c.startswith(target_letter)
    ]:
        for c2, c3 in itertools.combinations(other, 2):
            if are_all_connected(c1, c2, c3):
                s = tuple(sorted((c1, c2, c3)))
                if s not in sets:
                    sets.add(s)
    return sets


def run_program(input):
    connections = parse_input(input)
    return len(
        find_sets_of_three_connected_computers_with_at_least_one_starting_with_letter(
            connections, target_letter="t"
        )
    )


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
