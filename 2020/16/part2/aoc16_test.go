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

func TestRemoveInvalidNearbyTicketsRemovesCorrectTicketsForExampleFromAssignment(t *testing.T) {
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

	info.removeInvalidNearbyTickets()

	if len(info.nearbyTickets) != 1 || info.nearbyTickets[0][0] != 7 {
		t.Fatalf("unexpected nearby tickets: %v", info.nearbyTickets)
	}
}

func TestDetermineFieldsOrderReturnsCorrectOrderForExampleFromAssignment(t *testing.T) {
	info, _ := parseInputInfoFromString(
		`class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9`,
	)

	order := info.determineFieldsOrder()

	if len(order) != 3 || order[0] != "row" || order[1] != "class" || order[2] != "seat" {
		t.Fatalf("unexpected order: %v", order)
	}
}

func TestMapLocationsToMyTicketValuesReturnsCorrectMapForExampleFromAssignment(t *testing.T) {
	info, _ := parseInputInfoFromString(
		`class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9`,
	)
	fieldsOrder := info.determineFieldsOrder()

	m := info.mapLocationsToMyTicketValues(fieldsOrder)

	if len(m) != 3 || m["class"] != 12 || m["row"] != 11 || m["seat"] != 13 {
		t.Fatalf("unexpected map: %v", m)
	}
}

func TestMultiplyValuesForLocationsStartingWithReturnsCorrectResultForModifiedExampleFromAssignment(t *testing.T) {
	info, _ := parseInputInfoFromString(
		`departure location: 0-1 or 4-19
departure station: 0-5 or 8-19
arrival location: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9`,
	)
	fieldsOrder := info.determineFieldsOrder()
	m := info.mapLocationsToMyTicketValues(fieldsOrder)

	result := multiplyValuesForLocationsStartingWith(m, "departure")

	if result != 11*12 {
		t.Fatalf("unexpected result: %v", result)
	}
}
