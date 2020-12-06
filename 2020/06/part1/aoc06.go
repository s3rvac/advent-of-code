package main

import (
	"bufio"
	"fmt"
	"os"
)

type YesAnswersForPerson []rune

type YesAnswersForGroup []YesAnswersForPerson

func sumYesAnswersForGroup(yesAnswersForGroup YesAnswersForGroup) int {
	// Go does not have sets, so use a map instead.
	uniqueYesAnswers := make(map[rune]bool)
	for _, yesAnswersForPerson := range yesAnswersForGroup {
		for _, question := range yesAnswersForPerson {
			uniqueYesAnswers[question] = true
		}
	}
	return len(uniqueYesAnswers)
}

func sumYesAnswersPerGroup(yesAnswers []YesAnswersForGroup) int {
	sum := 0
	for _, yesAnswersForGroup := range yesAnswers {
		sum += sumYesAnswersForGroup(yesAnswersForGroup)
	}
	return sum
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadYesAnswersFromInput() []YesAnswersForGroup {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc06 INPUT_FILE")
		os.Exit(1)
	}

	file, err := os.Open(os.Args[1])
	if err != nil {
		printErrorAndExit(err)
	}
	defer file.Close()

	var yesAnswers []YesAnswersForGroup
	var yesAnswersForGroup YesAnswersForGroup
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" && len(yesAnswersForGroup) > 0 {
			yesAnswers = append(yesAnswers, yesAnswersForGroup)
			yesAnswersForGroup = make(YesAnswersForGroup, 0)
		} else {
			yesAnswersForGroup = append(yesAnswersForGroup, YesAnswersForPerson(line))
		}
	}
	// Include answers from the very last group (if any).
	if len(yesAnswersForGroup) > 0 {
		yesAnswers = append(yesAnswers, yesAnswersForGroup)
	}
	return yesAnswers
}

func main() {
	yesAnswers := loadYesAnswersFromInput()
	sum := sumYesAnswersPerGroup(yesAnswers)
	fmt.Println(sum)
}
