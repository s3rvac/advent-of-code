package main

import "testing"

func TestParseNotesFromStringReturnsCorrectRepresentationForValidNotes(t *testing.T) {
	notes, err := parseNotesFromString("939\n7,13,x,x,59,x,31,19")

	if err != nil {
		t.Fatalf("unexpectedly failed: %v", err)
	}
	if notes.earliestTimestamp != 939 {
		t.Fatalf("unexpected earliest timestamp: %v", notes.earliestTimestamp)
	}
	if len(notes.operatingBusIds) != 5 || notes.operatingBusIds[0] != 7 || notes.operatingBusIds[4] != 19 {
		t.Fatalf("unexpected operating bus IDs: %v", notes.operatingBusIds)
	}
}

func TestParseNotesFromStringReturnsErrorForInvalidEarliestTimestamp(t *testing.T) {
	_, err := parseNotesFromString("xxx\n7,13,x,x,59,x,31,19")

	if err == nil {
		t.Fatalf("unexpectedly succeeded")
	}
}

func TestParseNotesFromStringReturnsErrorForInvalidBusId(t *testing.T) {
	_, err := parseNotesFromString("939\n7,13,x,x,59,x,31,19zzz")

	if err == nil {
		t.Fatalf("unexpectedly succeeded")
	}
}

func TestGetEarliestBusIdAndWaitTimeFromNotesReturnsCorrectResultForExampleFromAssignment(t *testing.T) {
	notes, _ := parseNotesFromString("939\n7,13,x,x,59,x,31,19")

	earliestBusId, waitTime := getEarliestBusIdAndWaitTimeFromNotes(notes)

	if earliestBusId != BusId(59) {
		t.Fatalf("unexpected bus ID: %v", earliestBusId)
	}
	if waitTime != 5 {
		t.Fatalf("unexpected wait time: %v", waitTime)
	}
}
