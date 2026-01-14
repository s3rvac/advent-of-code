#
# Advent of Code 2025, day 12, parts 1 & 2
#
# WARNING: The solution might only work for my input (I do not guarantee that
# it works for every input)!
#

import dataclasses
import re


@dataclasses.dataclass
class Region:
    width: int
    length: int
    present_counts: list[int]

    @property
    def area(self):
        return self.width * self.length


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    def parse_present(raw_present):
        return raw_present.split("\n")[1:]

    def parse_region(raw_region):
        m = re.fullmatch(r"(\d+)x(\d+): (.+)", raw_region)
        assert m is not None, f"Invalid input: {raw_region}"
        return Region(
            width=int(m.group(1)),
            length=int(m.group(2)),
            present_counts=list(map(int, m.group(3).split(" "))),
        )

    parts = input.strip().split("\n\n")
    presents = list(map(parse_present, parts[:-1]))
    regions = list(map(parse_region, parts[-1].split("\n")))
    return presents, regions


def can_presents_fit_into_region(presents, region):
    # While the example input makes the problem really hard, the example input
    # (at least the one I get) is actually trivial to process by just comparing
    # the sum of the total area used by each present with the area of the
    # region. So, instead of trying to solve a very general (and much harder)
    # problem, I opted to solve the one provided in the example input.
    area_per_present = {
        i: sum(line.count("#") for line in present)
        for i, present in enumerate(presents)
    }
    total_used_area = sum(
        area_per_present[i] * count for i, count in enumerate(region.present_counts)
    )
    return total_used_area <= region.area


def run_program(input):
    presents, regions = parse_input(input)
    return sum(can_presents_fit_into_region(presents, region) for region in regions)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)

# Note: There are no tests for the example input as the example input
# represents a much harder problem than the actual input.
