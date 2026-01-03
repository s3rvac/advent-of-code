#
# Advent of Code 2025, day 08, part 1
#

import collections
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


def connect_junction_boxes_and_get_size_of_largest_circuit(
    coords, connection_count, circuit_count
):
    def distance(c1, c2):
        # https://en.wikipedia.org/wiki/Euclidean_distance
        x1, y1, z1 = c1
        x2, y2, z2 = c2
        return math.sqrt(
            math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2) + math.pow(z1 - z2, 2)
        )

    def get_strongly_connected_components():
        # https://en.wikipedia.org/wiki/Strongly_connected_component
        sccs = []
        to_process = set(coords)
        while to_process:
            scc = set()
            to_process_scc = {to_process.pop()}
            while to_process_scc:
                c1 = to_process_scc.pop()
                scc.add(c1)
                for c2 in connections[c1]:
                    if c2 not in scc:
                        to_process_scc.add(c2)
                    scc.add(c2)
                    to_process.discard(c2)
            sccs.append(scc)
        return sccs

    # Process the junction boxes in pairs ordered by their distance (from
    # shortest distance to the largest one).
    connections = collections.defaultdict(list)
    coord_pairs_to_process = sorted(
        itertools.combinations(coords, 2), key=lambda x: distance(x[0], x[1])
    )
    for c1, c2 in coord_pairs_to_process[:connection_count]:
        connections[c1].append(c2)
        connections[c2].append(c1)

    sccs = get_strongly_connected_components()
    sccs_sizes = [len(scc) for scc in sorted(sccs)]
    return sorted(sccs_sizes, reverse=True)[:circuit_count]


def run_program(input, connection_count=1000):
    coords = parse_input(input)
    sizes = connect_junction_boxes_and_get_size_of_largest_circuit(
        coords,
        connection_count,
        circuit_count=3,
    )
    return math.prod(sizes)


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

        result = run_program(input, connection_count=10)

        self.assertEqual(result, 40)
