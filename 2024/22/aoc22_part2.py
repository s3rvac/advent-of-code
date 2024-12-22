#
# Advent of Code 2024, day 22, part 2
#

import collections
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [int(n) for n in input.strip().split("\n")]


def get_all_evolutions_of_secret_number(n, evolution_count):
    def mix(m, n):
        return m ^ n

    def prune(m):
        return m % 16777216

    evolutions = [n]
    for _ in range(evolution_count):
        n = prune(mix(n, n * 64))
        n = prune(mix(n, n // 32))
        n = prune(mix(n, n * 2048))
        evolutions.append(n)
    return evolutions


def compute_max_bananas_we_can_buy(evolutions_per_number):
    def last_digit(n):
        return n % 10

    def prices_and_changes_for(evolutions):
        return [
            (last_digit(y), last_digit(y) - last_digit(x))
            for x, y in zip(evolutions, evolutions[1:])
        ]

    # We go over evolutions for each number and store the number of bananas
    # that we can buy for each sequence of four changes (as described in the
    # assignment) in a counter. Then, we can easily get the most bananas we can
    # buy by taking the sequence with the most bananas.
    bananas_per_seq = collections.Counter()
    for evolutions in evolutions_per_number:
        # We need to use a separate counter for each number and its
        # evolutions/changes because of the `in` check below.
        local_counter = collections.Counter()
        pcs = prices_and_changes_for(evolutions)
        for a, b, c, d in zip(pcs, pcs[1:], pcs[2:], pcs[3:]):
            seq = (a[1], b[1], c[1], d[1])
            # We can only provide to the monkey the first sequence for each
            # evolution, so use `setdefault()` so that we do not overwrite an
            # existing amount of bananas.
            local_counter.setdefault(seq, d[0])

        for seq, count in local_counter.items():
            bananas_per_seq[seq] += count

    return bananas_per_seq.most_common(1)[0][1]


def run_program(input, evolution_count=2000):
    secret_numbers = parse_input(input)
    evolutions_per_number = [
        get_all_evolutions_of_secret_number(secret_number, evolution_count)
        for secret_number in secret_numbers
    ]
    return compute_max_bananas_we_can_buy(evolutions_per_number)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            1
            2
            3
            2024
            """
        )

        result = run_program(input)

        self.assertEqual(result, 23)
