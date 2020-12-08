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

func getAccBeforeInstructionIsExecutedTwice(program Program) int {
	acc := 0

	// Go does not have sets, so we have to use a map.
	executedInstructionIndexes := make(map[int]bool)
	i := 0
	for {
		if _, alreadyExecuted := executedInstructionIndexes[i]; alreadyExecuted {
			// The instruction is about the be executed for the second time.
			return acc
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

	// The program has ended prematurely. Any returned value is fine at this
	// point.
	return acc
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
	acc := getAccBeforeInstructionIsExecutedTwice(program)
	fmt.Println(acc)
}
