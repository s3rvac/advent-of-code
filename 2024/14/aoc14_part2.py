#
# Advent of Code 2024, day 14, part 2
#

import collections
import dataclasses
import re


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


def print_robots_in_area(robots, area_width, area_height):
    robots_per_position = collections.Counter(
        {(robot.px, robot.py): 1 for robot in robots}
    )

    for y in range(area_height):
        for x in range(area_width):
            count = robots_per_position[(x, y)]
            print("." if count == 0 else str(count), end="")
        print()


def compute_seconds_needed_for_easter_egg(robots, area_width, area_height):
    def compute_new_position(p, v, size):
        new = p + v
        if new < 0:
            new = size + new
        elif new >= size:
            new = new - size
        return new

    # When working on the puzzle, I had no idea what to look for, so I tried
    # simulating the movement while continually printing the area into the
    # terminal and checking if it resembles the tree. Then, I have found that
    # when the tree is shown, each robot is at a unique position, which gave
    # me the end condition for the loop.
    seconds = 0
    while True:
        occupied_positions = set()
        for robot in robots:
            robot.px = compute_new_position(robot.px, robot.vx, area_width)
            robot.py = compute_new_position(robot.py, robot.vy, area_height)
            occupied_positions.add((robot.px, robot.py))
        seconds += 1
        if len(occupied_positions) == len(robots):
            print_robots_in_area(robots, area_width, area_height)
            return seconds


def run_program(input, area_width=101, area_height=103):
    robots = parse_input(input)
    return compute_seconds_needed_for_easter_egg(robots, area_width, area_height)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)
