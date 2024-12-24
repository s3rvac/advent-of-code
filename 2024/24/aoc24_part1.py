#
# Advent of Code 2024, day 24, part 1
#

import dataclasses
import re
import textwrap
import unittest


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


def compute_number_produced_by_z_wires(gate_connections, initial_wire_values):
    def value_for(gate, in1, in2):
        if in1 is None or in2 is None:
            return None
        elif gate == "AND":
            return in1 & in2
        elif gate == "OR":
            return in1 | in2
        else:
            return in1 ^ in2

    def decimal_number_produced_by_z_wires(wire_values):
        z_wires = reversed(
            sorted((wire, v) for wire, v in wire_values.items() if wire.startswith("z"))
        )
        return int("".join(str(v) for _, v in z_wires), 2)

    wire_values = initial_wire_values.copy()
    output_changed = True
    while output_changed:
        output_changed = False
        for gc in gate_connections:
            new_value = value_for(
                gc.gate, wire_values.get(gc.in1), wire_values.get(gc.in2)
            )
            if wire_values.get(gc.out) != new_value:
                wire_values[gc.out] = new_value
                output_changed = True

    return decimal_number_produced_by_z_wires(wire_values)


def run_program(input):
    gate_connections, wire_values = parse_input(input)
    return compute_number_produced_by_z_wires(gate_connections, wire_values)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input1(self):
        input = textwrap.dedent(
            """
            x00: 1
            x01: 1
            x02: 1
            y00: 0
            y01: 1
            y02: 0

            x00 AND y00 -> z00
            x01 XOR y01 -> z01
            x02 OR y02 -> z02
            """
        )

        result = run_program(input)

        self.assertEqual(result, 4)

    def test_program_returns_correct_result_for_example_input2(self):
        input = textwrap.dedent(
            """
            x00: 1
            x01: 0
            x02: 1
            x03: 1
            x04: 0
            y00: 1
            y01: 1
            y02: 1
            y03: 1
            y04: 1

            ntg XOR fgs -> mjb
            y02 OR x01 -> tnw
            kwq OR kpj -> z05
            x00 OR x03 -> fst
            tgd XOR rvg -> z01
            vdt OR tnw -> bfw
            bfw AND frj -> z10
            ffh OR nrd -> bqk
            y00 AND y03 -> djm
            y03 OR y00 -> psh
            bqk OR frj -> z08
            tnw OR fst -> frj
            gnj AND tgd -> z11
            bfw XOR mjb -> z00
            x03 OR x00 -> vdt
            gnj AND wpb -> z02
            x04 AND y00 -> kjc
            djm OR pbm -> qhw
            nrd AND vdt -> hwm
            kjc AND fst -> rvg
            y04 OR y02 -> fgs
            y01 AND x02 -> pbm
            ntg OR kjc -> kwq
            psh XOR fgs -> tgd
            qhw XOR tgd -> z09
            pbm OR djm -> kpj
            x03 XOR y03 -> ffh
            x00 XOR y04 -> ntg
            bfw OR bqk -> z06
            nrd XOR fgs -> wpb
            frj XOR qhw -> z04
            bqk OR frj -> z07
            y03 OR x01 -> nrd
            hwm AND bqk -> z03
            tgd XOR rvg -> z12
            tnw OR pbm -> gnj
            """
        )

        result = run_program(input)

        self.assertEqual(result, 2024)
