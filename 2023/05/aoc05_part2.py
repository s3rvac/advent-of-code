#
# Advent of Code 2023, day 05, part 2
#
# Note: Although the script is slow, it does the job.
#

import re
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    # Append an empty line to simplify the loop below (it will always end with
    # appending the map):
    lines = input.strip().split("\n") + [""]

    m = re.fullmatch("seeds: (.+)", lines[0])
    assert m is not None
    raw_seeds = m.group(1).split(" ")
    seed_ranges = [
        (int(start), int(length))
        for start, length in zip(raw_seeds[::2], raw_seeds[1::2])
    ]

    maps = []
    for line in lines[2:]:
        if m := re.fullmatch(r"(.+)-to-(.+) map:", line):
            map = {
                "from": m.group(1),
                "to": m.group(2),
                "ranges": [],
            }
        elif line:
            dst, src, range = line.split(" ")
            map["ranges"].append((int(dst), int(src), int(range)))
        else:
            maps.append(map)

    return {
        "seed_ranges": seed_ranges,
        "maps": maps,
    }


def get_min_location_from_alamac(almanac):
    # We need to work with whole ranges as working with standalone seeds would
    # be too slow and inefficient.
    def map_ranges(ranges, mappings):
        remaining = ranges
        mapped = []
        for dst, src, length in mappings:
            new_remaining = []
            for start, end in remaining:
                # No overlap:
                # [....]
                #        [....]
                # or
                #        [....]
                # [....]
                if src + length < start or src > end:
                    new_remaining.append((start, end))
                # Overlap of the whole range:
                # [...........]
                #    [.....]
                elif src <= start < src + length and src <= end < src + length:
                    mapped.append((dst + start - src, dst + end - src))
                # Overlap in the beginning of the range:
                #    [......]
                # [.....]
                elif src <= end < src + length:
                    mapped.append((dst, dst + end - src))
                    new_remaining.append((start, src - 1))
                # Overlap in the ending of the range:
                #    [......]
                #        [.....]
                else:
                    mapped.append((dst + start - src, dst + length))
                    new_remaining.append((src + length, end))
            remaining = new_remaining

        return mapped + remaining

    ranges = [(start, start + length - 1) for start, length in almanac["seed_ranges"]]

    # The maps are ordered in a correct way, e.g. seed-soil,
    # soil-fertilizer, etc.
    for map in almanac["maps"]:
        ranges = map_ranges(ranges, map["ranges"])

    return min(range[0] for range in ranges)


def run_program(input):
    almanac = parse_input(input)
    return get_min_location_from_alamac(almanac)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            seeds: 79 14 55 13

            seed-to-soil map:
            50 98 2
            52 50 48

            soil-to-fertilizer map:
            0 15 37
            37 52 2
            39 0 15

            fertilizer-to-water map:
            49 53 8
            0 11 42
            42 0 7
            57 7 4

            water-to-light map:
            88 18 7
            18 25 70

            light-to-temperature map:
            45 77 23
            81 45 19
            68 64 13

            temperature-to-humidity map:
            0 69 1
            1 0 69

            humidity-to-location map:
            60 56 37
            56 93 4
            """
        )

        result = run_program(input)

        self.assertEqual(result, 46)
