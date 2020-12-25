package main

import "testing"

func TestParseGameFromStringReturnsCorrectGameWhenInputStringIsValid(t *testing.T) {
	game, err := parseGameFromString("32415")

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(game.cups) != 5 || game.cups[0] != 3 || game.cups[4] != 5 ||
			game.minCup != 1 || game.maxCup != 5 || game.currCup != 3 {
		t.Fatalf("unexpected game: %v", game)
	}
}

func TestPadCupsWithCupNumbersUpToCorrectlyPadsCups(t *testing.T) {
	game, _ := parseGameFromString("32415")

	game.padCupsWithCupNumbersUpTo(1_000_000)

	cups := game.cups
	if len(cups) != 1_000_000 || cups[0] != 3 || cups[1] != 2 ||
			cups[2] != 4 || cups[3] != 1 || cups[4] != 5 ||
			cups[5] != 6 || cups[6] != 7 || cups[999_999] != 1_000_000 ||
			game.minCup != 1 || game.maxCup != 1_000_000 || game.currCup != 3 {
		t.Fatalf("unexpected cups: %v... (length: %v)", cups[:10], len(cups))
	}
}

func TestMultiplyTwoCupLabelsAfterGivenCupReturnsCurrectNumber(t *testing.T) {
	game, _ := parseGameFromString("32415")

	result := game.multiplyTwoCupLabelsAfterGivenCup(1)

	if result != 15 { // 5 * 3
		t.Fatalf("unexpected result: %v", result)
	}
}

func TestPerformMovesPerformsCorrectMovesOverGivenCupsForExampleFromAssignment(t *testing.T) {
	game, _ := parseGameFromString("389125467")

	game.performMoves(10)

	result := game.multiplyTwoCupLabelsAfterGivenCup(1)
	if result != 18 { // 9 * 2
		t.Fatalf("unexpected result: %v", result)
	}
}

// There is no test for 10M moves because its execution takes too long to
// finish.
