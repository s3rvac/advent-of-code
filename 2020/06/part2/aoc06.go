package main

import (
	"bufio"
	"fmt"
	"os"
)

type YesAnswersForPerson []rune

type YesAnswersForGroup []YesAnswersForPerson

func answeredYesToQuestion(question rune, yesAnswers YesAnswersForPerson) bool {
	for _, yesAnswer := range yesAnswers {
		if yesAnswer == question {
			return true
		}
	}

	return false
}

func sumYesAnswersForGroup(yesAnswersForGroup YesAnswersForGroup) int {
	if len(yesAnswersForGroup) == 0 {
		return 0
	}

	// Go does not have sets, so use a map instead.
	uniqueYesAnswers := make(map[rune]bool)

	// Initialize the map with all the "yes" answers from the first person.
	// They will form the basis.
	for _, question := range yesAnswersForGroup[0] {
		uniqueYesAnswers[question] = true
	}

	// Now, for each other person, go over all the "yes" answers gathered so
	// far. If the person did not answer "yes" to any of the questions, remove
	// that question from the map as it is no longer eligible.
	for i := 1; i < len(yesAnswersForGroup); i++ {
		// Changing a map while iterating over it is safe:
		// https://golang.org/ref/spec#For_statements
		for question, _ := range uniqueYesAnswers {
			if !answeredYesToQuestion(question, yesAnswersForGroup[i]) {
				delete(uniqueYesAnswers, question)
			}
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
