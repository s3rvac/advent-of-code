#
# Advent of Code 2023, day 19
#

import collections
import dataclasses
import textwrap
import unittest


@dataclasses.dataclass
class Rule:
    type: str
    target: str
    rating_name: str | None = None
    value: int | None = None


@dataclasses.dataclass
class Range:
    min: int
    max: int

    @classmethod
    def max_possible(cls):
        return Range(min=1, max=4000)

    def is_valid(self):
        return self.min <= self.max

    @property
    def rating(self):
        return self.max - self.min + 1


@dataclasses.dataclass
class Part:
    x: Range
    m: Range
    a: Range
    s: Range

    @classmethod
    def max_possible(cls):
        return cls(
            x=Range.max_possible(),
            m=Range.max_possible(),
            a=Range.max_possible(),
            s=Range.max_possible(),
        )

    def get_range_for(self, name):
        return getattr(self, name)

    def copy_with(self, name, min=None, max=None):
        def range_for(n):
            range = getattr(self, n)
            if name != n:
                return range
            return Range(min=min or range.min, max=max or range.max)

        return Part(
            x=range_for("x"), m=range_for("m"), a=range_for("a"), s=range_for("s")
        )

    def is_valid(self):
        for range in self.ranges:
            if not range.is_valid():
                return False
        return True

    @property
    def ranges(self):
        return [self.x, self.m, self.a, self.s]

    @property
    def rating(self):
        result = 1
        for range in self.ranges:
            result *= range.rating
        return result


def read_input():
    with open("input.txt", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    def parse_workflow_rule(raw_rule):
        if ":" in raw_rule:
            lhs, target = raw_rule.split(":")
            type = "<" if "<" in lhs else ">"
            rating_name, value = lhs.split(type)
            value = int(value)
            return Rule(type=type, target=target, rating_name=rating_name, value=value)
        else:
            return Rule(type="goto", target=raw_rule)

    def parse_workflow(raw_workflow):
        name, raw_rules = raw_workflow[:-1].split("{")
        rules = [parse_workflow_rule(raw_rule) for raw_rule in raw_rules.split(",")]
        return name, rules

    def parse_workflows(raw_workflows):
        return collections.OrderedDict(
            parse_workflow(raw_workflow)
            for raw_workflow in raw_workflows.strip().split("\n")
        )

    # We can ignore part ratings as they are irrelevant to the solution for
    # part 2.
    raw_workflows, _ = input.split("\n\n")
    return parse_workflows(raw_workflows)


def compute_accepted_parts(part, workflows, workflow_name):
    # Recursively compute all accepted parts for the given part and workflow.
    accepted_parts = []
    while True:
        if not part.is_valid() or workflow_name == "R":
            return accepted_parts
        elif workflow_name == "A":
            return accepted_parts + [part]

        for rule in workflows[workflow_name]:
            if rule.type == "<":
                range = part.get_range_for(rule.rating_name)
                new_part = part.copy_with(
                    rule.rating_name, max=min(range.max, rule.value - 1)
                )
                if new_part.is_valid():
                    accepted_parts += compute_accepted_parts(
                        new_part, workflows, rule.target
                    )
                part = part.copy_with(rule.rating_name, min=max(range.min, rule.value))
            elif rule.type == ">":
                range = part.get_range_for(rule.rating_name)
                if rule.value < range.max:
                    new_part = part.copy_with(
                        rule.rating_name, min=max(range.min, rule.value + 1)
                    )
                    accepted_parts += compute_accepted_parts(
                        new_part, workflows, rule.target
                    )
                part = part.copy_with(rule.rating_name, max=min(range.max, rule.value))
            else:  # goto
                workflow_name = rule.target
                break


def count_distinct_accepted_ratings(workflows):
    result = 0
    for part in compute_accepted_parts(Part.max_possible(), workflows, "in"):
        result += part.rating
    return result


def run_program(input):
    workflows = parse_input(input)
    return count_distinct_accepted_ratings(workflows)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            px{a<2006:qkq,m>2090:A,rfg}
            pv{a>1716:R,A}
            lnx{m>1548:A,A}
            rfg{s<537:gd,x>2440:R,A}
            qs{s>3448:A,lnx}
            qkq{x<1416:A,crn}
            crn{x>2662:A,R}
            in{s<1351:px,qqz}
            qqz{s>2770:qs,m<1801:hdj,R}
            gd{a>3333:R,R}
            hdj{m>838:A,pv}

            {x=787,m=2655,a=1222,s=2876}
            {x=1679,m=44,a=2067,s=496}
            {x=2036,m=264,a=79,s=2244}
            {x=2461,m=1339,a=466,s=291}
            {x=2127,m=1623,a=2188,s=1013}
            """
        )

        result = run_program(input)

        self.assertEqual(result, 167409079868000)
