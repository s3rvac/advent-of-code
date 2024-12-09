#
# Advent of Code 2024, day 09, part 1
#

import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    # Parses the input raw disk map, e.g.
    #
    #     12345
    #
    # to a representation suitable for further processing, where each position
    # is either the ID of the file or `None` (free space), e.g.
    #
    #     [0, None, None, 1, 1, 1, None, None, None, None, 2, 2, 2, 2, 2]
    #
    # See the assignment for more details.
    id = 0
    parse_next_as_file = True

    def parse_char(c):
        nonlocal id, parse_next_as_file
        if parse_next_as_file:
            result = [id] * int(c)
            id += 1
        else:
            result = [None] * int(c)
        parse_next_as_file = not parse_next_as_file
        return result

    disk_map = []
    for c in input.strip():
        disk_map.extend(parse_char(c))
    return disk_map


def compact_disk(disk_map):
    for i in range(len(disk_map) - 1, -1, -1):
        if disk_map[i] is not None:
            j = disk_map.index(None)
            if j >= i:
                break
            disk_map[j], disk_map[i] = disk_map[i], None


def compute_disk_checksum(disk_map):
    return sum(i * id for i, id in enumerate(disk_map) if id is not None)


def run_program(input):
    disk_map = parse_input(input)
    compact_disk(disk_map)
    return compute_disk_checksum(disk_map)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_parse_input_returns_correct_value(self):
        self.assertEqual(
            parse_input("12345"),
            [0, None, None, 1, 1, 1, None, None, None, None, 2, 2, 2, 2, 2],
        )

    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            2333133121414131402
            """
        )

        result = run_program(input)

        self.assertEqual(result, 1928)
