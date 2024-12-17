#
# Advent of Code 2024, day 17, part 1
#

import dataclasses
import re
import textwrap
import unittest


@dataclasses.dataclass
class Computer:
    reg_a: int
    reg_b: int
    reg_c: int
    program: list[int]


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    m = re.match(
        r"Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\n\nProgram: ([,\d]+)",
        input.strip(),
        flags=re.MULTILINE,
    )
    assert m is not None
    return Computer(
        reg_a=int(m.group(1)),
        reg_b=int(m.group(2)),
        reg_c=int(m.group(3)),
        program=[int(n) for n in m.group(4).split(",")],
    )


def run_computer_and_get_its_output_after_it_halts(computer):
    def combo_operand_value(operand):
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return computer.reg_a
        elif operand == 5:
            return computer.reg_b
        elif operand == 6:
            return computer.reg_c
        raise AssertionError(f"invalid combo operand: {operand}")

    output = []
    ip = 0
    while 0 <= ip < len(computer.program):
        opcode = computer.program[ip]
        operand = computer.program[ip + 1]
        match opcode:
            case 0:  # adv
                computer.reg_a = computer.reg_a >> combo_operand_value(operand)
            case 1:  # bxl
                computer.reg_b ^= operand
            case 2:  # bst
                computer.reg_b = combo_operand_value(operand) % 8
            case 3:  # jnz
                if computer.reg_a != 0:
                    ip = operand
                    continue
            case 4:  # bxc
                computer.reg_b ^= computer.reg_c
            case 5:  # out
                output.append(combo_operand_value(operand) % 8)
            case 6:  # bdv
                computer.reg_b = computer.reg_a >> combo_operand_value(operand)
            case 7:  # cdv
                computer.reg_c = computer.reg_a >> combo_operand_value(operand)
        ip += 2
    return output


def run_program(input):
    computer = parse_input(input)
    output = run_computer_and_get_its_output_after_it_halts(computer)
    return ",".join(map(str, output))


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            Register A: 729
            Register B: 0
            Register C: 0

            Program: 0,1,5,4,3,0
            """
        )

        result = run_program(input)

        self.assertEqual(result, "4,6,3,5,6,3,5,2,1,0")
