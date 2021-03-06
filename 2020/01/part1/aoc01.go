package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"strconv"
)

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputEntries() []int {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc01 INPUT_FILE")
		os.Exit(1)
	}

	file, err := os.Open(os.Args[1])
	if err != nil {
		printErrorAndExit(err)
	}
	defer file.Close()

	var entries []int
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		entry, err := strconv.Atoi(scanner.Text())
		if err != nil {
			printErrorAndExit(err)
		}
		entries = append(entries, entry)
	}
	return entries
}

func findTwoEntriesWithGivenSum(entries []int, sum int) ([]int, error) {
	for i := 0; i < len(entries); i++ {
		for j := i + 1; j < len(entries); j++ {
			if entries[i]+entries[j] == sum {
				return []int{entries[i], entries[j]}, nil
			}
		}
	}
	return []int{}, errors.New("no matching entries were found")
}

func main() {
	inputEntries := loadInputEntries()
	matchingEntries, err := findTwoEntriesWithGivenSum(inputEntries, 2020)
	if err != nil {
		printErrorAndExit(err)
	}
	fmt.Println(matchingEntries[0] * matchingEntries[1])
}
