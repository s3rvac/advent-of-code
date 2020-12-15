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
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
`,
	)
	addressSpace := make(AddressSpace)

	runProgram(program, &addressSpace)

	if len(addressSpace) != 10 || addressSpace[26] != 1 || addressSpace[58] != 100 {
		t.Fatalf("unexpected address space: %v", addressSpace)
	}
}

func TestSumNonZeroValuesInAddressSpaceReturnsCorrectValueForExampleFromAssignment(t *testing.T) {
	program, _ := parseProgramFromString(
		`
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
`,
	)
	addressSpace := make(AddressSpace)
	runProgram(program, &addressSpace)

	sum := sumNonZeroValuesInAddressSpace(&addressSpace)

	if sum != 208 {
		t.Fatalf("unexpected sum: %v", sum)
	}
}
