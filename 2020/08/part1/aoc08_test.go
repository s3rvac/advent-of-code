package main

import "testing"

func TestParseProgramFromStringReturnsCorrectProgramForAccInstruction(t *testing.T) {
	program, err := parseProgramFromString("acc +10")

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(program) != 1 {
		t.Fatalf("unexpected program: %v", program)
	}
	if (program[0] != Instruction{"acc", 10}) {
		t.Fatalf("unexpected program: %v", program)
	}
}

func TestParseProgramFromStringReturnsCorrectProgramForNopInstruction(t *testing.T) {
	program, err := parseProgramFromString("nop +0")

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(program) != 1 {
		t.Fatalf("unexpected program: %v", program)
	}
	if (program[0] != Instruction{"nop", 0}) {
		t.Fatalf("unexpected program: %v", program)
	}
}

func TestParseProgramFromStringReturnsCorrectProgramForJmpInstruction(t *testing.T) {
	program, err := parseProgramFromString("jmp -1")

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(program) != 1 {
		t.Fatalf("unexpected program: %v", program)
	}
	if (program[0] != Instruction{"jmp", -1}) {
		t.Fatalf("unexpected program: %v", program)
	}
}

func TestParseProgramFromStringReturnsErrorWhenThereIsInvalidInstruction(t *testing.T) {
	_, err := parseProgramFromString("xxx -1")

	if err == nil {
		t.Fatalf("unexpectedly valid program")
	}
}

func TestGetAccBeforeInstructionIsExecutedTwiceReturnsCorrectValueForExampleFromAssignment(t *testing.T) {
	program, _ := parseProgramFromString(
		`
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6`,
	)

	acc := getAccBeforeInstructionIsExecutedTwice(program)

	if acc != 5 {
		t.Fatalf("unexpected accumulator value: %v", acc)
	}
}
