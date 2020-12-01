package main

import "testing"

func TestFindThreeEntriesWhoseSumIsReturnsErrorWhenNoInputEntries(t *testing.T) {
	_, err := findThreeEntriesWhoseSumIs([]int{}, 100)
	if err == nil {
		t.Errorf("expected an error, got nil")
	}
}

func TestFindThreeEntriesWhoseSumIsReturnsErrorWhenNoMatchingEntries(t *testing.T) {
	_, err := findThreeEntriesWhoseSumIs([]int{1, 2, 3}, 10)
	if err == nil {
		t.Errorf("expected an error, got nil")
	}
}

func TestFindThreeEntriesWhoseSumIsReturnsCorrectEntriesWhenThereAreMatchingEntries(t *testing.T) {
	entries, err := findThreeEntriesWhoseSumIs([]int{1, 2, 3}, 6)
	if err != nil {
		t.Errorf("expected no error, but got %v", err)
	}
	if entries[0] != 1 || entries[1] != 2 || entries[2] != 3 {
		t.Errorf("got unexpected matching entries: %v", entries)
	}
}

func TestFindThreeEntriesWhoseSumIsReturnsCorrectEntriesForInputFromAssignment(t *testing.T) {
	entries, err := findThreeEntriesWhoseSumIs([]int{1721, 979, 366, 299, 675, 1456}, 2020)
	if err != nil {
		t.Errorf("expected no error, but got %v", err)
	}
	if entries[0] != 979 || entries[1] != 366 || entries[2] != 675 {
		t.Errorf("got unexpected matching entries: %v", entries)
	}
}
