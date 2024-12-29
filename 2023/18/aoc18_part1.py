#
# Advent of Code 2023, day 18, part 1
#

import textwrap
import unittest
import dataclasses


@dataclasses.dataclass
class DigInstruction:
    direction: str
    distance: int
    color: str


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    def parse_dig_instruction(line):
        # Example line: R 6 (#70c710)
        direction, distance, color = line.split(" ")
        return DigInstruction(
            direction=direction,
            distance=int(distance),
            color=color[1:-1],
        )

    return [parse_dig_instruction(line) for line in input.strip().split("\n")]


def dig_according_to_plan(dig_plan):
    def extend_map_with_terrain_if_needed():
        nonlocal map, i, j

        new_map = map
        if i == -1:
            i += 1
            new_map = [list("." * len(map[0]))] + map
        elif i == len(map):
            new_map = map + [list("." * len(map[0]))]
        elif j == -1:
            j += 1
            new_map = []
            for row in map:
                new_map.append(["."] + row)
        elif j == len(map[0]):
            new_map = []
            for row in map:
                new_map.append(row + ["."])
        map = new_map

    map = [["#"]]
    i, j = 0, 0
    for instr in dig_plan:
        for _ in range(instr.distance):
            if instr.direction == "R":
                j += 1
            elif instr.direction == "L":
                j -= 1
            elif instr.direction == "U":
                i -= 1
            elif instr.direction == "D":
                i += 1
            extend_map_with_terrain_if_needed()
            map[i][j] = "#"

    return map


def dig_interior(map):
    for row in map:
        for i in range(len(row)):
            if row[i] == ".":
                row[i] = "?"

    queue = set()
    visited = set()
    for i in range(len(map)):
        queue.add((i, 0))
        queue.add((i, len(map[0]) - 1))
    for j in range(len(map[0])):
        queue.add((0, j))
        queue.add((len(map) - 1, j))
    while queue:
        i, j = queue.pop()
        if (i, j) in visited or i < 0 or j < 0 or i >= len(map) or j >= len(map[0]):
            continue
        visited.add((i, j))
        if map[i][j] == "?":
            map[i][j] = "."
            queue.add((i - 1, j))
            queue.add((i, j - 1))
            queue.add((i, j + 1))
            queue.add((i + 1, j))

    for row in map:
        for i in range(len(row)):
            if row[i] == "?":
                row[i] = "#"

    return map


def count_dug_out_cells(map):
    count = 0
    for row in map:
        count += row.count("#")
    return count


def run_program(input):
    dig_plan = parse_input(input)
    map = dig_according_to_plan(dig_plan)
    map = dig_interior(map)
    return count_dug_out_cells(map)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            R 6 (#70c710)
            D 5 (#0dc571)
            L 2 (#5713f0)
            D 2 (#d2c081)
            R 2 (#59c680)
            D 2 (#411b91)
            L 5 (#8ceee2)
            U 2 (#caa173)
            L 1 (#1b58a2)
            U 2 (#caa171)
            R 2 (#7807d2)
            U 3 (#a77fa3)
            L 2 (#015232)
            U 2 (#7a21e3)
            """
        )

        result = run_program(input)

        self.assertEqual(result, 62)
