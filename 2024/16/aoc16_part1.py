#
# Advent of Code 2024, day 16, part 1
#

import heapq
import textwrap
import unittest


SCORE_INCREASE_STEP = 1
SCORE_INCREASE_TURN = 1000
TILE_START = "S"
TILE_END = "E"
TILE_WALL = "#"
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


def all_tiles(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            yield i, j


def find_tile(map, tile):
    for i, j in all_tiles(map):
        if map[i][j] == tile:
            return i, j
    raise AssertionError(f"tile {tile} not found")


def faces_are_one_turn_away(face1, face2):
    i1 = FACES.index(face1)
    i2 = FACES.index(face2)
    return abs(i1 - i2) == 1 or {i1, i2} == {0, len(FACES) - 1}


def compute_best_score_from_start_to_end(map):
    # Use a simplified version of Dijkstra's algorithm to find the path from
    # the start to the end having the lowest score.
    START = find_tile(map, TILE_START)
    END = find_tile(map, TILE_END)
    INFINITY = len(map) * len(map[0]) * SCORE_INCREASE_TURN

    scores = {(*START, "E"): 0}
    for i, j in all_tiles(map):
        if map[i][j] != TILE_WALL:
            for face in FACES:
                scores.setdefault((i, j, face), INFINITY)

    pq = []
    # Format: (score, i, j, face)
    heapq.heappush(pq, (0, *START, "E"))
    while pq:
        score, i, j, face = heapq.heappop(pq)
        if score > scores[(i, j, face)]:
            continue

        for new_face, (di, dj) in DIRECTIONS.items():
            new_i, new_j = i + di, j + dj
            if (
                0 <= new_i < len(map)
                and 0 <= new_j < len(map[i])
                and map[new_i][new_j] != TILE_WALL
            ):
                if new_face == face:
                    new_score = score + SCORE_INCREASE_STEP
                elif faces_are_one_turn_away(face, new_face):
                    new_score = score + SCORE_INCREASE_STEP + SCORE_INCREASE_TURN
                else:
                    new_score = score + SCORE_INCREASE_STEP + 2 * SCORE_INCREASE_TURN
                if new_score < scores[(new_i, new_j, new_face)]:
                    scores[(new_i, new_j, new_face)] = new_score
                    heapq.heappush(pq, (new_score, new_i, new_j, new_face))

    return min(score for (i, j, _), score in scores.items() if (i, j) == END)


def run_program(input):
    map = parse_input(input)
    return compute_best_score_from_start_to_end(map)


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

        self.assertEqual(result, 7036)

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

        self.assertEqual(result, 11048)
