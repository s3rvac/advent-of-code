#
# Advent of Code 2023, day 24 (part 1 only)
#

import dataclasses
import itertools
import textwrap
import unittest


@dataclasses.dataclass
class Hailstone:
    px: int
    py: int
    pz: int
    vx: int
    vy: int
    vz: int

    @classmethod
    def from_str(cls, s):
        position, velocity = s.split(' @ ')
        px, py, pz = position.split(', ')
        vx, vy, vz = velocity.split(', ')
        return cls(int(px), int(py), int(pz), int(vx), int(vy), int(vz))


def read_input():
    with open('input.txt', encoding='utf-8') as f:
        return f.read()


def parse_input(input):
    return [Hailstone.from_str(line.strip()) for line in input.strip().split('\n')]


def count_intersections(hailstones, min_xy, max_xy):
    return sum(
        do_hailstones_intersect(h1, h2, min_xy, max_xy)
        for h1, h2 in itertools.combinations(hailstones, 2)
    )


def do_hailstones_intersect(h1, h2, min_xy, max_xy):
    # Compute the intersection of two lines defined by the two hailstones. Each
    # line is represented by two points (the original position of the hailstone
    # and the position after one nanosecond).
    # Based on https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
    x1, y1, x2, y2 = h1.px, h1.py, h1.px + h1.vx, h1.py + h1.vy
    x3, y3, x4, y4 = h2.px, h2.py, h2.px + h2.vx, h2.py + h2.vy

    px_nominator = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    px_denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    py_nominator = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
    py_denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if px_denominator == 0 or py_denominator == 0:
        # The two lines are parallel or coincident.
        return False

    px = px_nominator / px_denominator
    py = py_nominator / py_denominator

    if px < min_xy or px > max_xy or py < min_xy or py > max_xy:
        # The two lines intersect outside of the test area.
        return False
    elif (
        (px > h1.px and h1.vx < 0)
        or (px < h1.px and h1.vx > 0)
        or (px > h2.px and h2.vx < 0)
        or (px < h2.px and h2.vx > 0)
    ):
        # The two lines intersect in the past.
        return False

    # The two lines interesect in the test area in the future.
    return True


def run_program(input, min_xy, max_xy):
    hailstones = parse_input(input)
    return count_intersections(hailstones, min_xy, max_xy)


if __name__ == '__main__':
    result = run_program(read_input(), min_xy=200000000000000, max_xy=400000000000000)
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            19, 13, 30 @ -2,  1, -2
            18, 19, 22 @ -1, -1, -2
            20, 25, 34 @ -2, -2, -4
            12, 31, 28 @ -1, -2, -1
            20, 19, 15 @  1, -5, -3
            """
        )

        result = run_program(input, min_xy=7, max_xy=27)

        self.assertEqual(result, 2)
