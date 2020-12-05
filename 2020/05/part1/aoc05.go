package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"regexp"
)

type BoardingPass struct {
	code   string
	row    int
	col    int
	seatId int
}

type Interval struct {
	low  int
	high int
}

func binaryPartition(interval Interval, instructions string) int {
	for _, instr := range instructions {
		switch instr {
		case 'F', 'L': // lower half
			interval = Interval{
				interval.low,
				interval.low + (interval.high-interval.low)/2,
			}
		case 'B', 'R': // upper half
			interval = Interval{
				interval.low + (interval.high-interval.low)/2 + 1,
				interval.high,
			}
		}
	}
	return interval.low
}

func seatIdForRowAndCol(row int, col int) int {
	return row*8 + col
}

func boardingPassFromString(code string) (BoardingPass, error) {
	// Code is e.g. "FBFBBFFRLR".
	parts := regexp.MustCompile(`^([FB]{7})([LR]{3})$`).FindStringSubmatch(code)
	if parts == nil {
		return BoardingPass{}, errors.New(fmt.Sprintf("boarding pass %s has incorrect format", code))
	}

	row := binaryPartition(Interval{0, 127}, parts[1])
	col := binaryPartition(Interval{0, 7}, parts[2])
	seatId := seatIdForRowAndCol(row, col)

	return BoardingPass{code, row, col, seatId}, nil
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputBoardingPasses() []BoardingPass {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc05 INPUT_FILE")
		os.Exit(1)
	}

	file, err := os.Open(os.Args[1])
	if err != nil {
		printErrorAndExit(err)
	}
	defer file.Close()

	passes := make([]BoardingPass, 0)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		pass, err := boardingPassFromString(scanner.Text())
		if err != nil {
			printErrorAndExit(err)
		}
		passes = append(passes, pass)
	}
	return passes
}

func getHighestSeatId(passes []BoardingPass) int {
	highestSeatId := 0
	for _, pass := range passes {
		if pass.seatId > highestSeatId {
			highestSeatId = pass.seatId
		}
	}
	return highestSeatId
}

func main() {
	passes := loadInputBoardingPasses()
	highestSeatId := getHighestSeatId(passes)
	fmt.Println(highestSeatId)
}
