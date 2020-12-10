package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"sort"
	"strconv"
	"strings"
)

type AdapterJoltages []int

func parseJoltagesFromString(s string) (AdapterJoltages, error) {
	adapterJoltages := make(AdapterJoltages, 0)

	lines := strings.Split(s, "\n")
	for _, line := range lines {
		if len(line) == 0 {
			continue
		}

		n, err := strconv.Atoi(line)
		if err != nil {
			return nil, errors.New("input string has invalid format")
		}
		adapterJoltages = append(adapterJoltages, n)
	}

	return adapterJoltages, nil
}

func findChainThatUsesAllAdapters(adapterJoltages AdapterJoltages) AdapterJoltages {
	chain := make(AdapterJoltages, 0)

	// We have to make a copy before sorting the joltages so that we do not
	// modify the input list.
	sortedAdapterJoltages := make(AdapterJoltages, len(adapterJoltages))
	copy(sortedAdapterJoltages, adapterJoltages)
	sort.Ints(sortedAdapterJoltages)

	// From the assignment: "Treat the charging outlet near your seat as having
	// an effective joltage rating of 0."
	lastUsedJoltage := 0
	chain = append(chain, 0)

	for len(chain) < len(adapterJoltages) {
		nextJoltageFound := false
		for _, joltage := range sortedAdapterJoltages {
			if joltage > lastUsedJoltage && joltage <= (lastUsedJoltage+3) {
				nextJoltageFound = true
				chain = append(chain, joltage)
				lastUsedJoltage = joltage
			}
		}

		if !nextJoltageFound {
			// There is no solution.
			return nil
		}
	}

	// From the assignment: "your device has a built-in joltage adapter rated
	// for 3 jolts higher than the highest-rated adapter in your bag."
	chain = append(chain, lastUsedJoltage+3)

	return chain
}

func multiplyOneJoltDiffsWithThreeJoltDiffs(chain AdapterJoltages) int {
	oneDiffCount := 0
	threeDiffCount := 0

	for i := 1; i < len(chain); i++ {
		switch chain[i] - chain[i-1] {
		case 1:
			oneDiffCount++
		case 3:
			threeDiffCount++
		}
	}

	return oneDiffCount * threeDiffCount
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputFileContent() string {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc10 INPUT_FILE")
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
	adapterJoltages, err := parseJoltagesFromString(input)
	if err != nil {
		printErrorAndExit(err)
	}
	chain := findChainThatUsesAllAdapters(adapterJoltages)
	result := multiplyOneJoltDiffsWithThreeJoltDiffs(chain)
	fmt.Println(result)
}
