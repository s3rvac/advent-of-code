#
# Advent of Code 2024, day 09, part 2
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
    # Pre-compute a mapping of file IDs to their start and end indexes to
    # speedup the compaction.
    #
    # Index intervals are half-open, i.e. (i, j) means <i, j); that is, all
    # indexes on i, i + 1, ..., up to j - 1.
    file_id_to_block_range = {}
    file_id = 0
    file_start = None
    for i in range(len(disk_map)):
        if disk_map[i] == file_id:
            if file_start is None:
                file_start = i
        elif file_start is not None:
            file_id_to_block_range[file_id] = (file_start, i)
            file_id += 1
            file_start = i if disk_map[i] == file_id else None
    if file_start is not None:
        file_id_to_block_range[file_id] = (file_start, len(disk_map))

    def get_first_free_blocks_of_size(size):
        for i in range(len(disk_map)):
            consecutive_free = 0
            if disk_map[i] is None:
                for j in range(i, len(disk_map)):
                    if disk_map[j] is not None:
                        break
                    consecutive_free += 1
                    if consecutive_free == size:
                        return i, i + size
        return None, None

    def swap_blocks(file_start, file_end, free_start, _):
        for i in range(file_end - file_start):
            disk_map[free_start + i], disk_map[file_start + i] = (
                disk_map[file_start + i],
                disk_map[free_start + i],
            )

    # Try compacting files one be one, starting with the highest ID.
    file_id = max(file_id_to_block_range)
    while file_id > 0:
        file_start, file_end = file_id_to_block_range[file_id]
        free_start, free_end = get_first_free_blocks_of_size(file_end - file_start)
        if free_start is not None and free_end <= file_start:
            swap_blocks(file_start, file_end, free_start, free_end)
        file_id -= 1


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

        self.assertEqual(result, 2858)
