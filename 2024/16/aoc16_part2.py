#
# Advent of Code 2024, day 16, part 2
#

import textwrap
import unittest


SCORE_INCREASE_STEP = 1
SCORE_INCREASE_TURN = 1000
TILE_REINDEER = "S"
TILE_END = "E"
FACES = ["N", "E", "S", "W"]
DIRECTIONS = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split("\n")]


def find_reindeer(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == TILE_REINDEER:
                return i, j
    raise AssertionError("reindeer not found")


def compute_best_paths_to_end(map):
    def try_step(i, j, face, score, path):
        di, dj = DIRECTIONS[face]
        i, j = i + di, j + dj
        if map[i][j] != "#" and (i, j) not in path:
            new_score = score + SCORE_INCREASE_STEP
            new_path = path | {(i, j)}
            to_check.append((i, j, face, new_score, new_path))

    # Do a depth-first search while keeping the score and the traversed paths.
    i, j = find_reindeer(map)
    best_score = None
    paths_to_end = []
    visited = {}
    # Format: (i, j, face, score, path)
    to_check = [(i, j, "E", 0, {(i, j)})]
    while to_check:
        i, j, face, score, path = to_check.pop()

        if map[i][j] == TILE_END:
            paths_to_end.append((score, path))
            if best_score is None or score <= best_score:
                best_score = score
            continue

        # (Optimization) If we have already visited the tile with a lower
        # score, it does not make sense to pursue the current path.
        visited_score = visited.get((i, j, face))
        if visited_score is not None and score > visited_score:
            continue
        visited[(i, j, face)] = score

        # (Optimization) If we already know that our path cannot result in the
        # best score, we can stop pursuing it.
        if best_score is not None and score > best_score:
            continue

        # Try doing a step forward.
        try_step(i, j, face, score, path)

        # Try turning left and doing a step.
        left_face = FACES[(FACES.index(face) - 1) % len(FACES)]
        try_step(i, j, left_face, score + SCORE_INCREASE_TURN, path)

        # Try turning right and doing a step.
        right_face = FACES[(FACES.index(face) + 1) % len(FACES)]
        try_step(i, j, right_face, score + SCORE_INCREASE_TURN, path)

    best_paths = [path for score, path in paths_to_end if score == best_score]
    return best_paths


def compute_number_of_unique_tiles_on_paths(paths):
    tiles = set()
    for path in paths:
        for tile in path:
            tiles.add(tile)
    return len(tiles)


def run_program(input):
    map = parse_input(input)
    best_paths = compute_best_paths_to_end(map)
    return compute_number_of_unique_tiles_on_paths(best_paths)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input1(self):
        input = textwrap.dedent(
            """
            ###############
            #.......#....E#
            #.#.###.#.###.#
            #.....#.#...#.#
            #.###.#####.#.#
            #.#.#.......#.#
            #.#.#####.###.#
            #...........#.#
            ###.#.#####.#.#
            #...#.....#.#.#
            #.#.#.###.#.#.#
            #.....#...#.#.#
            #.###.#.#.#.#.#
            #S..#.....#...#
            ###############
            """
        )

        result = run_program(input)

        self.assertEqual(result, 45)

    def test_program_returns_correct_result_for_example_input2(self):
        input = textwrap.dedent(
            """
            #################
            #...#...#...#..E#
            #.#.#.#.#.#.#.#.#
            #.#.#.#...#...#.#
            #.#.#.#.###.#.#.#
            #...#.#.#.....#.#
            #.#.#.#.#.#####.#
            #.#...#.#.#.....#
            #.#.#####.#.###.#
            #.#.#.......#...#
            #.#.###.#####.###
            #.#.#...#.....#.#
            #.#.#.#####.###.#
            #.#.#.........#.#
            #.#.#.#########.#
            #S#.............#
            #################
            """
        )

        result = run_program(input)

        self.assertEqual(result, 64)
