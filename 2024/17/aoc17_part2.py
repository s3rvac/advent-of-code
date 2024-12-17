#
# Advent of Code 2024, day 17, part 2
#
# WARNING: The solution only works for my input (it is not general enough to
# work for any input)!
#

import dataclasses
import re
import sys


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


def find_min_reg_a_value_resulting_in_output_same_as_program(computer):
    # For part 2, I gave up trying to find a general solution and only figured
    # out a solution to my specific input. Here is a high-level
    # representation of the program in my input after I disassembled it:
    #
    #    1) B = A % 8
    #    2) B = B ^ 3
    #    3) C = A >> B
    #    4) A = A >> 3
    #    5) B = B ^ 5
    #    6) B = B ^ C
    #    7) out(B % 8)
    #    8) jnz(A)
    #
    # For 3) and 4), recall that dividing a number by 2**n is the same as
    # shifting it n bits to the right.
    #
    # When looking at the instructions, we can see that during each iteration,
    # the program basically computes the values of B and C from A, uses those
    # to output a value, and shifts A by 3 in instruction n. 4 (even though the
    # shift happens in the middle, the program can be rearranged as after
    # instructions n. 4, the value of A is not used). That is, the program
    # computes one output value at a time from a part of A (see the modulo in
    # the first instruction).
    #
    # What we can do is to start with A = 0, go over the numbers in the program
    # from the end, test all the possible 8 values (0-7) as the lower bits of A
    # (while shifting A by 3 to the left to get the higher bits), check which
    # values result in the target output, and store those values of A.
    #
    # The last piece of the puzzle is to get the minimal viable value of A as
    # this is what the assignment requests.

    def my_program_output_for(A):
        B = A % 8
        B = B ^ 3
        C = A >> B
        B = B ^ 5
        B = B ^ C
        return B % 8

    def find_reg_a_values_producing_output(viable_reg_a_values, target_output):
        reg_a_values = set()
        for reg_a in viable_reg_a_values:
            for lower_reg_a_bits in range(8):
                reg_a_test = (reg_a << 3) | lower_reg_a_bits
                output = my_program_output_for(reg_a_test)
                if output == target_output:
                    reg_a_values.add(reg_a_test)
        return reg_a_values

    viable_reg_a_values = {0}
    for target_output in reversed(computer.program):
        viable_reg_a_values = find_reg_a_values_producing_output(
            viable_reg_a_values, target_output
        )

    if not viable_reg_a_values:
        # As I have written above, the solution only works for my specific
        # input. If we have no viable values of A, we know that the program
        # differs from my input.
        sys.exit("error: incompatible program input")

    return min(viable_reg_a_values)


def run_program(input):
    computer = parse_input(input)
    return find_min_reg_a_value_resulting_in_output_same_as_program(computer)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)
