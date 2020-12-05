package main

import "testing"

func scenarioCheckThatBoardingPassFromStringReturnsCorrectPass(t *testing.T, code string, expectedRow int,
	expectedCol int, expectedSeatId int) {
	pass, err := boardingPassFromString(code)

	if err != nil {
		t.Fatalf("unexpected error when parsing boarding pass %v", code)
	}
	if pass.row != expectedRow {
		t.Fatalf("unexpected row when parsing boarding pass %v: expected %v, got %v", code, expectedRow, pass.row)
	}
	if pass.col != expectedCol {
		t.Fatalf("unexpected col when parsing boarding pass %v: expected %v, got %v", code, expectedCol, pass.col)
	}
	if pass.seatId != expectedSeatId {
		t.Fatalf("unexpected seat ID when parsing boarding pass %v: expected %v, got %v", code, expectedSeatId, pass.seatId)
	}
}

func TestBoardingPassFromStringReturnsCorrectBoardingPassWhenStringIsValid(t *testing.T) {
	scenarioCheckThatBoardingPassFromStringReturnsCorrectPass(t, "FBFBBFFRLR", 44, 5, 357)
	scenarioCheckThatBoardingPassFromStringReturnsCorrectPass(t, "BFFFBBFRRR", 70, 7, 567)
	scenarioCheckThatBoardingPassFromStringReturnsCorrectPass(t, "FFFBBBFRRR", 14, 7, 119)
	scenarioCheckThatBoardingPassFromStringReturnsCorrectPass(t, "BBFFBBFRLL", 102, 4, 820)
}

func TestBoardingPassFromStringReturnsErrorWhenSeatSpecHasInvalidFormat(t *testing.T) {
	_, err := boardingPassFromString("xxx")

	if err == nil {
		t.Fatalf("expected an error, got a valid boarding pass")
	}
}

func TestGetHighestSeatIdReturnsCorrectValue(t *testing.T) {
	passes := []BoardingPass{
		BoardingPass{"FBFBBFFRLR", 44, 5, 357},
		BoardingPass{"BFFFBBFRRR", 70, 7, 567},
		BoardingPass{"FFFBBBFRRR", 14, 7, 119},
		BoardingPass{"BBFFBBFRLL", 102, 4, 820},
	}

	highestSeatId := getHighestSeatId(passes)

	if highestSeatId != 820 {
		t.Fatalf("unexpected highest seat ID: %v", highestSeatId)
	}
}
