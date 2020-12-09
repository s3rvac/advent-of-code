package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

type Numbers []int

func parseNumbersFromString(s string) (Numbers, error) {
	numbers := make(Numbers, 0)

	lines := strings.Split(s, "\n")
	for _, line := range lines {
		if len(line) > 0 {
			n, err := strconv.Atoi(line)
			if err != nil {
				return nil, errors.New(fmt.Sprintf("invalid number: %s", line))
			}

			numbers = append(numbers, n)
		}
	}

	return numbers, nil
}

func isSumOfTwoNumbersInWindow(n int, window Numbers) bool {
	for i := 0; i < len(window); i++ {
		for j := i + 1; j < len(window); j++ {
			if window[i]+window[j] == n {
				return true
			}
		}
	}

	return false
}

func findFirstNumberAfterPreambleWhichIsNotSumOfPreviousNumbers(numbers Numbers, preambleSize int) int {
	window := make(Numbers, preambleSize)
	copy(window, numbers)

	for i := preambleSize; i < len(numbers); i++ {
		n := numbers[i]
		if !isSumOfTwoNumbersInWindow(n, window) {
			return n
		}

		// Slide the window, append the new number, and try the next number.
		window = append(window, n)
		window = window[1:]
	}

	// There is no such number.
	return 0
}

func findContiguousListThatSumsToGivenNumber(numbers Numbers, n int) Numbers {
	for i := 0; i < len(numbers); i++ {
		sum := 0
		for j := i; j < len(numbers); j++ {
			sum += numbers[j]
			if sum == n {
				return numbers[i : j+1]
			}
		}
	}

	// There is no such list.
	return nil
}

func sumSmallestAndLargestNumberInList(numbers Numbers) int {
	if len(numbers) == 0 {
		return 0
	}

	smallest := numbers[0]
	largest := numbers[0]

	for _, n := range numbers[1:] {
		if n < smallest {
			smallest = n
		}
		if n > largest {
			largest = n
		}
	}

	return smallest + largest
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputFileContent() string {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc09 INPUT_FILE")
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
	numbers, err := parseNumbersFromString(input)
	if err != nil {
		printErrorAndExit(err)
	}
	n := findFirstNumberAfterPreambleWhichIsNotSumOfPreviousNumbers(numbers, 25)
	list := findContiguousListThatSumsToGivenNumber(numbers, n)
	sum := sumSmallestAndLargestNumberInList(list)
	fmt.Println(sum)
}
