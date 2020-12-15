package main

import "testing"

func TestParseInputNumbersFromStringReturnsCorrectNumbersWhenInputStringIsValid(t *testing.T) {
	numbers, err := parseInputNumbersFromString("1,2,3")

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(numbers) != 3 || numbers[0] != 1 || numbers[1] != 2 || numbers[2] != 3 {
		t.Fatalf("unexpected numbers: %v", numbers)
	}
}

func scenarioComputesCorrectNthSpokenNumber(t *testing.T, numbers []int, n int, expectedNumber int) {
	number := computeNthSpokenNumber(numbers, n)

	if number != expectedNumber {
		t.Fatalf("unexpected %v-th number from %v: %v (expected: %v)", n, numbers, number, expectedNumber)
	}
}

func TestComputeNthSpokenNumberReturnsCorrectNumberForExamplesFromAssignment(t *testing.T) {
	scenarioComputesCorrectNthSpokenNumber(t, []int{0, 3, 6}, 30000000, 175594)
	scenarioComputesCorrectNthSpokenNumber(t, []int{1, 3, 2}, 30000000, 2578)
	scenarioComputesCorrectNthSpokenNumber(t, []int{2, 1, 3}, 30000000, 3544142)
	scenarioComputesCorrectNthSpokenNumber(t, []int{1, 2, 3}, 30000000, 261214)
	scenarioComputesCorrectNthSpokenNumber(t, []int{2, 3, 1}, 30000000, 6895259)
	scenarioComputesCorrectNthSpokenNumber(t, []int{3, 2, 1}, 30000000, 18)
	scenarioComputesCorrectNthSpokenNumber(t, []int{3, 1, 2}, 30000000, 362)
}

func TestComputeNthSpokenNumberReturnsCorrectNumberWhenNthNumberIsFromInitialNumbers(t *testing.T) {
	scenarioComputesCorrectNthSpokenNumber(t, []int{0, 3, 6}, 3, 6)
}
