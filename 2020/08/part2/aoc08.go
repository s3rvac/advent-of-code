package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Instruction struct {
	operation string
	argument  int
}

type Program []Instruction

func parseProgramFromString(s string) (Program, error) {
	var program Program

	lines := strings.Split(s, "\n")
	for _, line := range lines {
		if len(line) == 0 {
			continue
		}

		m := regexp.MustCompile(`^(acc|jmp|nop) ([-+]\d+)$`).FindStringSubmatch(line)
		if len(m) != 3 {
			return program, errors.New(fmt.Sprintf("invalid instruction: %s", line))
		}

		operation := m[1]
		argument, err := strconv.Atoi(m[2])
		if err != nil {
			return program, errors.New(fmt.Sprintf("invalid instruction: %s", line))
		}

		program = append(program, Instruction{operation, argument})
	}

	return program, nil
}

func runProgramAndCheckIfItTerminates(program Program) (bool, int) {
	acc := 0

	// Go does not have sets, so we have to use a map.
	executedInstructionIndexes := make(map[int]bool)
	for i := 0; i < len(program); {
		if _, alreadyExecuted := executedInstructionIndexes[i]; alreadyExecuted {
			// The instruction is about the be executed for the second time, so
			// there is an infinite loop.
			return false, acc
		}
		executedInstructionIndexes[i] = true

		currentInstruction := program[i]
		switch currentInstruction.operation {
		case "nop":
			i += 1
		case "acc":
			acc += currentInstruction.argument
			i += 1
		case "jmp":
			i += currentInstruction.argument
		}
	}

	// The program has terminated.
	return true, acc
}

func fixProgramAndGetAccAtEnd(program Program) int {
	// Let's start by running the original program. If it terminates, we
	// are done.
	terminated, acc := runProgramAndCheckIfItTerminates(program)
	if terminated {
		return acc
	}

	// Try to fix every instruction, one by one, and see which fix results into
	// a terminating program.
	for i := 0; i < len(program); i++ {
		// First, copy the program so we can experiment with the copy.
		programCopy := make(Program, len(program))
		copy(programCopy, program)

		// Perform the fix.
		instruction := &programCopy[i]
		if instruction.operation == "nop" {
			instruction.operation = "jmp"
		} else if instruction.operation == "jmp" {
			instruction.operation = "nop"
		}

		// Run the program and check its termination status.
		terminated, acc := runProgramAndCheckIfItTerminates(programCopy)
		if terminated {
			return acc
		}
	}

	// The program cannot be fixed.
	return 0
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputFileContent() string {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc08 INPUT_FILE")
		os.Exit(1)
	}

	content, err := ioutil.ReadFile(os.Args[1])
	if err != nil {
		printErrorAndExit(err)
	}
	return string(content)
}

func main() {
	input := loadInputFileContent()
	program, err := parseProgramFromString(input)
	if err != nil {
		printErrorAndExit(err)
	}
	acc := fixProgramAndGetAccAtEnd(program)
	fmt.Println(acc)
}
