package main

import (
	"strings"
	"testing"
)

func representationsDiffer(repr1, repr2 string) bool {
	return strings.Trim(repr1, "\n") != strings.Trim(repr2, "\n")
}

func TestParseSeatLayoutFromStringCorrectlyParsesStringWhenItIsValid(t *testing.T) {
	inputRepr := `
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
`

	layout, err := parseSeatLayoutFromString(inputRepr)

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	outputRepr := layout.toString()
	if representationsDiffer(inputRepr, outputRepr) {
		t.Fatalf("unexpected representation:\n%v", outputRepr)
	}
}

func TestParseSeatLayoutFromStringReturnsErrorWhenLayoutHasInvalidFormat(t *testing.T) {
	inputRepr := "xxx"

	_, err := parseSeatLayoutFromString(inputRepr)

	if err == nil {
		t.Fatalf("unexpectedly succeeded")
	}
}

func TestParseSeatLayoutFromStringReturnsErrorWhenLayoutHasUnevenRowLengths(t *testing.T) {
	inputRepr := "LLL\n."

	_, err := parseSeatLayoutFromString(inputRepr)

	if err == nil {
		t.Fatalf("unexpectedly succeeded")
	}
}

func TestProgressCorrectlyChangesLayoutWhenChangesCanHappenForExampleFromAssignment1(t *testing.T) {
	inputRepr := `
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
`
	layout, _ := parseSeatLayoutFromString(inputRepr)

	changed := layout.progress()

	if !changed {
		t.Fatalf("unexpectedly unchanged")
	}
	outputRepr := layout.toString()
	expectedOutputRepr := `
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
`
	if representationsDiffer(outputRepr, expectedOutputRepr) {
		t.Fatalf("unexpected representation:\n%v", outputRepr)
	}
}

func TestProgressCorrectlyChangesLayoutWhenChangesCanHappenForExampleFromAssignment2(t *testing.T) {
	inputRepr := `
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
`
	layout, _ := parseSeatLayoutFromString(inputRepr)

	changed := layout.progress()

	if !changed {
		t.Fatalf("unexpectedly unchanged")
	}
	outputRepr := layout.toString()
	expectedOutputRepr := `
#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#
`
	if representationsDiffer(outputRepr, expectedOutputRepr) {
		t.Fatalf("unexpected representation:\n%v", outputRepr)
	}
}

func TestProgressUntilNoChangeResultsIntoCorrectLayoutForExampleFromAssignment(t *testing.T) {
	inputRepr := `
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
`
	layout, _ := parseSeatLayoutFromString(inputRepr)

	layout.progressUntilNoChange()

	outputRepr := layout.toString()
	expectedOutputRepr := `
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
`
	if representationsDiffer(outputRepr, expectedOutputRepr) {
		t.Fatalf("unexpected representation:\n%v", outputRepr)
	}
}

func TestGetOccupiedSeatCountReturnsCorrectValueForExampleFromAssignment(t *testing.T) {
	inputRepr := `
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
`
	layout, _ := parseSeatLayoutFromString(inputRepr)

	count := layout.getOccupiedSeatCount()

	if count != 26 {
		t.Fatalf("unexpected count: %v", count)
	}
}
