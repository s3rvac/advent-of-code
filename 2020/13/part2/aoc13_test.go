package main

import (
	"math/big"
	"testing"
)

func TestParseScheduleFromStringReturnsCorrectRepresentationForValidSchedule(t *testing.T) {
	schedule, err := parseScheduleFromString("939\n7,13,x,x,59,x,31,19")

	if err != nil {
		t.Fatalf("unexpectedly failed: %v", err)
	}
	if len(schedule) != 8 || schedule[0] != 7 || schedule[1] != 13 || schedule[2] != -1 ||
		schedule[3] != -1 || schedule[4] != 59 || schedule[5] != -1 ||
		schedule[6] != 31 || schedule[7] != 19 {
		t.Fatalf("unexpected schedule: %v", schedule)
	}
}

func TestParseScheduleFromStringReturnsErrorForInvalidBusId(t *testing.T) {
	_, err := parseScheduleFromString("939\n7,13,x,x,59,x,31,19zzz")

	if err == nil {
		t.Fatalf("unexpectedly succeeded")
	}
}

func scenarioGetEarliestTimestampForDepartureOfAllBusesReturnsCorrectTimestamp(t *testing.T, scheduleRepr string, expectedTimestamp int64) {
	schedule, _ := parseScheduleFromString("bogus first line\n" + scheduleRepr)

	earliestTimestamp := getEarliestTimestampForDepartureOfAllBuses(schedule)

	if earliestTimestamp.Cmp(big.NewInt(expectedTimestamp)) != 0 {
		t.Fatalf(
			"unexpected earliest timestamp %v for \"%v\" (expected: %v)",
			earliestTimestamp,
			scheduleRepr,
			expectedTimestamp,
		)
	}
}

func TestGetEarliestTimestampForDepartureOfAllBusesReturnsCorrectTimestamp(t *testing.T) {
	scenarioGetEarliestTimestampForDepartureOfAllBusesReturnsCorrectTimestamp(
		t,
		"7,13,x,x,59,x,31,19",
		1068781,
	)
	scenarioGetEarliestTimestampForDepartureOfAllBusesReturnsCorrectTimestamp(
		t,
		"17,x,13,19",
		3417,
	)
	scenarioGetEarliestTimestampForDepartureOfAllBusesReturnsCorrectTimestamp(
		t,
		"67,7,59,61",
		754018,
	)
	scenarioGetEarliestTimestampForDepartureOfAllBusesReturnsCorrectTimestamp(
		t,
		"67,x,7,59,61",
		779210,
	)
	scenarioGetEarliestTimestampForDepartureOfAllBusesReturnsCorrectTimestamp(
		t,
		"67,7,x,59,61",
		1261476,
	)
	scenarioGetEarliestTimestampForDepartureOfAllBusesReturnsCorrectTimestamp(
		t,
		"1789,37,47,1889",
		1202161486,
	)
}
