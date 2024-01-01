#
# Advent of Code 2023, day 10
#

import copy
import textwrap
import unittest


def read_input():
    with open('input.txt', encoding='utf-8') as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split('\n')]


def pretty_print_grid(grid):
    for line in grid:
        print(''.join(line))
    print()


def get_number_of_tiles_enclosed_by_loop(grid):
    # Let me give an overview of the solution as the approach is non-trivial:
    #
    # 1. We need to find the starting position and replace its tile with
    #    a proper pipe. This replacement is needed in the following step.
    # 2. Expand the grid by replacing each tile with a 3x3 matrix. This
    #    simplifies the flood-fill algorithm in the fourth step.
    # 3. Find the loop and change all its tiles to a dedicated character ('#').
    # 4. Replace all tiles that are not part of the loop with the ground tile
    #    ('.'). The reason is that all non-'#' tiles act as ground.
    # 5. Use the flood-fill algorithm to replace all ground tiles outside the
    #    loop with a space (' '). Begin in the top-left corner, which, by step
    #    2, is guaranteed to be ground outside of the loop.
    # 6. Count the ground tiles in the expanded grid by counting the number of
    #    3x3 matrices composed entirely of '.'.
    #
    start_position = find_start_position(grid)
    grid = replace_start_position_with_pipe(start_position, grid)
    start_position, grid = expand_grid(start_position, grid)
    grid = find_and_mark_loop(start_position, grid)
    grid = mark_non_loop_tiles(grid)
    grid = flood_grid(grid)
    return count_ground_tiles_in_expanded_grid(grid)


def find_start_position(grid):
    for i, line in enumerate(grid):
        for j, pipe in enumerate(line):
            if pipe == 'S':
                return i, j


def replace_start_position_with_pipe(start_position, grid):
    # Replace the start position ('S') with a proper pipe, depending on which
    # pipe fits there.
    new_grid = copy.deepcopy(grid)

    i, j = start_position
    if grid[i - 1][j] in ['|', '7', 'F'] and grid[i + 1][j] in ['|', 'L', 'J']:
        new_grid[i][j] = '|'
    elif grid[i][j - 1] in ['-', 'L', 'F'] and grid[i][j + 1] in ['-', 'J', '7']:
        new_grid[i][j] = '-'
    elif grid[i - 1][j] in ['|', '7', 'F'] and grid[i][j + 1] in ['-', 'J', '7']:
        new_grid[i][j] = 'L'
    elif grid[i - 1][j] in ['|', '7', 'F'] and grid[i][j - 1] in ['-', 'L', 'F']:
        new_grid[i][j] = 'J'
    elif grid[i][j - 1] in ['-', 'L', 'F'] and grid[i + 1][j] in ['|', 'L', 'J']:
        new_grid[i][j] = '7'
    else:
        new_grid[i][j] = 'F'

    return new_grid


def expand_grid(start_position, grid):
    # Replace each tile in the grid with a 3x3 matrix. This simplifies the
    # flood-fill algorithm as pipes might touch each other.
    new_start_position = start_position[0] * 3 + 1, start_position[1] * 3 + 1
    new_grid = []

    for line in grid:
        new_lines = []
        for c in line:
            if c == '-':
                new_lines.append(
                    [
                        ['.', '.', '.'],
                        ['-', '-', '-'],
                        ['.', '.', '.'],
                    ]
                )
            elif c == '|':
                new_lines.append(
                    [
                        ['.', '|', '.'],
                        ['.', '|', '.'],
                        ['.', '|', '.'],
                    ]
                )
            elif c == 'L':
                new_lines.append(
                    [
                        ['.', '|', '.'],
                        ['.', 'L', '-'],
                        ['.', '.', '.'],
                    ]
                )
            elif c == 'J':
                new_lines.append(
                    [
                        ['.', '|', '.'],
                        ['-', 'J', '.'],
                        ['.', '.', '.'],
                    ]
                )
            elif c == '7':
                new_lines.append(
                    [
                        ['.', '.', '.'],
                        ['-', '7', '.'],
                        ['.', '|', '.'],
                    ]
                )
            elif c == 'F':
                new_lines.append(
                    [
                        ['.', '.', '.'],
                        ['.', 'F', '-'],
                        ['.', '|', '.'],
                    ]
                )
            else:
                new_lines.append(
                    [
                        ['.', '.', '.'],
                        ['.', '.', '.'],
                        ['.', '.', '.'],
                    ]
                )
        for i in [0, 1, 2]:
            new_line = []
            for lines in new_lines:
                new_line.extend(lines[i])
            new_grid.append(new_line)

    return new_start_position, new_grid


def find_and_mark_loop(start_position, grid):
    # Do a breath-first search from the starting position ('S') to find the
    # loop and replace all its characters with '#'. Depth-first search would
    # also work here.
    new_grid = copy.deepcopy(grid)

    visited_positions = set()
    positions_to_check = [start_position]
    while positions_to_check:
        current_position = positions_to_check.pop(0)
        visited_positions.add(current_position)
        new_grid[current_position[0]][current_position[1]] = '#'
        for position in get_next_positions(current_position, grid):
            if position not in visited_positions:
                positions_to_check.append(position)

    return new_grid


