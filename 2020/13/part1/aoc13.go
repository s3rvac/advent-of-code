package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

type BusId int

type Notes struct {
	earliestTimestamp int
	operatingBusIds   []BusId
}

func parseNotesFromString(s string) (Notes, error) {
	lines := strings.Split(s, "\n")
	if len(lines) < 2 {
		return Notes{}, errors.New(fmt.Sprintf("invalid input: %s", s))
	}

	earliestTimestamp, err := strconv.Atoi(lines[0])
	if err != nil {
		return Notes{}, errors.New(fmt.Sprintf("invalid input (earliest timestamp): %s", lines[0]))
	}

	operatingBusIds := make([]BusId, 0)
	rawBusIds := strings.Split(lines[1], ",")
	for _, rawBusId := range rawBusIds {
		if rawBusId == "x" {
			continue
		}

		busId, err := strconv.Atoi(rawBusId)
		if err != nil {
			return Notes{}, errors.New(fmt.Sprintf("invalid bus ID: %s", rawBusId))
		}

		operatingBusIds = append(operatingBusIds, BusId(busId))
	}

	return Notes{earliestTimestamp, operatingBusIds}, nil
}

func getWaitTimeForBusId(earliestTimestamp int, busId BusId) int {
	mod := earliestTimestamp % int(busId)
	if mod == 0 {
		return 0
	} else {
		return int(busId) - mod
	}
}

func getEarliestBusIdAndWaitTimeFromNotes(notes Notes) (BusId, int) {
	selectedBusId := BusId(-1)
	selectedBusWaitTime := -1

	for _, busId := range notes.operatingBusIds {
		busWaitTime := getWaitTimeForBusId(notes.earliestTimestamp, busId)
		if selectedBusWaitTime == -1 || busWaitTime <= selectedBusWaitTime {
			selectedBusId = busId
			selectedBusWaitTime = busWaitTime
		}
	}

	return selectedBusId, selectedBusWaitTime
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputFileContent() string {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc13 INPUT_FILE")
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
	notes, err := parseNotesFromString(input)
	if err != nil {
		printErrorAndExit(err)
	}
	earliestBusId, waitTime := getEarliestBusIdAndWaitTimeFromNotes(notes)
	fmt.Println(int(earliestBusId) * waitTime)
}
