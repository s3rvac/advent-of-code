package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"math/big"
	"os"
	"strconv"
	"strings"
)

type BusId int

type Schedule []BusId

func parseScheduleFromString(s string) (Schedule, error) {
	lines := strings.Split(s, "\n")
	if len(lines) < 2 {
		return nil, errors.New(fmt.Sprintf("invalid input: %s", s))
	}

	// From the assignment: "The first line in your input is no longer
	// relevant."

	schedule := make([]BusId, 0)
	rawBusIds := strings.Split(lines[1], ",")
	for _, rawBusId := range rawBusIds {
		if rawBusId == "x" {
			schedule = append(schedule, BusId(-1))
			continue
		}

		busId, err := strconv.Atoi(rawBusId)
		if err != nil {
			return nil, errors.New(fmt.Sprintf("invalid bus ID: %s", rawBusId))
		}

		schedule = append(schedule, BusId(busId))
	}

	return schedule, nil
}

// Based on https://rosettacode.org/wiki/Chinese_remainder_theorem#Go
func crt(a, n []*big.Int) *big.Int {
	p := new(big.Int).Set(n[0])
	for _, n1 := range n[1:] {
		p.Mul(p, n1)
	}
	var x, q, s, z big.Int
	for i, n1 := range n {
		q.Div(p, n1)
		z.GCD(nil, &s, n1, &q)
		x.Add(&x, s.Mul(a[i], s.Mul(&s, &q)))
	}
	return x.Mod(&x, p)
}

func getEarliestTimestampForDepartureOfAllBuses(schedule Schedule) *big.Int {
	// The earliest timestamp is computed via the Chinese remainder theorem.
	// https://en.wikipedia.org/wiki/Chinese_remainder_theorem
	var n []*big.Int
	var a []*big.Int

	N := big.NewInt(1)
	for offset, busId := range schedule {
		if busId != BusId(-1) {
			n = append(n, big.NewInt(int64(busId)))
			a = append(a, big.NewInt(int64(offset)))
			N.Mul(N, big.NewInt(int64(busId)))
		}
	}

	return N.Sub(N, crt(a, n))
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
	schedule, err := parseScheduleFromString(input)
	if err != nil {
		printErrorAndExit(err)
	}
	earliestTimestamp := getEarliestTimestampForDepartureOfAllBuses(schedule)
	fmt.Println(earliestTimestamp)
}
