#
# Advent of Code 2024, day 16, part 2
#

import heapq
import itertools
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


def opposite_face(face):
    return FACES[(FACES.index(face) + 2) % len(FACES)]


def get_score_dict_for_starting_positions(map, starts_with_faces):
    # Use a slightly modified version of Dijkstra's algorithm from part 1 to
    # get the scores dictionary with lowest (best) scores for each position.
    # Start from the given list of starting positions, including faces.
    INFINITY = len(map) * len(map[0]) * SCORE_INCREASE_TURN

    scores = {}
    for start in starts_with_faces:
        scores = {start: 0}
    for i, j in all_tiles(map):
        if map[i][j] != TILE_WALL:
            for face in FACES:
                scores.setdefault((i, j, face), INFINITY)

    pq = []
    for start in starts_with_faces:
        # Format: (score, i, j, face)
        heapq.heappush(pq, (0, *start))
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
                if new_score <= scores[(new_i, new_j, new_face)]:
                    scores[(new_i, new_j, new_face)] = new_score
                    heapq.heappush(pq, (new_score, new_i, new_j, new_face))

    return scores


def compute_number_of_tiles_on_best_paths(map):
    # The computation works as follows:
    # 1) Get the scores dictionary from Dijkstra's algorithm from the start tile.
    # 2) Get the scores dictionary from Dijkstra's algorithm from the end tile
    #    while considering all possible faces.
    # 3) Go over all the tiles in the map and check if the sum of scores from
    #    both start and end is the best score (while considering the fact that
    #    the faces for start and end are either opposite or one turn away to
    #    handle corners). If so, this tile is on a best path.
    start = find_tile(map, TILE_START)
    end = find_tile(map, TILE_END)

    from_start_scores = get_score_dict_for_starting_positions(map, [(*start, "E")])
    best_score = min(
        score for (i, j, _), score in from_start_scores.items() if (i, j) == end
    )
    from_end_scores = get_score_dict_for_starting_positions(
        map, [(*end, face) for face in FACES]
    )

    tiles = {start, end}
    for i, j in all_tiles(map):
        for face1, face2 in itertools.product(FACES, repeat=2):
            from_start = (i, j, face1)
            from_end = (i, j, face2)
            if (
                face1 == opposite_face(face2)
                and from_start_scores.get(from_start, 0)
                + from_end_scores.get(from_end, 0)
                == best_score
            ):
                tiles.add((i, j))
            elif faces_are_one_turn_away(face1, face2) and from_start_scores.get(
                from_start, 0
            ) + from_end_scores.get(from_end, 0) == (best_score - SCORE_INCREASE_TURN):
                tiles.add((i, j))
    return len(tiles)


def run_program(input):
    map = parse_input(input)
    return compute_number_of_tiles_on_best_paths(map)


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
