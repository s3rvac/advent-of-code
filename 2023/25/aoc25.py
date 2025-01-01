#
# Advent of Code 2023, day 25
#
# WARNING: The solution works for my input but might not be general enough to
# work for any input!
#
# Requirements: pip install networkx==3.4.2
#

import textwrap
import unittest

import networkx


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    graph = networkx.Graph()
    for line in input.strip().split("\n"):
        nodes = line.replace(":", "").split()
        for node in nodes[1:]:
            graph.add_edge(nodes[0], node, weight=1)
    return graph


def disconnect_wires_to_separate_graph_into_two_components(graph):
    # Use the Stoer-Wagner algorithm [1], implemented in the networkx library
    # [2], to find the minimal cut in the graph. For both the example and my
    # input, the cut size is 3, which means that the graph can be separated
    # into two components by removing 3 edges. This is exactly what is required
    # by the assignment. Hence, I did not invest more time into finding a
    # general solution.
    #
    # [1] https://en.wikipedia.org/wiki/Stoer%E2%80%93Wagner_algorithm
    # [2] https://networkx.org/documentation/networkx-3.4/reference/algorithms/generated/networkx.algorithms.connectivity.stoerwagner.stoer_wagner.html
    cut_size, components = networkx.stoer_wagner(graph)
    assert cut_size == 3, "your input requires multiple algorithm runs"
    return components


def run_program(input):
    graph = parse_input(input)
    components = disconnect_wires_to_separate_graph_into_two_components(graph)
    return len(components[0]) * len(components[1])


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            jqt: rhn xhk nvd
            rsh: frs pzl lsr
            xhk: hfx
            cmg: qnr nvd lhk bvb
            rhn: xhk bvb hfx
            bvb: xhk hfx
            pzl: lsr hfx nvd
            qnr: nvd
            ntq: jqt hfx bvb xhk
            nvd: lhk
            lsr: lhk
            rzs: qnr cmg lsr rsh
            frs: qnr lhk lsr
            """
        )

        result = run_program(input)

        self.assertEqual(result, 54)
