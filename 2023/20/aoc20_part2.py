#
# Advent of Code 2023, day 20, part 2
#

import collections
import dataclasses
import math
import typing


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


def compute_button_key_presses_to_send_low_pulse_to_rx(modules):
    def get_inputs_for_module(module_name):
        return [
            input_module_name
            for input_module_name, module in modules.items()
            if module_name in module.destinations
        ]

    def is_module_untyped(module_name):
        return module_name not in modules

    # My solution is based on the following assumptions that hold for the
    # puzzle input that I have:
    #
    # - The `rx` module has only a single input module.
    # - That input module is a conjunction (it sends a low pulse to `rx` if it
    #   remembers a high pulse from all its inputs).
    # - The inputs to that conjunction are flipflops and send a high pulse in
    #   regular intervals.
    #
    # The solution is to simulate key presses in the system and note the number
    # of key presses that it takes to send a low pulse to each of the inputs to
    # the `rx` module. Then, when we have the number of key presses for each
    # input of the `rx` module, we can find the least common multiple (LCM) of
    # those numbers to find the number of key presses that it takes to send a
    # low pulse to the `rx` module.
    flipflop_statuses = {
        name: "off" for name, module in modules.items() if module.type == "flipflop"
    }
    conjunction_statuses = {
        name: {m: "low" for m in get_inputs_for_module(name)}
        for name, module in modules.items()
        if module.type == "conjunction"
    }

    rx_input_name = get_inputs_for_module("rx")[0]
    key_presses_to_send_high_pulse_to_rx_input = {
        module: 0 for module in get_inputs_for_module(rx_input_name)
    }

    key_presses = 0
    while True:
        key_presses += 1
        to_process = collections.deque([("button", "broadcaster", "low")])
        while to_process:
            input_module_name, module_name, pulse = to_process.popleft()
            if is_module_untyped(module_name):
                continue
            elif (
                module_name in key_presses_to_send_high_pulse_to_rx_input
                and key_presses_to_send_high_pulse_to_rx_input[module_name] == 0
                and pulse == "low"
            ):
                key_presses_to_send_high_pulse_to_rx_input[module_name] = key_presses
            if all(v > 0 for v in key_presses_to_send_high_pulse_to_rx_input.values()):
                return math.lcm(*key_presses_to_send_high_pulse_to_rx_input.values())

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


def run_program(input):
    modules = parse_input(input)
    return compute_button_key_presses_to_send_low_pulse_to_rx(modules)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)
