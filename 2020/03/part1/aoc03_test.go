package main

import "testing"

func TestNewForestMapCreatesEmptyMap(t *testing.T) {
	m := newForestMap()

	if !m.isEmpty() {
		t.Fatalf("expected the map to be empty")
	}
}

func TestAddRowFromStringAddsRowToForestMap(t *testing.T) {
	m := newForestMap()

	m.addRowFromString(".#")

	if m.isEmpty() {
		t.Fatalf("expected the map to be non-empty")
	}
	if m.hasTreeOnIndex(0, 0) {
		t.Fatalf("expected the map to not have a tree on (0, 0)")
	}
	if !m.hasTreeOnIndex(0, 1) {
		t.Fatalf("expected the map to have a tree on (0, 1)")
	}
}

func TestHasTreeOnIndexDuplicatesRowWhenColIndexOutOfRange(t *testing.T) {
	m := newForestMap()
	m.addRowFromString(".#")

	if m.hasTreeOnIndex(0, 2) {
		t.Fatalf("expected the map to have no tree on (0, 2)")
	}
	if !m.hasTreeOnIndex(0, 3) {
		t.Fatalf("expected the map to have a tree on (0, 3)")
	}
	if m.hasTreeOnIndex(0, 4) {
		t.Fatalf("expected the map to have no tree on (0, 4)")
	}
	if !m.hasTreeOnIndex(0, 5) {
		t.Fatalf("expected the map to have a tree on (0, 5)")
	}
}

func TestHasTreeOnIndexReturnsFalseWhenNegativeRowIndex(t *testing.T) {
	m := newForestMap()

	hasTree := m.hasTreeOnIndex(-1, 0)

	if hasTree {
		t.Fatalf("expected the map to have no tree on a negative index")
	}
}

func TestHasTreeOnIndexReturnsFalseWhenNegativeColIndex(t *testing.T) {
	m := newForestMap()
	m.addRowFromString("#")

	hasTree := m.hasTreeOnIndex(0, -1)

	if hasTree {
		t.Fatalf("expected the map to have no tree on a negative index")
	}
}

func TestHasTreeOnIndexReturnsFalseWhenNoSuchRow(t *testing.T) {
	m := newForestMap()

	hasTree := m.hasTreeOnIndex(1, 0)

	if hasTree {
		t.Fatalf("expected the map to have no tree on (1, 0) as there is no such row")
	}
}

func TestCountEncounteredTreesReturnsCorrectResultForExampleInAssignment(t *testing.T) {
	m := newForestMap()
	m.addRowFromString("..##.........##.........##.........##.........##.........##.......")
	m.addRowFromString("#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..")
	m.addRowFromString(".#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.")
	m.addRowFromString("..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#")
	m.addRowFromString(".#...##..#..#...##..#..#...##..#..#...##..#..#...##..#..#...##..#.")
	m.addRowFromString("..#.##.......#.##.......#.##.......#.##.......#.##.......#.##.....")
	m.addRowFromString(".#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#")
	m.addRowFromString(".#........#.#........#.#........#.#........#.#........#.#........#")
	m.addRowFromString("#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...")
	m.addRowFromString("#...##....##...##....##...##....##...##....##...##....##...##....#")
	m.addRowFromString(".#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#")

	treeCount := m.countEncounteredTrees()

	if treeCount != 7 {
		t.Fatalf("unexpected tree count: %v", treeCount)
	}
}
