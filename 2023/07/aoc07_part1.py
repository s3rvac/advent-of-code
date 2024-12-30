#
# Advent of Code 2023, day 07, part 1
#

import collections
import textwrap
import unittest


# The cards are ordered by their strength.
AVAILABLE_CARDS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    def parse_hand_and_bid(line):
        raw_hand, raw_bid = line.split(" ")
        return list(raw_hand), int(raw_bid)

    return [parse_hand_and_bid(line) for line in input.strip().split("\n")]


def compute_total_winnings(hands_and_bids):
    ordered_hands_and_bids = sorted(hands_and_bids, key=hand_and_bid_ordering_key)

    total_winnings = 0
    for rank, (_, bid) in enumerate(ordered_hands_and_bids, start=1):
        total_winnings += rank * bid
    return total_winnings


def hand_and_bid_ordering_key(hand_and_bid):
    hand, _ = hand_and_bid
    return get_hand_type(hand), get_cards_strengths(hand)


def get_hand_type(hand):
    """Selects the hand type when the given hand does not contain any."""
    counts = sorted(collections.Counter(hand).values(), reverse=True)

    # Five of kind
    if counts == [5]:
        return 7
    # Four of kind
    elif counts == [4, 1]:
        return 6
    # Full house
    elif counts == [3, 2]:
        return 5
    # Three of kind
    elif counts == [3, 1, 1]:
        return 4
    # Two pairs
    elif counts == [2, 2, 1]:
        return 3
    # One pair
    elif counts == [2, 1, 1, 1]:
        return 2
    # High card
    return 1


def get_cards_strengths(hand):
    return [AVAILABLE_CARDS.index(card) for card in hand]


def run_program(input):
    hands_and_bids = parse_input(input)
    return compute_total_winnings(hands_and_bids)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            32T3K 765
            T55J5 684
            KK677 28
            KTJJT 220
            QQQJA 483
            """
        )

        result = run_program(input)

        self.assertEqual(result, 6440)

    def test_get_hand_type_returns_correct_type(self):
        self.assertEqual(get_hand_type("AAAAA"), 7)
        self.assertEqual(get_hand_type("AA8AA"), 6)
        self.assertEqual(get_hand_type("23332"), 5)
        self.assertEqual(get_hand_type("TTT98"), 4)
        self.assertEqual(get_hand_type("23432"), 3)
        self.assertEqual(get_hand_type("A23A4"), 2)
        self.assertEqual(get_hand_type("23456"), 1)

    def test_get_cards_strengths_returns_correct_strengths(self):
        self.assertEqual(get_cards_strengths("AAAAA"), [12, 12, 12, 12, 12])
        self.assertEqual(get_cards_strengths("AA8AA"), [12, 12, 6, 12, 12])
        self.assertEqual(get_cards_strengths("23332"), [0, 1, 1, 1, 0])
        self.assertEqual(get_cards_strengths("TTT98"), [8, 8, 8, 7, 6])
        self.assertEqual(get_cards_strengths("23432"), [0, 1, 2, 1, 0])
        self.assertEqual(get_cards_strengths("A23A4"), [12, 0, 1, 12, 2])
        self.assertEqual(get_cards_strengths("23456"), [0, 1, 2, 3, 4])
        self.assertEqual(get_cards_strengths("22222"), [0, 0, 0, 0, 0])
