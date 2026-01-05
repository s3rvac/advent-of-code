#
# Advent of Code 2025, day 08, part 2
#

import itertools
import math
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    def parse_line(line):
        x, y, z = line.split(",")
        return (int(x), int(y), int(z))

    return [parse_line(line) for line in input.strip().split("\n")]


def connect_junction_boxes_and_get_result(coords):
    def distance(c1, c2):
        # https://en.wikipedia.org/wiki/Euclidean_distance
        x1, y1, z1 = c1
        x2, y2, z2 = c2
        return math.sqrt(
            math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2) + math.pow(z1 - z2, 2)
        )

    def all_junction_boxes_form_single_circuit():
        # To speed up the computation, first check if all junction boxes have
        # at least one connection. If they do not, they cannot form a circuit.
        if not all(connections.values()):
            return False

        # Check if all junction boxes form a single circuit by checking that
        # all junction boxes are reachable from the first junction box.
        # https://en.wikipedia.org/wiki/Strongly_connected_component
        scc = set()
        to_process = {coords[0]}
        while to_process:
            c1 = to_process.pop()
            scc.add(c1)
            for c2 in connections[c1]:
                if c2 not in scc:
                    to_process.add(c2)
                    scc.add(c2)
        return len(scc) == len(coords)

    # Process the junction boxes in pairs ordered by their distance (from
    # shortest distance to the largest one).
    connections = {c: [] for c in coords}
    coord_pairs_to_process = sorted(
        itertools.combinations(coords, 2), key=lambda x: distance(x[0], x[1])
    )
    for c1, c2 in coord_pairs_to_process:
        connections[c1].append(c2)
        connections[c2].append(c1)
        if all_junction_boxes_form_single_circuit():
            return c1[0] * c2[0]

    raise AssertionError("invalid input")


def run_program(input):
    coords = parse_input(input)
    return connect_junction_boxes_and_get_result(coords)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            162,817,812
            57,618,57
            906,360,560
            592,479,940
            352,342,300
            466,668,158
            542,29,236
            431,825,988
            739,650,466
            52,470,668
            216,146,977
            819,987,18
            117,168,530
            805,96,715
            346,949,466
            970,615,88
            941,993,340
            862,61,35
            984,92,344
            425,690,689
            """
        )

        result = run_program(input)

        self.assertEqual(result, 25272)
