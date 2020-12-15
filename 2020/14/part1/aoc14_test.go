package main

import "testing"

func TestParseProgramFromStringReturnsCorrectProgramWhenInputIsValid(t *testing.T) {
	program, err := parseProgramFromString(
		`
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
`,
	)

	if err != nil {
		t.Fatalf("unexpected failure: %v", err)
	}
	if len(program) != 3 ||
		(program[0] != Instruction{"XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", 8, 11}) ||
		(program[1] != Instruction{"XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", 7, 101}) ||
		(program[2] != Instruction{"XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", 8, 0}) {
		t.Fatalf("unexpected program: %v", program)
	}
}

func TestRunProgramCorrectlyUpdatesAddressSpaceForExampleFromAssignment(t *testing.T) {
	program, _ := parseProgramFromString(
		`
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
`,
	)
	addressSpace := make(AddressSpace)

	runProgram(program, &addressSpace)

	if len(addressSpace) != 2 || addressSpace[7] != 101 || addressSpace[8] != 64 {
		t.Fatalf("unexpected address space: %v", addressSpace)
	}
}

func TestSumNonZeroValuesInAddressSpaceReturnsCorrectValue(t *testing.T) {
	addressSpace := make(AddressSpace)
	addressSpace[5] = 1
	addressSpace[12] = 0
	addressSpace[1000] = 4
	addressSpace[54666] = 5

	sum := sumNonZeroValuesInAddressSpace(&addressSpace)

	if sum != 10 {
		t.Fatalf("unexpected sum: %v", sum)
	}
}
