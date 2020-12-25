package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

type Cup int

type Cups []Cup

func parseCupsFromString(s string) (Cups, error) {
	cups := make(Cups, 0)

	for _, c := range strings.Trim(s, "\n") {
		c, err := strconv.Atoi(string(c))
		if err != nil {
			return nil, errors.New(fmt.Sprintf("invalid string: %s", s))
		}
		cups = append(cups, Cup(c))
	}

	return cups, nil
}

func findCupIndex(cups Cups, cupToFind Cup) int {
	for i := 0; i < len(cups); i++ {
		if cups[i] == cupToFind {
			return i
		}
	}
	return -1
}

func computeNextIndex(cups Cups, from int) int {
	return (from + 1) % len(cups)
}

func extractCupFromIndex(cups Cups, i int) (Cups, Cup, int) {
	cup := cups[i]
	cups = append(cups[:i], cups[i+1:]...)
	return cups, cup, computeNextIndex(cups, i-1)
}

func takeCupsFromCurrentCup(cups Cups, n int, currentCup Cup) (Cups, Cups) {
	takenCups := make(Cups, 0, n)

	i := findCupIndex(cups, currentCup)
	i = computeNextIndex(cups, i)
	for x := 0; x < n; x++ {
		newCups, takenCup, newI := extractCupFromIndex(cups, i)
		cups = newCups
		i = newI
		takenCups = append(takenCups, takenCup)
	}

	return cups, takenCups
}

func minMax(cups Cups) (Cup, Cup) {
	min, max := cups[0], cups[0]
	for _, c := range cups {
		if c > max {
			max = c
		}
		if c < min {
			min = c
		}
	}
	return min, max
}

func containsCup(cups Cups, cupToFind Cup) bool {
	return findCupIndex(cups, cupToFind) != -1
}

func selectDestinationCup(cups Cups, currentCup Cup) Cup {
	lowestCup, highestCup := minMax(cups)

	destinationCup := currentCup
	for {
		destinationCup -= 1
		if destinationCup < lowestCup {
			destinationCup = highestCup
		}

		if containsCup(cups, destinationCup) {
			return destinationCup
		}
	}
}

func selectNewCurrentCup(cups Cups, currentCup Cup) Cup {
	// The new current cup is the one immediately after the current cup.
	i := computeNextIndex(cups, findCupIndex(cups, currentCup))
	return cups[i]
}

func joinCups(cups1 Cups, cups2 Cups) Cups {
	result := make(Cups, 0, len(cups1)+len(cups2))
	result = append(result, cups1...)
	result = append(result, cups2...)
	return result
}

func placeCupsAfterCup(cups Cups, takenCups Cups, destinationCup Cup) Cups {
	i := findCupIndex(cups, destinationCup)
	if i == len(cups)-1 {
		// The destination cup is the last one in cups.
		return joinCups(cups, takenCups)
	} else {
		// The destination cup is inside cups (it is not the last one).
		return joinCups(cups[:i+1], joinCups(takenCups, cups[i+1:]))
	}
}

func performMove(cups Cups, currentCup Cup) (Cups, Cup) {
	cups, takenCups := takeCupsFromCurrentCup(cups, 3, currentCup)
	destinationCup := selectDestinationCup(cups, currentCup)
	cups = placeCupsAfterCup(cups, takenCups, destinationCup)
	currentCup = selectNewCurrentCup(cups, currentCup)
	return cups, currentCup
}

func performMoves(cups Cups, moveCount int) Cups {
	currentCup := cups[0]
	for n := 0; n < moveCount; n++ {
		cups, currentCup = performMove(cups, currentCup)
	}

	return cups
}

func getFinalLabelling(cups Cups) string {
	beforeOne := make([]string, 0)
	afterOne := make([]string, 0)

	foundOne := false
	for _, c := range cups {
		if c == 1 {
			foundOne = true
			continue
		}

		c := strconv.Itoa(int(c))
		if foundOne {
			afterOne = append(afterOne, c)
		} else {
			beforeOne = append(beforeOne, c)
		}
	}

	return strings.Join(append(afterOne, beforeOne...), "")
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputFileContent() string {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc23 INPUT_FILE")
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
	cups, err := parseCupsFromString(input)
	if err != nil {
		printErrorAndExit(err)
	}
	cups = performMoves(cups, 100)
	labelling := getFinalLabelling(cups)
	fmt.Println(labelling)
}
