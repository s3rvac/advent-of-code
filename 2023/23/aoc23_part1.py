#
# Advent of Code 2023, day 23, part 1
#

import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split("\n")]


def get_longest_hike_length(map):
    # We perform a depth-first search and store the length of each hike. Then,
    # we return the length of the longest hike.
    longest_hike_length = 0

    # The start is always in the first row and second column.
    START = 0, 1

    # The end is always in the last row and second-to-last column.
    END = len(map) - 1, len(map[-1]) - 2

    # Format: (i, j, steps, visited)
    hikes_to_check = [(*START, 0, set())]
    while hikes_to_check:
        i, j, steps, visited = hikes_to_check.pop()
        for ix, jx in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            new_i = i + ix
            new_j = j + jx
            if (
                new_i < 0
                or new_i >= len(map)
                or new_j < 0
                or new_j >= len(map[0])
                or map[new_i][new_j] == "#"
                or (new_i, new_j) in visited
            ):
                continue

            if map[new_i][new_j] in "<>^v":
                if (map[new_i][new_j], ix, jx) in [
                    (">", 0, 1),
                    ("<", 0, -1),
                    ("^", -1, 0),
                    ("v", 1, 0),
                ]:
                    hikes_to_check.append(
                        (
                            new_i + ix,
                            new_j + jx,
                            steps + 2,
                            visited | {(new_i, new_j), (new_i + ix, new_j + jx)},
                        )
                    )
                else:
                    continue

            if (new_i, new_j) == END:
                longest_hike_length = max(steps + 1, longest_hike_length)
                continue

            hikes_to_check.append((new_i, new_j, steps + 1, visited | {(new_i, new_j)}))

    return longest_hike_length


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

        self.assertEqual(result, 94)
