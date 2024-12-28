#
# Advent of Code 2024, day 24, part 2
#
# WARNING: The solution might only work for my input (I do not guarantee that
# it works for every input)!
#

import dataclasses
import itertools
import re


@dataclasses.dataclass
class GateConnection:
    in1: str
    in2: str
    gate: str
    out: str


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    def parse_gate_connection(line):
        m = re.fullmatch(r"(.*) (AND|OR|XOR) (.*) -> (.*)", line)
        assert m is not None, f"invalid gate connection: {line}"
        return GateConnection(
            in1=m.group(1),
            in2=m.group(3),
            gate=m.group(2),
            out=m.group(4),
        )

    raw_wire_values, raw_gate_connections = input.strip().split("\n\n")
    wire_values = {
        wire: int(value)
        for wire, value in [line.split(": ") for line in raw_wire_values.split("\n")]
    }
    gate_connections = [
        parse_gate_connection(line) for line in raw_gate_connections.split("\n")
    ]
    return gate_connections, wire_values


def find_wires_to_swap_to_get_adder(gate_connections):
    # After inspecting my input, I have discovered that it implements a
    # ripple-carry adder, and that every gate connection has a specific
    # function. What worked for my input was to check that each gate connection
    # belongs to a specific category, and then switch the outputs of gate
    # connections that do not belong to any of those categories (i.e. wires
    # that are incorrect). I did not need to do any simulations as the input is
    # built in such a way that the described method suffices to find exactly
    # the wires that are incorrect and need to be switched.
    #
    # Here are all the gate-connection categories:
    #
    # 1) xN XOR yN => aN      -- i.e. a XOR of the input x and y bits
    # 2) xN AND yN => bN      -- i.e. an AND of the input x and y bits
    # 3) c(N-1) XOR aN => zN  -- i.e. a XOR of 1) and the incoming carry (=> z bit)
    # 4) c(N-1) AND aN => dN  -- i.e. an AND of 1) and the incoming carry
    # 5) bN OR dN => cN       -- i.e. and OR of both ANDs from 2) and 3)
    #
    # The assumption from the assignment is that input wires are correct; the
    # only incorrect wires are the output ones.
    #
    c00 = None
    for gc in gate_connections:
        if gc.in1 == "x00" and gc.gate == "AND" and gc.in2 == "y00":
            c00 = gc.out

    should_be_bN_or_dN = set()
    should_be_aN_or_cN = set()
    for gc in gate_connections:
        if not re.match(r"[xy](\d+)", gc.in1):
            if gc.gate in ("XOR", "AND"):
                should_be_aN_or_cN |= {gc.in1, gc.in2}
            else:
                should_be_bN_or_dN |= {gc.in1, gc.in2}

    incorrect_wires = set()
    for gc in gate_connections:
        # The following wires are OK for my input (i.e. marking them as
        # incorrect would be wrong).
        if gc.out in ("z00", "z45", c00):
            continue

        # Categories 1) and 2):
        if re.match(r"[xy]\d+", gc.in1) and re.match(r"[xy]\d+", gc.in2):
            if gc.gate == "XOR" and gc.out not in should_be_aN_or_cN:
                incorrect_wires.add(gc.out)
            elif gc.gate == "AND" and gc.out not in should_be_bN_or_dN:
                incorrect_wires.add(gc.out)
        # Category 3):
        elif gc.gate == "XOR" and not re.match(r"z(\d+)", gc.out):
            incorrect_wires.add(gc.out)
        # Category 4):
        elif gc.gate == "AND" and gc.out not in should_be_bN_or_dN:
            incorrect_wires.add(gc.out)
        # Category 5):
        elif gc.gate == "OR" and gc.out not in should_be_aN_or_cN:
            incorrect_wires.add(gc.out)

    return incorrect_wires


def run_program(input):
    gate_connections, _ = parse_input(input)
    wires = find_wires_to_swap_to_get_adder(gate_connections)
    return ",".join(sorted(wires))


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)
