package main

import "testing"

func TestParseDecksFromStringReturnsCorrectDecksForValidInputString(t *testing.T) {
	deck1, deck2, err := parseDecksFromString(
		`Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10`,
	)

	if err != nil {
		t.Fatalf("unexpectedly failed: %v", err)
	}
	if len(deck1) != 5 || deck1[0] != 9 || deck1[4] != 1 {
		t.Fatalf("unexpected deck1: %v", deck1)
	}
	if len(deck2) != 5 || deck2[0] != 5 || deck2[4] != 10 {
		t.Fatalf("unexpected deck2: %v", deck2)
	}
}

func TestPlayGameReturnsCorrectScoreForLoopingExampleFromAssignment(t *testing.T) {
	deck1, deck2, _ := parseDecksFromString(
		`Player 1:
43
19

Player 2:
2
29
14`,
	)

	winner, _ := playGame(deck1, deck2)

	if winner != 1 {
		t.Fatalf("unexpected winner: %v", winner)
	}
}

func TestPlayGameReturnsCorrectScoreForExampleFromAssignment(t *testing.T) {
	deck1, deck2, _ := parseDecksFromString(
		`Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10`,
	)

	winner, winningScore := playGame(deck1, deck2)

	if winner != 2 {
		t.Fatalf("unexpected winner: %v", winner)
	}
	if winningScore != 291 {
		t.Fatalf("unexpected winning score: %v", winningScore)
	}
}
