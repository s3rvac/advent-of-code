#
# Advent of Code 2023, day 22, part 2
#

import dataclasses
import textwrap
import unittest


@dataclasses.dataclass(frozen=True)
class Brick:
    x1: int
    y1: int
    z1: int
    x2: int
    y2: int
    z2: int

    @classmethod
    def from_string(cls, s):
        def parse_coords(coords):
            return tuple(int(x) for x in coords.split(","))

        first, second = s.split("~")
        return cls(*parse_coords(first), *parse_coords(second))

    def moved_down(self):
        return Brick(self.x1, self.y1, self.z1 - 1, self.x2, self.y2, self.z2 - 1)

    def is_above_ground(self):
        return self.z1 > 0 and self.z2 > 0

    @staticmethod
    def ranges_overlap(x_start, x_end, y_start, y_end):
        return max(x_start, y_start) <= min(x_end, y_end)

    def collides_with(self, other):
        return (
            self.ranges_overlap(self.x1, self.x2, other.x1, other.x2)
            and self.ranges_overlap(self.y1, self.y2, other.y1, other.y2)
            and self.ranges_overlap(self.z1, self.z2, other.z1, other.z2)
        )


class Bricks(list):
    def without_brick(self, brick):
        i = self.index(brick)
        return Bricks(self[:i] + self[i + 1 :])

    def order_by_z(self):
        return self.sort(key=lambda brick: brick.z1)


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return Bricks(Brick.from_string(line) for line in input.strip().split("\n"))


def try_moving_brick_down(brick, i, bricks):
    while True:
        new_brick = brick.moved_down()
        if not new_brick.is_above_ground():
            return brick
        for j, other in enumerate(bricks):
            if i != j and new_brick.collides_with(other):
                return brick
        brick = new_brick


def stabilize_bricks(bricks):
    # By ordering the bricks by their z coordinates, we can speedup the
    # computation as we can just checks the bricks one by one, without a need
    # of returning to an already positioned brick.
    bricks.order_by_z()

    fallen_brick_ids = set()
    for i, brick in enumerate(bricks):
        if new_brick := try_moving_brick_down(brick, i, bricks):
            if new_brick != brick:
                bricks[i] = new_brick
                fallen_brick_ids.add(i)
    return len(fallen_brick_ids)


def count_bricks_that_would_fall_after_disintegrating_brick(brick, bricks):
    new_bricks = bricks.without_brick(brick)
    fallen_brick_count = stabilize_bricks(new_bricks)
    return fallen_brick_count


def count_bricks_that_would_fall_after_disintegrating_one_brick_at_a_time(bricks):
    return sum(
        count_bricks_that_would_fall_after_disintegrating_brick(brick, bricks)
        for brick in bricks
    )


def run_program(input):
    bricks = parse_input(input)
    stabilize_bricks(bricks)
    return count_bricks_that_would_fall_after_disintegrating_one_brick_at_a_time(bricks)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            1,0,1~1,2,1
            0,0,2~2,0,2
            0,2,3~2,2,3
            0,0,4~0,2,4
            2,0,5~2,2,5
            0,1,6~2,1,6
            1,1,8~1,1,9
            """
        )

        result = run_program(input)

        self.assertEqual(result, 7)
