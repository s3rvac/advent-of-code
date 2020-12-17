package main

import "testing"

func TestGetActiveCubeCountReturnsCorrectCountForInitialState(t *testing.T) {
	pd, _ := parsePocketDimensionFromInputString(
		`.#.
..#
###
`,
	)

	activeCubeCount := pd.getActiveCubeCount()

	if activeCubeCount != 5 {
		t.Fatalf("unexpected active cube count: %v", activeCubeCount)
	}
}

func TestIsCubeOnCoordsActiveReturnsTrueForActiveCube(t *testing.T) {
	pd, _ := parsePocketDimensionFromInputString(".#.")

	if !pd.isCubeOnCoordsActive(Coords{0, 1, 0}) {
		t.Fatalf("unexpectedly inactive")
	}
}

func TestIsCubeOnCoordsActiveReturnsFalseForInactiveCube(t *testing.T) {
	pd, _ := parsePocketDimensionFromInputString(".#.")

	if pd.isCubeOnCoordsActive(Coords{0, 0, 0}) {
		t.Fatalf("unexpectedly active")
	}
}

func TestIsCubeOnCoordsActiveReturnsFalseForNonExistingCube(t *testing.T) {
	pd, _ := parsePocketDimensionFromInputString(".")

	if pd.isCubeOnCoordsActive(Coords{2, 2, 2}) {
		t.Fatalf("unexpectedly active")
	}
}

func TestGetCubeNeighborsReturnsCorrectCoords(t *testing.T) {
	pd, _ := parsePocketDimensionFromInputString("#")

	neighbors := pd.getCubeNeighbors(Coords{0, 0, 0})

	if len(neighbors) != 26 {
		t.Fatalf("unexpected neighbors: %v", neighbors)
	}
}

func TestGetActiveNeighborsCountReturnsCorrectValue(t *testing.T) {
	pd, _ := parsePocketDimensionFromInputString(
		`.#.
.##
.##
`,
	)

	count := pd.getActiveNeighborsCount(Coords{1, 1, 0})

	if count != 4 {
		t.Fatalf("unexpected number of active neighbors: %v", count)
	}
}

func TestGetActiveCubeCountReturnsCorrectCountForExampleFromAssignmentAfterSixCycles(t *testing.T) {
	pd, _ := parsePocketDimensionFromInputString(
		`.#.
..#
###
`,
	)
	pd.runCycles(6)

	activeCubeCount := pd.getActiveCubeCount()

	if activeCubeCount != 112 {
		t.Fatalf("unexpected active cube count: %v", activeCubeCount)
	}
}
