#
# Advent of Code 2023, day 16, part 2
#

import dataclasses
import textwrap
import unittest


@dataclasses.dataclass(frozen=True)
class Beam:
    x: int
    y: int
    dx: int
    dy: int


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split("\n")]


def count_max_energized_tiles(contraption):
    return max(
        count_energized_tiles_from_start_beam(contraption, start_beam=beam)
        for beam in gen_possible_start_beams(contraption)
    )


def gen_possible_start_beams(contraption):
    row_count = len(contraption)
    col_count = len(contraption[0])

    # Top edge:
    for y in range(col_count):
        yield Beam(0, y, +1, 0)

    # Bottom edge:
    for y in range(col_count):
        yield Beam(row_count - 1, y, -1, 0)

    # Left edge:
    for x in range(row_count):
        yield Beam(x, 0, 0, +1)

    # Right edge:
    for x in range(row_count):
        yield Beam(x, col_count - 1, 0, -1)


def count_energized_tiles_from_start_beam(contraption, start_beam):
    def is_in_bounds(beam):
        return 0 <= beam.x < len(contraption) and 0 <= beam.y < len(contraption[beam.x])

    # We keep iterating until we cover all the possible paths in the
    # contraption. Then, the we get the number of energized tiles from the set
    # of beams that we have visited.
    visited_beams = set()
    beams = [start_beam]
    while beams:
        beam = beams.pop()
        if beam not in visited_beams and is_in_bounds(beam):
            visited_beams.add(beam)
            beams.extend(get_next_beams(beam, contraption))

    return len({(beam.x, beam.y) for beam in visited_beams})


def get_next_beams(beam, contraption):
    match contraption[beam.x][beam.y]:
        case ".":
            return [
                Beam(
                    beam.x + beam.dx,
                    beam.y + beam.dy,
                    beam.dx,
                    beam.dy,
                )
            ]
        case "\\":
            if beam.dx == 0 and beam.dy == +1:
                return [Beam(beam.x + 1, beam.y, +1, 0)]
            elif beam.dx == 0 and beam.dy == -1:
                return [Beam(beam.x - 1, beam.y, -1, 0)]
            elif beam.dx == -1 and beam.dy == 0:
                return [Beam(beam.x, beam.y - 1, 0, -1)]
            elif beam.dx == +1 and beam.dy == 0:
                return [Beam(beam.x, beam.y + 1, 0, +1)]
        case "/":
            if beam.dx == 0 and beam.dy == +1:
                return [Beam(beam.x - 1, beam.y, -1, 0)]
            elif beam.dx == 0 and beam.dy == -1:
                return [Beam(beam.x + 1, beam.y, +1, 0)]
            elif beam.dx == -1 and beam.dy == 0:
                return [Beam(beam.x, beam.y + 1, 0, +1)]
            elif beam.dx == +1 and beam.dy == 0:
                return [Beam(beam.x, beam.y - 1, 0, -1)]
        case "|":
            if beam.dy == 0:
                return [Beam(beam.x + beam.dx, beam.y, beam.dx, 0)]
            else:
                return [
                    Beam(beam.x - 1, beam.y, -1, 0),
                    Beam(beam.x + 1, beam.y, +1, 0),
                ]
        case "-":
            if beam.dx == 0:
                return [Beam(beam.x, beam.y + beam.dy, 0, beam.dy)]
            else:
                return [
                    Beam(beam.x, beam.y - 1, 0, -1),
                    Beam(beam.x, beam.y + 1, 0, +1),
                ]
    raise AssertionError("unhandled move in get_next_beams()")


def run_program(input):
    contraption = parse_input(input)
    return count_max_energized_tiles(contraption)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            r"""
            .|...\....
            |.-.\.....
            .....|-...
            ........|.
            ..........
            .........\
            ..../.\\..
            .-.-/..|..
            .|....-|.\
            ..//.|....
            """
        )

        result = run_program(input)

        self.assertEqual(result, 51)
