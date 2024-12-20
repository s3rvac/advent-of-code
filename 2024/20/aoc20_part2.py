#
# Advent of Code 2024, day 20, part 2
#

import collections
import itertools
import textwrap
import unittest


NEIGHBOR_DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
TILE_START = "S"
TILE_END = "E"
TILE_WALL = "#"


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split("\n")]


def all_non_wall_tiles(map):
    for i in range(1, len(map) - 1):
        for j in range(1, len(map[i]) - 1):
            if map[i][j] != TILE_WALL:
                yield i, j


def find_tile(map, tile):
    for i, j in all_non_wall_tiles(map):
        if map[i][j] == tile:
            return i, j
    raise AssertionError(f"tile {tile} not found")


def taxicab_distance(i1, j1, i2, j2):
    # https://en.wikipedia.org/wiki/Taxicab_geometry
    return abs(i1 - i2) + abs(j1 - j2)


def all_pairs_of_free_space_at_most_length_apart(map, max_length):
    # We could just use `itertools.product(all_non_wall_tiles(map), repeat=2)`,
    # but the following way is much faster (altough less readable) as it goes
    # over fewer pairs.
    for i1, j1 in all_non_wall_tiles(map):
        for i2 in range(
            max(1, i1 - max_length - 1), min(i1 + max_length + 1, len(map) - 1)
        ):
            for j2 in range(
                max(1, j1 - max_length - 1), min(j1 + max_length + 1, len(map[i2]) - 1)
            ):
                if (
                    map[i2][j2] != TILE_WALL
                    and taxicab_distance(i1, j1, i2, j2) <= max_length
                ):
                    yield (i1, j1), (i2, j2)


def get_times_to_get_to_each_tile_from_start_tile(map, start_tile):
    # Use breadth-first search from the start tile to get a mapping of each
    # tile to the time required to get to it from the start tile.
    times_map = {}
    visited = set()
    # Format: (i, j, time)
    q = collections.deque([(*start_tile, 0)])

    while q:
        i, j, time = q.popleft()
        times_map[(i, j)] = time
        visited.add((i, j))

        for di, dj in NEIGHBOR_DIRECTIONS:
            new_i, new_j = i + di, j + dj
            if (
                0 <= new_i < len(map)
                and 0 <= new_j < len(map[i])
                and map[new_i][new_j] != TILE_WALL
                and (new_i, new_j) not in visited
            ):
                q.append((new_i, new_j, time + 1))

    return times_map


def get_cheat_count_to_finish_race_and_save_time(map, cheat_length, min_time_save):
    # We do it this way:
    #
    # 1) Get a mapping of each tile to the time required to get to it from the
    #    START tile.
    # 2) Get a mapping of each tile to the time required to get to it from the
    #    END tile.
    # 3) Generate all possible pairs of free space that are at most
    #    `cheat_length` apart. These are our only options for cheating.
    # 4) For all those pairs `(m, n)`, check if we can save enough time by
    #    going from the START tile to `m`, then from `m to `n`, and then from
    #    `n` to the END tile.
    start_tile = find_tile(map, TILE_START)
    times_start = get_times_to_get_to_each_tile_from_start_tile(map, start_tile)

    end_tile = find_tile(map, TILE_END)
    times_end = get_times_to_get_to_each_tile_from_start_tile(map, end_tile)

    baseline = times_start[end_tile]

    cheat_count = 0
    pairs = all_pairs_of_free_space_at_most_length_apart(map, cheat_length)
    for (i1, j1), (i2, j2) in pairs:
        time = (
            times_start[(i1, j1)]
            + taxicab_distance(i1, j1, i2, j2)
            + times_end[(i2, j2)]
        )
        if baseline - time >= min_time_save:
            cheat_count += 1
    return cheat_count


def run_program(input, cheat_length=20, min_time_save=100):
    map = parse_input(input)
    return get_cheat_count_to_finish_race_and_save_time(
        map, cheat_length, min_time_save
    )


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            ###############
            #...#...#.....#
            #.#.#.#.#.###.#
            #S#...#.#.#...#
            #######.#.#.###
            #######.#.#...#
            #######.#.###.#
            ###..E#...#...#
            ###.#######.###
            #...###...#...#
            #.#####.#.###.#
            #.#...#.#.#...#
            #.#.#.#.#.#.###
            #...#...#...###
            ###############
            """
        )

        self.assertEqual(run_program(input, min_time_save=80), 0)
        self.assertEqual(run_program(input, min_time_save=76), 3)
        self.assertEqual(run_program(input, min_time_save=74), 7)
        self.assertEqual(run_program(input, min_time_save=72), 29)
        self.assertEqual(run_program(input, min_time_save=70), 41)
        self.assertEqual(run_program(input, min_time_save=68), 55)
        self.assertEqual(run_program(input, min_time_save=66), 67)
        self.assertEqual(run_program(input, min_time_save=64), 86)
        self.assertEqual(run_program(input, min_time_save=50), 285)
