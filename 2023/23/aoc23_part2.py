#
# Advent of Code 2023, day 23, part 2
#

import collections
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split("\n")]


def get_longest_hike_length(map):
    # We find the longest hike in two steps:
    #
    # 1) First, we construct a graph out of the grid in a way that minimizes
    #    the number of nodes by compressing "long halls" that do not have any
    #    turns. This has to be done in order to make the second step
    #    computationally feasible.
    # 2) Second, we use the graph to find the longest hike by checking all the
    #    hikes in it.

    # The end is always in the last row and second-to-last column.
    END = len(map) - 1, len(map[-1]) - 2

    # Graph format: (i, j): {(neighbor i, neighbor j, distance), ...}
    graph = collections.defaultdict(set)

    # Step 1): Use depth-first search to construct the graph.
    # Stack format: (i, j, from_i, from_j, orig_i, orig_j, distance)
    s = [(1, 1, 0, 1, 0, 1, 1)]
    visited = set()
    while s:
        i, j, from_i, from_j, orig_i, orig_j, distance = s.pop()

        if (i, j) in visited or (i, j) == END:
            graph[(orig_i, orig_j)].add((i, j, distance))
            continue

        neighbors = []
        for ni, nj in [(i, j + 1), (i + 1, j), (i - 1, j), (i, j - 1)]:
            if (
                (ni, nj) != (from_i, from_j)
                and 0 <= ni < len(map)
                and 0 <= nj < len(map[i])
                and map[ni][nj] != "#"
            ):
                neighbors.append((ni, nj))
        if len(neighbors) == 1:
            # A "long hall".
            s.append((*neighbors[0], i, j, orig_i, orig_j, distance + 1))
        elif len(neighbors) > 1:
            # Multiple neighbors (i.e. a "hub" node).
            visited.add((i, j))
            graph[(orig_i, orig_j)].add((i, j, distance))
            graph[(i, j)].add((orig_i, orig_j, distance))
            for ni, nj in neighbors:
                s.append((ni, nj, i, j, i, j, 1))

    # Step 2): Check all possible hikes to find the longest one.
    hike_lengths = set()

    # Format: (i, j, steps, visited nodes)
    hikes_to_check = [(0, 1, 0, set())]
    while hikes_to_check:
        i, j, steps, visited = hikes_to_check.pop()
        for new_i, new_j, distance in graph[(i, j)]:
            if (new_i, new_j) == END:
                hike_lengths.add(steps + distance)
                continue

            if (new_i, new_j) not in visited:
                hikes_to_check.append(
                    (new_i, new_j, steps + distance, visited | {(new_i, new_j)})
                )

    return max(hike_lengths)


def run_program(input):
    map = parse_input(input)
    return get_longest_hike_length(map)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            #.#####################
            #.......#########...###
            #######.#########.#.###
            ###.....#.>.>.###.#.###
            ###v#####.#v#.###.#.###
            ###.>...#.#.#.....#...#
            ###v###.#.#.#########.#
            ###...#.#.#.......#...#
            #####.#.#.#######.#.###
            #.....#.#.#.......#...#
            #.#####.#.#.#########v#
            #.#...#...#...###...>.#
            #.#.#v#######v###.###v#
            #...#.>.#...>.>.#.###.#
            #####v#.#.###v#.#.###.#
            #.....#...#...#.#.#...#
            #.#########.###.#.#.###
            #...###...#...#...#.###
            ###.###.#.###v#####v###
            #...#...#.#.>.>.#.>.###
            #.###.###.#.###.#.#v###
            #.....###...###...#...#
            #####################.#
            """
        )

        result = run_program(input)

        self.assertEqual(result, 154)
