package main

import "testing"

func TestParseCupsFromStringReturnsCorrectCupsWhenInputStringIsValid(t *testing.T) {
	cups, err := parseCupsFromString("32415")

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(cups) != 5 || cups[0] != 3 || cups[4] != 5 {
		t.Fatalf("unexpected cups: %v", cups)
	}
}

func TestGetFinalLabellingReturnsCorrectValue(t *testing.T) {
	cups := Cups{5, 8, 3, 7, 4, 1, 9, 2, 6}

	labelling := getFinalLabelling(cups)

	if labelling != "92658374" {
		t.Fatalf("unexpected labelling: %v", labelling)
	}
}

func TestPerformMovesPerformsCorrectMovesOverGivenCupsForExampleFromAssignment1(t *testing.T) {
	cups := Cups{3, 8, 9, 1, 2, 5, 4, 6, 7}

	cups = performMoves(cups, 10)

	labelling := getFinalLabelling(cups)
	if labelling != "92658374" {
		t.Fatalf("unexpected labelling: %v", labelling)
	}
}

func TestPerformMovesPerformsCorrectMovesOverGivenCupsForExampleFromAssignment2(t *testing.T) {
	cups := Cups{3, 8, 9, 1, 2, 5, 4, 6, 7}

	cups = performMoves(cups, 100)

	labelling := getFinalLabelling(cups)
	if labelling != "67384529" {
		t.Fatalf("unexpected labelling: %v", labelling)
	}
}
