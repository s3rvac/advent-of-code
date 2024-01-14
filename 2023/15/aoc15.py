#
# Advent of Code 2023, day 15
#

import re
import textwrap
import unittest


def read_input():
    with open('input.txt', encoding='utf-8') as f:
        return f.read()


def parse_input(input):
    return input.strip('\n').split(',')


def do_hashmap_procedure(initialization_sequence):
    def parse_step(step):
        m = re.fullmatch(r'([a-z]+)([-=])(\d?)', step)
        label = m.group(1)
        op = m.group(2)
        focal_length = int(m.group(3)) if m.group(3) else 0
        return op, label, focal_length

    boxes = {i: list() for i in range(256)}

    for step in initialization_sequence:
        op, label, focal_length = parse_step(step)
        box_id = hash_string(label)
        box = boxes[box_id]
        if op == '=':
            new_lens = (label, focal_length)
            for i in range(len(box)):
                if box[i][0] == label:
                    box[i] = new_lens
                    break
            else:  # nobreak
                box.append(new_lens)
        else:  # op == '-'
            for i in range(len(box)):
                if box[i][0] == label:
                    del box[i]
                    break

    return boxes


def hash_string(string):
    hash = 0
    for c in string:
        hash += ord(c)
        hash *= 17
        hash %= 256
    return hash


def get_focusing_power(boxes):
    focusing_power = 0
    for box_number, box in boxes.items():
        for slot_number, lens in enumerate(box, start=1):
            focusing_power += (box_number + 1) * slot_number * lens[1]
    return focusing_power


def run_program(input):
    initialization_sequence = parse_input(input)
    boxes = do_hashmap_procedure(initialization_sequence)
    return get_focusing_power(boxes)


if __name__ == '__main__':
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
            """
        )

        result = run_program(input)

        self.assertEqual(result, 145)
