#
# Advent of Code 2023, day 14, part 2
#

import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split("\n")]


def cycle_platform_n_times(platform, n):
    # The gist behind the implementation is that we try to find the period with
    # which the platform configuration repeats itself, and then use this period
    # to dramatically reduce the number of cycles that we need to perform.
    def current_configuration():
        return "".join("".join(row) for row in platform)

    i = 0

    # Find the first platform configuration that repeats itself.
    seen_configurations = set()
    while i < n:
        cycle_platform_once(platform)
        i += 1
        if current_configuration() in seen_configurations:
            break
        seen_configurations.add(current_configuration())

    repeating_configuration = current_configuration()

    # Find the repeat period, i.e. how many cycles we need to get back to the
    # repeating configuration.
    repeat_period = 0
    while i < n:
        cycle_platform_once(platform)
        i += 1
        repeat_period += 1
        if current_configuration() == repeating_configuration:
            break

    # Skip cycles which would get us into the repeating configuration and
    # finalize the cycling.
    n = max((n - i), 0) % repeat_period
    for _ in range(n):
        cycle_platform_once(platform)


def cycle_platform_once(platform):
    def tilt_platform(move_stones_to):
        # Iteratively move stones until the platform does not change anymore.
        platform_changed = True
        while platform_changed:
            platform_changed = False
            for i in range(len(platform)):
                for j in range(len(platform[i])):
                    x, y = move_stones_to(i, j)
                    if (
                        0 <= x < len(platform)
                        and 0 <= y < len(platform[i])
                        and platform[i][j] == "O"
                        and platform[x][y] == "."
                    ):
                        platform[x][y] = "O"
                        platform[i][j] = "."
                        platform_changed = True

    tilt_platform(move_stones_to=lambda i, j: (i - 1, j))  # North
    tilt_platform(move_stones_to=lambda i, j: (i, j - 1))  # West
    tilt_platform(move_stones_to=lambda i, j: (i + 1, j))  # South
    tilt_platform(move_stones_to=lambda i, j: (i, j + 1))  # East


def get_total_load_for_platform(platform):
    return sum(
        row.count("O") * load_per_rock
        for row, load_per_rock in zip(platform, range(len(platform), 0, -1))
    )


def run_program(input):
    platform = parse_input(input)
    cycle_platform_n_times(platform, n=1_000_000_000)
    return get_total_load_for_platform(platform)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            O....#....
            O.OO#....#
            .....##...
            OO.#O....O
            .O.....O#.
            O.#..O.#.#
            ..O..#O..O
            .......O..
            #....###..
            #OO..#....
            """
        )

        result = run_program(input)

        self.assertEqual(result, 64)
