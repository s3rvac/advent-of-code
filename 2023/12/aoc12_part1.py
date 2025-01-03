#
# Advent of Code 2023, day 12, part 1
#

import dataclasses
import functools
import textwrap
import unittest


@dataclasses.dataclass
class SpringRecord:
    springs: str
    damaged: tuple[int, ...]


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    def parse_spring_record(sr):
        springs, raw_damanged_springs = sr.split()
        damaged = tuple(int(n) for n in raw_damanged_springs.split(","))
        return SpringRecord(springs, damaged)

    return list(map(parse_spring_record, input.strip().split("\n")))


def get_arrangement_counts(spring_records):
    return list(map(get_arrangement_count, spring_records))


def get_arrangement_count(spring_record):
    # We employ a recursive approach with caching of intermediary results to
    # speedup the computation.
    @functools.cache
    def get_count(s, d):
        if not d:
            return 1 if s.count("#") == 0 else 0
        elif not s:
            return 0
        elif s[0] == "?":
            return get_count("." + s[1:], d) + get_count("#" + s[1:], d)
        elif s[0] == "#":
            i = 0
            n = d[0]
            while n > 0 and i < len(s) and s[i] in ("#", "?"):
                n -= 1
                i += 1
            if n == 0 and (i == len(s) or s[i] in (".", "?")):
                return get_count(s[i + 1 :], d[1:])
            return 0
        return get_count(s[1:], d)

    return get_count(spring_record.springs, spring_record.damaged)


def run_program(input):
    spring_records = parse_input(input)
    return sum(get_arrangement_counts(spring_records))


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_get_arrangement_count_returns_correct_result(self):
        SR = SpringRecord
        self.assertEqual(get_arrangement_count(SR(".", (1,))), 0)
        self.assertEqual(get_arrangement_count(SR("#", (2,))), 0)
        self.assertEqual(get_arrangement_count(SR("#.#", (2,))), 0)
        self.assertEqual(get_arrangement_count(SR("?", (1,))), 1)
        self.assertEqual(get_arrangement_count(SR("?..", (1,))), 1)
        self.assertEqual(get_arrangement_count(SR("#", (1,))), 1)
        self.assertEqual(get_arrangement_count(SR("#.", (1,))), 1)
        self.assertEqual(get_arrangement_count(SR("#?", (1,))), 1)
        self.assertEqual(get_arrangement_count(SR("#?.", (1,))), 1)
        self.assertEqual(get_arrangement_count(SR("#.#", (1, 1))), 1)
        self.assertEqual(get_arrangement_count(SR("???", (1, 1))), 1)
        self.assertEqual(get_arrangement_count(SR("??", (1,))), 2)
        self.assertEqual(get_arrangement_count(SR("?.?", (1,))), 2)
        self.assertEqual(get_arrangement_count(SR("??.??", (1, 1))), 4)
        self.assertEqual(get_arrangement_count(SR("????", (1,))), 4)
        self.assertEqual(get_arrangement_count(SR("????", (1, 1))), 3)
        self.assertEqual(get_arrangement_count(SR("???.###", (1, 1, 3))), 1)
        self.assertEqual(get_arrangement_count(SR(".??..??...?##.", (1, 1, 3))), 4)
        self.assertEqual(get_arrangement_count(SR("?#?#?#?#?#?#?#?", (1, 3, 1, 6))), 1)
        self.assertEqual(get_arrangement_count(SR("????.#...#...", (4, 1, 1))), 1)
        self.assertEqual(get_arrangement_count(SR("????.######..#####.", (1, 6, 5))), 4)
        self.assertEqual(get_arrangement_count(SR("???????", (2, 1))), 10)
        self.assertEqual(get_arrangement_count(SR("?###????????", (3, 2, 1))), 10)

    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            ???.### 1,1,3
            .??..??...?##. 1,1,3
            ?#?#?#?#?#?#?#? 1,3,1,6
            ????.#...#... 4,1,1
            ????.######..#####. 1,6,5
            ?###???????? 3,2,1
            """
        )

        result = run_program(input)

        self.assertEqual(result, 21)
