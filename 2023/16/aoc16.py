#
# Advent of Code 2023, day 16
#

import dataclasses
import textwrap
import unittest


@dataclasses.dataclass(frozen=True)
class Beam:
    pos_x: int
    pos_y: int
    dir_x: int
    dir_y: int


def read_input():
    with open('input.txt', encoding='utf-8') as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split('\n')]


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
    # The gist is that we create a copy of the contraption composed of 0s (not
    # energized) and 1s (energized), and then do a depth-first search
    # (breadth-first search would work as well) until we cover all the possible
    # paths in the contraption.
    is_energized_grid = [list(0 for _ in range(len(row))) for row in contraption]

    beams = [start_beam]
    checked_beams = set()
    while beams:
        beam = beams.pop()
        if beam in checked_beams or is_beam_out_of_bounds(beam, contraption):
            continue

        checked_beams.add(beam)
        is_energized_grid[beam.pos_x][beam.pos_y] = 1
        next_beams = get_next_beams(beam, contraption)
        beams.extend(next_beams)

    return sum(sum(row) for row in is_energized_grid)


def is_beam_out_of_bounds(beam, contraption):
    return (
        beam.pos_x < 0
        or beam.pos_x >= len(contraption)
        or beam.pos_y < 0
        or beam.pos_y >= len(contraption[0])
    )


def get_next_beams(beam, contraption):
    tile = contraption[beam.pos_x][beam.pos_y]
    if tile == '.':
        return [
            Beam(
                beam.pos_x + beam.dir_x,
                beam.pos_y + beam.dir_y,
                beam.dir_x,
                beam.dir_y,
            )
        ]
    elif tile == '\\':
        if beam.dir_x == 0 and beam.dir_y == +1:
            return [Beam(beam.pos_x + 1, beam.pos_y, +1, 0)]
        elif beam.dir_x == 0 and beam.dir_y == -1:
            return [Beam(beam.pos_x - 1, beam.pos_y, -1, 0)]
        elif beam.dir_x == -1 and beam.dir_y == 0:
            return [Beam(beam.pos_x, beam.pos_y - 1, 0, -1)]
        elif beam.dir_x == +1 and beam.dir_y == 0:
            return [Beam(beam.pos_x, beam.pos_y + 1, 0, +1)]
    elif tile == '/':
        if beam.dir_x == 0 and beam.dir_y == +1:
            return [Beam(beam.pos_x - 1, beam.pos_y, -1, 0)]
        elif beam.dir_x == 0 and beam.dir_y == -1:
            return [Beam(beam.pos_x + 1, beam.pos_y, +1, 0)]
        elif beam.dir_x == -1 and beam.dir_y == 0:
            return [Beam(beam.pos_x, beam.pos_y + 1, 0, +1)]
        elif beam.dir_x == +1 and beam.dir_y == 0:
            return [Beam(beam.pos_x, beam.pos_y - 1, 0, -1)]
    elif tile == '|':
        if beam.dir_y == 0:
            return [Beam(beam.pos_x + beam.dir_x, beam.pos_y, beam.dir_x, 0)]
        else:
            return [
                Beam(beam.pos_x - 1, beam.pos_y, -1, 0),
                Beam(beam.pos_x + 1, beam.pos_y, +1, 0),
            ]
    elif tile == '-':
        if beam.dir_x == 0:
            return [Beam(beam.pos_x, beam.pos_y + beam.dir_y, 0, beam.dir_y)]
        else:
            return [
                Beam(beam.pos_x, beam.pos_y - 1, 0, -1),
                Beam(beam.pos_x, beam.pos_y + 1, 0, +1),
            ]


def run_program(input):
    contraption = parse_input(input)
    return count_max_energized_tiles(contraption)


if __name__ == '__main__':
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
