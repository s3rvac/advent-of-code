package main

import "testing"

func TestFindTwoEntriesWhoseSumIsReturnsErrorWhenNoInputEntries(t *testing.T) {
	_, err := findTwoEntriesWhoseSumIs([]int{}, 100)
	if err == nil {
		t.Errorf("expected an error, got nil")
	}
}

func TestFindTwoEntriesWhoseSumIsReturnsErrorWhenNoMatchingEntries(t *testing.T) {
	_, err := findTwoEntriesWhoseSumIs([]int{1, 2}, 5)
	if err == nil {
		t.Errorf("expected an error, got nil")
	}
}

func TestFindTwoEntriesWhoseSumIsReturnsCorrectEntriesWhenThereAreMatchingEntries(t *testing.T) {
	entries, err := findTwoEntriesWhoseSumIs([]int{1, 2, 3}, 5)
	if err != nil {
		t.Errorf("expected no error, but got %v", err)
	}
	if entries[0] != 2 || entries[1] != 3 {
		t.Errorf("got unexpected matching entries: %v", entries)
	}
}

func TestFindTwoEntriesWhoseSumIsReturnsCorrectEntriesForInputFromAssignment(t *testing.T) {
	entries, err := findTwoEntriesWhoseSumIs([]int{1721, 979, 366, 299, 675, 1456}, 2020)
	if err != nil {
		t.Errorf("expected no error, but got %v", err)
	}
	if entries[0] != 1721 || entries[1] != 299 {
		t.Errorf("got unexpected matching entries: %v", entries)
	}
}