def get_next_positions(current_position, grid):
    # Based on the pipe at the current position in the grid, return the two
    # positions that connect to the pipe.
    i, j = current_position
    next_positions_for_pipe = {
        '|': [(i - 1, j), (i + 1, j)],
        '-': [(i, j - 1), (i, j + 1)],
        'L': [(i - 1, j), (i, j + 1)],
        'J': [(i - 1, j), (i, j - 1)],
        '7': [(i, j - 1), (i + 1, j)],
        'F': [(i, j + 1), (i + 1, j)],
    }
    return next_positions_for_pipe[grid[i][j]]


def mark_non_loop_tiles(grid):
    # Go over the grid and replace all tiles that are not part of the loop
    # with '.'. This simplifies the next steps.
    new_grid = copy.deepcopy(grid)

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != '#':
                new_grid[i][j] = '.'

    return new_grid


def flood_grid(grid):
    # Do a flood fill over the grid (https://en.wikipedia.org/wiki/Flood_fill),
    # replacing ground tiles ('.') with ' '.
    new_grid = copy.deepcopy(grid)

    positions_to_flood = [(0, 0)]
    while positions_to_flood:
        i, j = positions_to_flood.pop()
        new_grid[i][j] = ' '
        neighbors = [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]
        for x, y in neighbors:
            if (
                0 <= x < len(new_grid)
                and 0 <= y < len(new_grid[i])
                and new_grid[x][y] == '.'
            ):
                positions_to_flood.append((x, y))

    return new_grid


def count_ground_tiles_in_expanded_grid(grid):
    # Count the number of ground tiles in the expanded grid. A single ground
    # tile in the original grid is represented by nine groud tiles in the
    # expanded grid. Therefore, count all occurrences of a 3x3 '.' matrix.
    ground_tile_count = 0

    marked_grid = copy.deepcopy(grid)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            expanded_ground_positions = [
                (i, j),
                (i, j + 1),
                (i, j + 2),
                (i + 1, j),
                (i + 1, j + 1),
                (i + 1, j + 2),
                (i + 2, j),
                (i + 2, j + 1),
                (i + 2, j + 2),
            ]
            for x, y in expanded_ground_positions:
                if (
                    x >= len(marked_grid)
                    or y >= len(marked_grid[i])
                    or marked_grid[x][y] != '.'
                ):
                    break
            else:  # nobreak
                ground_tile_count += 1
                for x, y in expanded_ground_positions:
                    marked_grid[x][y] = 'x'

    return ground_tile_count


def run_program(input):
    grid = parse_input(input)
    return get_number_of_tiles_enclosed_by_loop(grid)


if __name__ == '__main__':
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_first_example_input(self):
        input = textwrap.dedent(
            """
            ...........
            .S-------7.
            .|F-----7|.
            .||.....||.
            .||.....||.
            .|L-7.F-J|.
            .|..|.|..|.
            .L--J.L--J.
            ...........
            """
        )

        result = run_program(input)

        self.assertEqual(result, 4)

    def test_program_returns_correct_result_for_second_example_input(self):
        input = textwrap.dedent(
            """
            ..........
            .S------7.
            .|F----7|.
            .||....||.
            .||....||.
            .|L-7F-J|.
            .|..||..|.
            .L--JL--J.
            ..........
            """
        )

        result = run_program(input)

        self.assertEqual(result, 4)

    def test_program_returns_correct_result_for_third_example_input(self):
        input = textwrap.dedent(
            """
            .F----7F7F7F7F-7....
            .|F--7||||||||FJ....
            .||.FJ||||||||L7....
            FJL7L7LJLJ||LJ.L-7..
            L--J.L7...LJS7F-7L7.
            ....F-J..F7FJ|L7L7L7
            ....L7.F7||L7|.L7L7|
            .....|FJLJ|FJ|F7|.LJ
            ....FJL-7.||.||||...
            ....L---J.LJ.LJLJ...
            """
        )

        result = run_program(input)

        self.assertEqual(result, 8)

    def test_program_returns_correct_result_for_fourth_example_input(self):
        input = textwrap.dedent(
            """
            FF7FSF7F7F7F7F7F---7
            L|LJ||||||||||||F--J
            FL-7LJLJ||||||LJL-77
            F--JF--7||LJLJ7F7FJ-
            L---JF-JLJ.||-FJLJJ7
            |F|F-JF---7F7-L7L|7|
            |FFJF7L7F-JF7|JL---7
            7-L-JL7||F7|L7F-7F7|
            L.L7LFJ|||||FJL7||LJ
            L7JLJL-JLJLJL--JLJ.L
            """
        )

        result = run_program(input)

        self.assertEqual(result, 10)
