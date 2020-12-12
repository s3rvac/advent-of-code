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
	// Go does not have proper enums, so just use runes.
	action rune
	value  int
}

type Instructions []Instruction

func parseInstruction(s string) (Instruction, error) {
	m := regexp.MustCompile(`^(N|S|E|W|L|R|F)(\d+)$`).FindStringSubmatch(s)
	if len(m) != 3 {
		return Instruction{}, errors.New(fmt.Sprintf("invalid instruction: %s", s))
	}

	value, err := strconv.Atoi(m[2])
	if err != nil {
		return Instruction{}, errors.New(fmt.Sprintf("invalid instruction (value conversion failed): %s", s))
	}

	action := rune(m[1][0])
	if (action == 'L' || action == 'R') && (value > 360 || value%90 != 0) {
		return Instruction{}, errors.New(fmt.Sprintf("invalid turn: %s", s))
	}

	return Instruction{action, value}, nil
}

func parseStringAsInstructions(s string) (Instructions, error) {
	instructions := make(Instructions, 0)

	lines := strings.Split(s, "\n")
	for _, line := range lines {
		if len(line) == 0 {
			continue
		}

		instruction, err := parseInstruction(line)
		if err != nil {
			return nil, err
		}

		instructions = append(instructions, instruction)
	}

	return instructions, nil
}

func turn(waypointX *int, waypointY *int, left bool, degrees int) {
	//       y
	//       ^ N
	//       |
	//  W    |    E
	//  <---------> x
	//       |
	//       |
	//       v S
	//

	// To simplify the code, translate rotation by 270 degress to an opposite
	// rotation by 90 degress.
	if degrees == 270 {
		degrees = 90
		left = !left
	}

	if degrees == 90 {
		if left {
			*waypointX, *waypointY = -*waypointY, *waypointX
		} else {
			*waypointX, *waypointY = *waypointY, -*waypointX
		}
	} else if degrees == 180 {
		*waypointX, *waypointY = -*waypointX, -*waypointY
	}
}

func followInstruction(instr Instruction, shipX *int, shipY *int, waypointX *int, waypointY *int) {
	//       y
	//       ^ N
	//       |
	//  W    |    E
	//  <---------> x
	//       |
	//       |
	//       v S
	//
	switch instr.action {
	case 'N':
		*waypointY += instr.value

	case 'S':
		*waypointY -= instr.value

	case 'E':
		*waypointX += instr.value

	case 'W':
		*waypointX -= instr.value

	case 'L', 'R':
		turn(waypointX, waypointY, instr.action == 'L', instr.value)

	case 'F':
		*shipX += *waypointX * instr.value
		*shipY += *waypointY * instr.value
	}
}

func abs(x int) int {
	if x < 0 {
		x = -x
	}
	return x
}

func followInstructionsAndComputeDistanceFromStart(instructions Instructions) int {
	// Follow the instructions.
	//
	//       y
	//       ^ N
	//       |
	//  W    |    E
	//  <---------> x
	//       |
	//       |
	//       v S
	//
	shipX := 0
	shipY := 0
	// From the assignment: "The waypoint starts 10 units east and 1 unit north
	// relative to the ship."
	waypointX := 10
	waypointY := 1

	for _, instr := range instructions {
		followInstruction(instr, &shipX, &shipY, &waypointX, &waypointY)
	}

	// Compute the Manhattan distance from the start.
	return abs(shipX) + abs(shipY)
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputFileContent() string {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc12 INPUT_FILE")
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
	instructions, err := parseStringAsInstructions(input)
	if err != nil {
		printErrorAndExit(err)
	}
	distance := followInstructionsAndComputeDistanceFromStart(instructions)
	fmt.Println(distance)
}
