package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

func parseInputNumbersFromString(s string) ([]int, error) {
	numbers := make([]int, 0)

	for _, x := range strings.Split(strings.Trim(s, "\n"), ",") {
		n, err := strconv.Atoi(x)
		if err != nil {
			return nil, errors.New(fmt.Sprintf("invalid input string: %s", s))
		}
		numbers = append(numbers, n)
	}

	return numbers, nil
}

func computeNthSpokenNumber(initialNumbers []int, n int) int {
	spokenInTurn := make(map[int]int)
	lastNumber := initialNumbers[0]
	turn := 2

	// Initialization.
	for _, number := range initialNumbers[1:] {
		spokenInTurn[lastNumber] = turn - 1
		lastNumber = number
		turn++
	}

	// Computation.
	for turn <= n {
		newLastNumber := 0
		if lastTurn, spoken := spokenInTurn[lastNumber]; spoken {
			newLastNumber = turn - lastTurn - 1
		}
		spokenInTurn[lastNumber] = turn - 1
		lastNumber = newLastNumber
		turn++
	}

	return lastNumber
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputFileContent() string {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc15 INPUT_FILE")
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
	numbers, err := parseInputNumbersFromString(input)
	if err != nil {
		printErrorAndExit(err)
	}
	number := computeNthSpokenNumber(numbers, 2020)
	fmt.Println(number)
}
