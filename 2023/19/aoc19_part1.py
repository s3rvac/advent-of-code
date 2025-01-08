#
# Advent of Code 2023, day 19, part 1
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


def read_input():
    with open("input", encoding="utf-8") as f:
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
            return Rule(type="goto_workflow", target=raw_rule)

    def parse_workflow(raw_workflow):
        # Example: px{a<2006:qkq,m>2090:A,rfg}
        name, raw_rules = raw_workflow[:-1].split("{")
        rules = [parse_workflow_rule(raw_rule) for raw_rule in raw_rules.split(",")]
        return name, rules

    def parse_workflows(raw_workflows):
        return collections.OrderedDict(
            parse_workflow(raw_workflow)
            for raw_workflow in raw_workflows.strip().split("\n")
        )

    def parse_part_and_ratings(raw_part_and_ratings):
        # Example: {x=787,m=2655,a=1222,s=2876}
        return {
            name: int(value)
            for name, value in (
                part.split("=") for part in raw_part_and_ratings[1:-1].split(",")
            )
        }

    def parse_parts_and_ratings(raw_parts_and_ratings):
        return [
            parse_part_and_ratings(raw_rating)
            for raw_rating in raw_parts_and_ratings.strip().split("\n")
        ]

    raw_workflows, raw_parts_and_ratings = input.split("\n\n")
    return parse_workflows(raw_workflows), parse_parts_and_ratings(
        raw_parts_and_ratings
    )


def is_part_accepted(part_with_ratings, workflows):
    workflow_name = "in"
    while True:
        if workflow_name == "A":
            return True
        elif workflow_name == "R":
            return False

        for rule in workflows[workflow_name]:
            if rule.type == "goto_workflow":
                workflow_name = rule.target
                break
            elif rule.type == "<" and part_with_ratings[rule.rating_name] < rule.value:
                workflow_name = rule.target
                break
            elif rule.type == ">" and part_with_ratings[rule.rating_name] > rule.value:
                workflow_name = rule.target
                break


def sum_ratings_of_accepted_parts(workflows, parts_and_ratings):
    result = 0
    for part in parts_and_ratings:
        if is_part_accepted(part, workflows):
            result += sum(part.values())
    return result


def run_program(input):
    workflows, parts_and_ratings = parse_input(input)
    return sum_ratings_of_accepted_parts(workflows, parts_and_ratings)


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

        self.assertEqual(result, 19114)
