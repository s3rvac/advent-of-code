#
# Advent of Code 2024, day 14, part 1
#

import dataclasses
import math
import re
import textwrap
import unittest


@dataclasses.dataclass
class Robot:
    px: int
    py: int
    vx: int
    vy: int


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    def parse_line(line):
        m = re.fullmatch(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line)
        assert m is not None, line
        return Robot(
            px=int(m.group(1)),
            py=int(m.group(2)),
            vx=int(m.group(3)),
            vy=int(m.group(4)),
        )

    return [parse_line(line) for line in input.strip().split("\n")]


def simulate_robots_in_area(robots, area_width, area_height, seconds):
    def compute_new_position(p, v, size):
        new = p + v
        if new < 0:
            new = size + new
        elif new >= size:
            new = new - size
        return new

    for _ in range(seconds):
        for robot in robots:
            robot.px = compute_new_position(robot.px, robot.vx, area_width)
            robot.py = compute_new_position(robot.py, robot.vy, area_height)


def compute_safety_factor(robots, area_width, area_height):
    middle_width = area_width // 2
    middle_height = area_height // 2

    quadrant_counts = [0, 0, 0, 0]
    for robot in robots:
        if robot.px < middle_width and robot.py < middle_height:
            quadrant_counts[0] += 1
        elif robot.px > middle_width and robot.py < middle_height:
            quadrant_counts[1] += 1
        elif robot.px < middle_width and robot.py > middle_height:
            quadrant_counts[2] += 1
        elif robot.px > middle_width and robot.py > middle_height:
            quadrant_counts[3] += 1
    return math.prod(quadrant_counts)


def run_program(input, area_width=101, area_height=103, seconds=100):
    robots = parse_input(input)
    simulate_robots_in_area(robots, area_width, area_height, seconds)
    return compute_safety_factor(robots, area_width, area_height)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            p=0,4 v=3,-3
            p=6,3 v=-1,-3
            p=10,3 v=-1,2
            p=2,0 v=2,-1
            p=0,0 v=1,3
            p=3,0 v=-2,-2
            p=7,6 v=-1,-3
            p=3,0 v=-1,-2
            p=9,3 v=2,3
            p=7,3 v=-1,2
            p=2,4 v=2,-3
            p=9,5 v=-3,-3
            """
        )

        result = run_program(input, area_width=11, area_height=7)

        self.assertEqual(result, 12)
