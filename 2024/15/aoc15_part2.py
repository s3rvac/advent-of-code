#
# Advent of Code 2024, day 15, part 2
#

import copy
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


def scale_map(map):
    new_map = []
    for row in map:
        new_row = []
        for c in row:
            if c == "#":
                new_row.extend(["#", "#"])
            elif c == "O":
                new_row.extend(["[", "]"])
            elif c == ".":
                new_row.extend([".", "."])
            elif c == "@":
                new_row.extend(["@", "."])
        new_map.append(new_row)
    return new_map


def find_robot(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == "@":
                return i, j
    raise AssertionError("robot not found")


def move_robot_in_map_according_to_movements(map, movements):
    def is_empty(i, j):
        return map[i][j] == "."

    def is_box(i, j):
        return map[i][j] in ("[", "]")

    def box_left_coords(i, j):
        return (i, j) if map[i][j] == "[" else (i, j - 1)

    def box_both_coords(i, j):
        return (i, j, i, j + 1) if map[i][j] == "[" else (i, j - 1, i, j)

    def swap(i, j, k, l):
        map[i][j], map[k][l] = map[k][l], map[i][j]

    def move_robot(ri, rj, move):
        di, dj = DIRECTIONS_FOR_MOVE[move]

        if is_empty(ri + di, rj + dj):
            # Move the robot one step.
            swap(ri, rj, ri + di, rj + dj)
            return ri + di, rj + dj

        if is_box(ri + di, rj + dj):
            # Get coordinates of all the boxes in the path via a fixed-point
            # calculation (keep iterating until the set of coordinates is
            # unchanged).
            boxes = {box_left_coords(ri + di, rj + dj)}
            old_boxes = set()
            while boxes != old_boxes:
                old_boxes = copy.copy(boxes)
                for bi, bj in old_boxes:
                    b1i, b1j, b2i, b2j = box_both_coords(bi, bj)
                    if is_box(b1i + di, b1j + dj):
                        boxes.add(box_left_coords(b1i + di, b1j + dj))
                    if is_box(b2i + di, b2j + dj):
                        boxes.add(box_left_coords(b2i + di, b2j + dj))

            # Check if all the boxes are movable; quit if not.
            for bi, bj in boxes:
                b1i, b1j, b2i, b2j = box_both_coords(bi, bj)
                if map[b1i + di][b1j + dj] == "#" or map[b2i + di][b2j + dj] == "#":
                    return ri, rj

            # Move the boxes by swapping them with their neighboring positions.
            # For this to work, we must to start with the outermost boxes and
            # continue towards the most innermost boxes (from the perspective
            # of the robot). Therefore, we need to order the boxes.
            key = lambda x: (-1 if sum([di, dj]) == 1 else 1) * x[abs(dj)]
            for bi, bj in sorted(boxes, key=key):
                b1i, b1j, b2i, b2j = box_both_coords(bi, bj)
                if (di, dj) == (0, 1):
                    swap(b2i, b2j, b2i + di, b2j + dj)
                    swap(b1i, b1j, b1i + di, b1j + dj)
                else:
                    swap(b1i, b1j, b1i + di, b1j + dj)
                    swap(b2i, b2j, b2i + di, b2j + dj)

            # Finally, move the robot.
            swap(ri, rj, ri + di, rj + dj)
            return ri + di, rj + dj

        return ri, rj

    ri, rj = find_robot(map)
    for move in movements:
        ri, rj = move_robot(ri, rj, move)


def get_gps_coords_of_all_boxes(map):
    coords = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == "[":
                coords.append(100 * i + j)
    return coords


def run_program(input):
    map, movements = parse_input(input)
    map = scale_map(map)
    move_robot_in_map_according_to_movements(map, movements)
    return sum(get_gps_coords_of_all_boxes(map))


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
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

        self.assertEqual(result, 9021)
