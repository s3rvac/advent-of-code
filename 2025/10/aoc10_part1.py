#
# Advent of Code 2025, day 10, part 1
#

import collections
import dataclasses
import itertools
import multiprocessing
import re
import textwrap
import unittest


@dataclasses.dataclass
class Machine:
    lights_config: str
    buttons: list[list[int]]

    def get_init_lights_config(self):
        return self.lights_config.replace("#", ".")


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    def parse_machine(raw_machine):
        m = re.fullmatch(r"\[([\.#]+)\] (.+) \{(.*)\}", raw_machine)
        assert m is not None
        lights = m.group(1)
        buttons = [
            list(map(int, raw_buttons.strip("()").split(",")))
            for raw_buttons in m.group(2).split(" ")
        ]
        return Machine(lights, buttons)

    return [parse_machine(line) for line in input.strip().split("\n")]


def get_fewest_bpress_count_to_configure_lights(machine):
    def apply_button(button, lights_config):
        for i in button:
            lights_config = (
                lights_config[:i]
                + ("#" if lights_config[i] == "." else ".")
                + lights_config[i + 1 :]
            )
        return lights_config

    # Keep track of the minimal number of button presses per each configuration
    # to speed up the computation.
    min_counts = {
        "".join(config): float("+inf")
        for config in itertools.product("#.", repeat=len(machine.lights_config))
    }

    # The stored pairs in `to_check` are (lights config, button press count).
    to_check = collections.deque([(machine.get_init_lights_config(), 0)])
    while to_check:
        lights_config, bpress_count = to_check.popleft()
        min_counts[lights_config] = min(min_counts[lights_config], bpress_count)
        if (
            bpress_count <= min_counts[lights_config]
            and bpress_count <= min_counts[machine.lights_config]
        ):
            for button in machine.buttons:
                new_lights_config = apply_button(button, lights_config)
                to_check.append((new_lights_config, bpress_count + 1))
    return min_counts[machine.lights_config]


def run_program(input):
    machines = parse_input(input)
    with multiprocessing.Pool() as pool:
        return sum(pool.map(get_fewest_bpress_count_to_configure_lights, machines))


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
            [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
            [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
            """
        )

        result = run_program(input)

        self.assertEqual(result, 7)
