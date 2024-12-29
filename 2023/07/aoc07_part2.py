#
# Advent of Code 2023, day 07
#

import collections
import itertools
import textwrap
import unittest


def read_input():
    with open('input.txt', encoding='utf-8') as f:
        return f.read()


def parse_input(input):
    return [parse_hand_and_bid(line) for line in input.strip().split('\n')]


def parse_hand_and_bid(line):
    raw_hand, raw_bid = line.split(' ')
    return list(raw_hand), int(raw_bid)


def compute_total_winnings(hands_and_bids):
    ordered_hands_and_bids = sorted(hands_and_bids, key=hand_and_bid_ordering_key)

    total_winnings = 0
    for rank, (_, bid) in enumerate(ordered_hands_and_bids, start=1):
        total_winnings += rank * bid
    return total_winnings


def hand_and_bid_ordering_key(hand_and_bid):
    hand, _ = hand_and_bid
    return get_best_hand_type(hand), get_cards_strengths(hand)


def get_best_hand_type(hand):
    """Selects the best hand type when the given hand may contain jokers."""
    joker_count = hand.count('J')

    # A hand with 4 or 5 jokers can always be converted to five of kind, so do
    # this right away to speed up the computation.
    if joker_count in (4, 5):
        return get_hand_type(['A', 'A', 'A', 'A', 'A'])

    available_cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']

    hand_types = []
    for joker_replacement in itertools.product(available_cards, repeat=joker_count):
        hand_without_jokers = replace_jokers(hand, joker_replacement)
        hand_types.append(get_hand_type(hand_without_jokers))
    return max(hand_types)


def replace_jokers(hand, joker_replacement):
    new_hand = []
    i = 0
    for card in hand:
        if card == 'J':
            new_hand.append(joker_replacement[i])
            i += 1
        else:
            new_hand.append(card)
    return new_hand


def get_hand_type(hand):
    """Selects the hand type when the given hand does not contain any."""
    counts = [count for _, count in collections.Counter(hand).most_common()]

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
    strengths = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
    return [strengths.index(card) for card in hand]


def run_program(input):
    hands_and_bids = parse_input(input)
    return compute_total_winnings(hands_and_bids)


if __name__ == '__main__':
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

        self.assertEqual(result, 5905)

    def test_get_hand_type_returns_correct_type(self):
        self.assertEqual(get_hand_type('AAAAA'), 7)
        self.assertEqual(get_hand_type('AA8AA'), 6)
        self.assertEqual(get_hand_type('23332'), 5)
        self.assertEqual(get_hand_type('TTT98'), 4)
        self.assertEqual(get_hand_type('23432'), 3)
        self.assertEqual(get_hand_type('A23A4'), 2)
        self.assertEqual(get_hand_type('23456'), 1)

    def test_get_best_hand_type_returns_correct_type(self):
        self.assertEqual(get_best_hand_type('JJJJJ'), 7)
        self.assertEqual(get_best_hand_type('AJAAJ'), 7)
        self.assertEqual(get_best_hand_type('AAAAJ'), 7)
        self.assertEqual(get_best_hand_type('AA8AJ'), 6)
        self.assertEqual(get_best_hand_type('JA8AJ'), 6)
        self.assertEqual(get_best_hand_type('23J32'), 5)
        self.assertEqual(get_best_hand_type('TTJ98'), 4)
        self.assertEqual(get_best_hand_type('JTJ98'), 4)
        self.assertEqual(get_best_hand_type('A23J4'), 2)
        self.assertEqual(get_best_hand_type('23456'), 1)

    def test_get_cards_strengths_returns_correct_strengths(self):
        self.assertEqual(get_cards_strengths('AAAAA'), [12, 12, 12, 12, 12])
        self.assertEqual(get_cards_strengths('AA8AA'), [12, 12, 7, 12, 12])
        self.assertEqual(get_cards_strengths('23332'), [1, 2, 2, 2, 1])
        self.assertEqual(get_cards_strengths('TTT98'), [9, 9, 9, 8, 7])
        self.assertEqual(get_cards_strengths('23432'), [1, 2, 3, 2, 1])
        self.assertEqual(get_cards_strengths('A23A4'), [12, 1, 2, 12, 3])
        self.assertEqual(get_cards_strengths('23456'), [1, 2, 3, 4, 5])
        self.assertEqual(get_cards_strengths('JJJJJ'), [0, 0, 0, 0, 0])
