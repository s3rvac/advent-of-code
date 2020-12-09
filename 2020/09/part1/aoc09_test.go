package main

import "testing"

func TestParseNumbersFromStringReturnsCorrectNumbersWhenInputStringIsValid(t *testing.T) {
	numbers, err := parseNumbersFromString("1\n2\n3")

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(numbers) != 3 || numbers[0] != 1 || numbers[1] != 2 || numbers[2] != 3 {
		t.Fatalf("unexpected numbers: %v", numbers)
	}
}

func TestParseNumbersFromStringReturnsErrorWhenInputStringIsInvalid(t *testing.T) {
	_, err := parseNumbersFromString("xxx")

	if err == nil {
		t.Fatalf("unexpectedly succeeded")
	}
}

func TestFindFirstNumberAfterPreambleWhichIsNotSumOfPreviousNumbersReturnsCorrectResultForExampleFromAssignemtn(t *testing.T) {
	numbers, _ := parseNumbersFromString(
		`35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576`,
	)

	n := findFirstNumberAfterPreambleWhichIsNotSumOfPreviousNumbers(numbers, 5)

	if n != 127 {
		t.Fatalf("unexpected number: %v", n)
	}
}
