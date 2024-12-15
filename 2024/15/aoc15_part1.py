#
# Advent of Code 2024, day 15, part 1
#

import textwrap
import unittest


DIRECTIONS_FOR_MOVE = {
    ">": (0, 1),
    "<": (0, -1),
    "v": (1, 0),
    "^": (-1, 0),
}


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    raw_map, raw_movements = input.strip().split("\n\n")
    map = [list(line) for line in raw_map.split("\n")]
    movements = raw_movements.replace("\n", "")
    return map, movements


def find_robot(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == "@":
                return i, j
    raise AssertionError("robot not found")


def move_robot_in_map_according_to_movements(map, movements):
    def swap(i, j, k, l):
        map[i][j], map[k][l] = map[k][l], map[i][j]

    def move_robot(ri, rj, move):
        di, dj = DIRECTIONS_FOR_MOVE[move]

        if map[ri + di][rj + dj] == ".":
            # Move the robot one step.
            swap(ri, rj, ri + di, rj + dj)
            return ri + di, rj + dj

        if map[ri + di][rj + dj] == "O":
            # Check if we can move all the boxes one step.
            xi = ri + di
            xj = rj + dj
            while map[xi][xj] == "O":
                xi += di
                xj += dj
            if map[xi][xj] == ".":
                # Move all the boxes and the robot one step.
                while (xi, xj) != (ri, rj):
                    swap(xi, xj, xi - di, xj - dj)
                    xi -= di
                    xj -= dj
                return ri + di, rj + dj

        return ri, rj

    ri, rj = find_robot(map)
    for move in movements:
        ri, rj = move_robot(ri, rj, move)


def get_gps_coords_of_all_boxes(map):
    coords = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == "O":
                coords.append(100 * i + j)
    return coords


def run_program(input):
    map, movements = parse_input(input)
    move_robot_in_map_according_to_movements(map, movements)
    return sum(get_gps_coords_of_all_boxes(map))


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input1(self):
        input = textwrap.dedent(
            """
            ########
            #..O.O.#
            ##@.O..#
            #...O..#
            #.#.O..#
            #...O..#
            #......#
            ########

            <^^>>>vv<v>>v<<
            """
        )

        result = run_program(input)

        self.assertEqual(result, 2028)

    def test_program_returns_correct_result_for_example_input2(self):
        input = textwrap.dedent(
            """
            ##########
            #..O..O.O#
            #......O.#
            #.OO..O.O#
            #..O@..O.#
            #O#..O...#
            #O..O..O.#
            #.OO.O.OO#
            #....O...#
            ##########

            <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
            vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
            ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
            <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
            ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
            ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
            >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
            <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
            ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
            v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
            """
        )

        result = run_program(input)

        self.assertEqual(result, 10092)
