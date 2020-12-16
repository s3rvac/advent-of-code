package main

import "testing"

func TestParseInputInfoFromStringReturnsCorrectRepresentationForExampleFromAssignment(t *testing.T) {
	info, err := parseInputInfoFromString(
		`class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
`,
	)

	if err != nil {
		t.Fatalf("unexpectedly failed: %v", err)
	}
	if len(info.rules) != 3 || len(info.rules["class"]) != 2 ||
		info.rules["class"][0].from != 1 || info.rules["class"][0].to != 3 {
		t.Fatalf("unexpected rules: %v", info.rules)
	}
	if len(info.myTicket) != 3 || info.myTicket[0] != 7 {
		t.Fatalf("unexpected ticket: %v", info.myTicket)
	}
	if len(info.nearbyTickets) != 4 || len(info.nearbyTickets[0]) != 3 || info.nearbyTickets[0][0] != 7 {
		t.Fatalf("unexpected nearby tickets: %v", info.nearbyTickets)
	}
}

func TestComputeErrorScanningRateReturnsCorrectValueForExampleFromAssignment(t *testing.T) {
	info, _ := parseInputInfoFromString(
		`class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
`,
	)

	rate := info.computeErrorScanningRate()

	if rate != 71 {
		t.Fatalf("unexpected rate: %v", rate)
	}
}
