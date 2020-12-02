package main

import "testing"

func TestFindThreeEntriesWithGivenSumReturnsErrorWhenNoInputEntries(t *testing.T) {
	_, err := findThreeEntriesWithGivenSum([]int{}, 100)

	if err == nil {
		t.Errorf("expected an error, got nil")
	}
}

func TestFindThreeEntriesWithGivenSumReturnsErrorWhenNoMatchingEntries(t *testing.T) {
	_, err := findThreeEntriesWithGivenSum([]int{1, 2, 3}, 10)

	if err == nil {
		t.Errorf("expected an error, got nil")
	}
}

func TestFindThreeEntriesWithGivenSumReturnsCorrectEntriesWhenThereAreMatchingEntries(t *testing.T) {
	entries, err := findThreeEntriesWithGivenSum([]int{1, 2, 3}, 6)

	if err != nil {
		t.Errorf("expected no error, but got %v", err)
	}
	if entries[0] != 1 || entries[1] != 2 || entries[2] != 3 {
		t.Errorf("got unexpected matching entries: %v", entries)
	}
}

func TestFindThreeEntriesWithGivenSumReturnsCorrectEntriesForInputFromAssignment(t *testing.T) {
	entries, err := findThreeEntriesWithGivenSum([]int{1721, 979, 366, 299, 675, 1456}, 2020)

	if err != nil {
		t.Errorf("expected no error, but got %v", err)
	}
	if entries[0] != 979 || entries[1] != 366 || entries[2] != 675 {
		t.Errorf("got unexpected matching entries: %v", entries)
	}
}
