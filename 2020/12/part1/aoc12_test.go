package main

import "testing"

func TestParseStringAsInstructionsReturnsCorrectInstructionsWhenTheyAreValid(t *testing.T) {
	instructions, err := parseStringAsInstructions(
		`N1
S2
E3
W4
L90
R180
F5
`,
	)

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(instructions) != 7 ||
		(instructions[0] != Instruction{'N', 1}) ||
		(instructions[1] != Instruction{'S', 2}) ||
		(instructions[2] != Instruction{'E', 3}) ||
		(instructions[3] != Instruction{'W', 4}) ||
		(instructions[4] != Instruction{'L', 90}) ||
		(instructions[5] != Instruction{'R', 180}) ||
		(instructions[6] != Instruction{'F', 5}) {
		t.Fatalf("unexpected instructions: %v", instructions)
	}
}

func TestParseStringAsInstructionsReturnsErrorWhenInstructionsHaveInvalidFormat(t *testing.T) {
	_, err := parseStringAsInstructions("xxx")

	if err == nil {
		t.Fatalf("unexpectedly succeeded")
	}
}

func TestParseStringAsInstructionsReturnsErrorWhenTurnIsNotMultipleOf90(t *testing.T) {
	_, err := parseStringAsInstructions("L1")

	if err == nil {
		t.Fatalf("unexpectedly succeeded")
	}
}

func TestParseStringAsInstructionsReturnsErrorWhenTurnIsGreaterThan360(t *testing.T) {
	_, err := parseStringAsInstructions("R450")

	if err == nil {
		t.Fatalf("unexpectedly succeeded")
	}
}

func TestParseStringAsInstructionsReturnsErrorWhenValueIsNegative(t *testing.T) {
	_, err := parseStringAsInstructions("N-1")

	if err == nil {
		t.Fatalf("unexpectedly succeeded")
	}
}

func TestFollowInstructionsAndComputeDistanceFromStartReturnsCorrectDistanceForExampleFromAssignment(t *testing.T) {
	instructions, _ := parseStringAsInstructions(
		`F10
N3
F7
R90
F11
`,
	)

	distance := followInstructionsAndComputeDistanceFromStart(instructions)

	if distance != 25 {
		t.Fatalf("unexpected distance: %v", distance)
	}
}
