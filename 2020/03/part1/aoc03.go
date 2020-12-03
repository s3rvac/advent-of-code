package main

import (
	"bufio"
	"fmt"
	"os"
)

// In the map, `true` means there is a tree, and `false` means there is no
// tree.
//
// Per the assignment, the forest pattern repeats indefinitely to the right, so
// only the base pattern is stored.
type ForestMap struct {
	m [][]bool
}

func newForestMap() *ForestMap {
	return &ForestMap{make([][]bool, 0)}
}

func (m *ForestMap) isEmpty() bool {
	return len(m.m) == 0
}

func (m *ForestMap) addRowFromString(str string) {
	chars := []rune(str)
	row := make([]bool, 0, len(chars))
	for _, c := range chars {
		hasTree := c == '#'
		row = append(row, hasTree)
	}
	m.m = append(m.m, row)
}

func (m *ForestMap) hasTreeOnIndex(row int, col int) bool {
	if row < 0 || col < 0 || row > len(m.m) {
		return false
	}

	// Per the assignment, the forest pattern repeats indefinitely to the
	// right, so incorporate that possibility into the check.
	col = col % len(m.m[row])

	return m.m[row][col]
}

func (m *ForestMap) countEncounteredTrees() int {
	treeCount := 0

	row := 0
	col := 0
	for row < len(m.m) {
		if m.hasTreeOnIndex(row, col) {
			treeCount++
		}
		row += 1
		col += 3
	}

	return treeCount
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputMap() *ForestMap {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc03 INPUT_FILE")
		os.Exit(1)
	}

	file, err := os.Open(os.Args[1])
	if err != nil {
		printErrorAndExit(err)
	}
	defer file.Close()

	m := newForestMap()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		m.addRowFromString(scanner.Text())
	}
	return m
}

func main() {
	m := loadInputMap()
	treeCount := m.countEncounteredTrees()
	fmt.Println(treeCount)
}
