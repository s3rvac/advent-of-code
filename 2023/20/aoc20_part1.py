#
# Advent of Code 2023, day 20, part 1
#

import collections
import dataclasses
import textwrap
import typing
import unittest


@dataclasses.dataclass
class Module:
    name: str
    type: str
    destinations: typing.List[str]


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    def parse_line(line):
        type_and_name, destinations = line.split(" -> ")
        if type_and_name.startswith("&"):
            type = "conjunction"
            name = type_and_name[1:]
        elif type_and_name.startswith("%"):
            type = "flipflop"
            name = type_and_name[1:]
        else:
            assert type_and_name == "broadcaster"
            type = name = type_and_name
        return name, Module(name, type, destinations.split(", "))

    return dict(parse_line(line) for line in input.strip().split("\n"))


def compute_pulses_after_pressing_button_n_times(modules, n):
    def get_inputs_for_module(module_name):
        return [
            input_module_name
            for input_module_name, module in modules.items()
            if module_name in module.destinations
        ]

    flipflop_statuses = {
        name: "off" for name, module in modules.items() if module.type == "flipflop"
    }
    conjunction_statuses = {
        name: {m: "low" for m in get_inputs_for_module(name)}
        for name, module in modules.items()
        if module.type == "conjunction"
    }

    pulse_count = {"low": 0, "high": 0}
    for _ in range(n):
        to_process = collections.deque([("button", "broadcaster", "low")])
        while to_process:
            input_module_name, module_name, pulse = to_process.popleft()
            pulse_count[pulse] += 1
            if module_name not in modules:
                # Untyped module.
                continue
            module = modules[module_name]
            if module.type == "broadcaster":
                for destination in module.destinations:
                    to_process.append((module_name, destination, pulse))
            elif module.type == "flipflop":
                if pulse == "low":
                    if flipflop_statuses[module_name] == "on":
                        flipflop_statuses[module_name] = "off"
                        next_pulse = "low"
                    else:
                        flipflop_statuses[module_name] = "on"
                        next_pulse = "high"
                    for destination in module.destinations:
                        to_process.append((module_name, destination, next_pulse))
            elif module.type == "conjunction":
                conjunction_statuses[module_name][input_module_name] = pulse
                if all(
                    status == "high"
                    for status in conjunction_statuses[module_name].values()
                ):
                    next_pulse = "low"
                else:
                    next_pulse = "high"
                for destination in module.destinations:
                    to_process.append((module_name, destination, next_pulse))

    return pulse_count["low"], pulse_count["high"]


def run_program(input):
    modules = parse_input(input)
    low_pulse_count, high_pulse_count = compute_pulses_after_pressing_button_n_times(
        modules, n=1000
    )
    return low_pulse_count * high_pulse_count


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input1(self):
        input = textwrap.dedent(
            """
            broadcaster -> a, b, c
            %a -> b
            %b -> c
            %c -> inv
            &inv -> a
            """
        )

        result = run_program(input)

        self.assertEqual(result, 32000000)

    def test_program_returns_correct_result_for_example_input2(self):
        input = textwrap.dedent(
            """
            broadcaster -> a
            %a -> inv, con
            &inv -> b
            %b -> con
            &con -> output
            """
        )

        result = run_program(input)

        self.assertEqual(result, 11687500)
