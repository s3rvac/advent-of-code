package main

import (
	"bytes"
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"strings"
)

// Go does not have proper enums, so just use runes.
type SeatRow []rune

type SeatLayout struct {
	grid []SeatRow
}

func parseSeatLayoutRow(s string) (SeatRow, error) {
	row := make(SeatRow, 0)

	for _, c := range []rune(s) {
		switch c {
		case '.', '#', 'L':
			row = append(row, c)
		default:
			return nil, errors.New(fmt.Sprintf("invalid character: %c", c))
		}
	}

	return row, nil
}

func parseSeatLayoutFromString(s string) (SeatLayout, error) {
	grid := make([]SeatRow, 0)

	lines := strings.Split(s, "\n")
	for _, line := range lines {
		if len(line) == 0 {
			continue
		}

		row, err := parseSeatLayoutRow(line)
		if err != nil {
			return SeatLayout{}, err
		}

		if len(grid) > 0 && len(grid[0]) != len(row) {
			return SeatLayout{}, errors.New(fmt.Sprintf("invalid row length: %s", line))
		}

		grid = append(grid, row)
	}

	return SeatLayout{grid}, nil
}

func (layout *SeatLayout) toString() string {
	var b bytes.Buffer

	for _, row := range layout.grid {
		b.WriteString(string(row))
		b.WriteString("\n")
	}

	return b.String()
}

func (layout *SeatLayout) getCellValue(i, j int) (rune, bool) {
	if i < 0 || i >= len(layout.grid) {
		return 'x', false
	} else if j < 0 || j >= len(layout.grid[i]) {
		return 'x', false
	}

	return layout.grid[i][j], true
}

func (layout *SeatLayout) hasVisibleOccupiedSeatInDirection(i, j int, dirI, dirJ int) bool {
	for {
		i += dirI
		j += dirJ

		cellValue, cellExists := layout.getCellValue(i, j)
		if !cellExists {
			return false
		} else if cellValue == '#' {
			return true
		} else if cellValue == 'L' {
			return false
		}
	}
}

func (layout *SeatLayout) isCellOccupied(i, j int) bool {
	cellValue, cellExists := layout.getCellValue(i, j)
	return cellExists && cellValue == '#'
}

func (layout *SeatLayout) getOccupiedSeatCountVisibleFromCell(i, j int) int {
	count := 0

	if layout.hasVisibleOccupiedSeatInDirection(i, j, -1, -1) {
		count += 1
	}
	if layout.hasVisibleOccupiedSeatInDirection(i, j, -1, 0) {
		count += 1
	}
	if layout.hasVisibleOccupiedSeatInDirection(i, j, -1, +1) {
		count += 1
	}
	if layout.hasVisibleOccupiedSeatInDirection(i, j, 0, -1) {
		count += 1
	}
	if layout.hasVisibleOccupiedSeatInDirection(i, j, 0, +1) {
		count += 1
	}
	if layout.hasVisibleOccupiedSeatInDirection(i, j, +1, -1) {
		count += 1
	}
	if layout.hasVisibleOccupiedSeatInDirection(i, j, +1, 0) {
		count += 1
	}
	if layout.hasVisibleOccupiedSeatInDirection(i, j, +1, +1) {
		count += 1
	}

	return count
}

func (layout *SeatLayout) getNewCellState(i, j int) rune {
	cell := layout.grid[i][j]
	switch cell {
	case 'L':
		// If a seat is empty (L) and there are no occupied seats visible from
		// it, the seat becomes occupied.
		if layout.getOccupiedSeatCountVisibleFromCell(i, j) == 0 {
			return '#'
		}
	case '#':
		// If a seat is occupied (#) and five or more seats that are visible
		// from it are also occupied, the seat becomes empty.
		if layout.getOccupiedSeatCountVisibleFromCell(i, j) >= 5 {
			return 'L'
		}
	}

	// The cell is either floor or there was no change.
	return cell
}

func (layout *SeatLayout) progress() (changed bool) {
	if len(layout.grid) == 0 || len(layout.grid[0]) == 0 {
		return false
	}

	// Create a new grid which we will fill with new changes. Then, we will
	// replace the original grid with the new one. We need to modify a copy
	// because all changes to the grid happen in parallel (we would not be able
	// to do them sequentially when using just one grid).
	newGrid := make([]SeatRow, 0)
	for _, row := range layout.grid {
		newGrid = append(newGrid, make(SeatRow, len(row)))
	}

	changed = false
	for i := 0; i < len(layout.grid); i++ {
		for j := 0; j < len(layout.grid[0]); j++ {
			newGrid[i][j] = layout.getNewCellState(i, j)
			if newGrid[i][j] != layout.grid[i][j] {
				changed = true
			}
		}
	}

	layout.grid = newGrid
	return changed
}

func (layout *SeatLayout) progressUntilNoChange() {
	for {
		changed := layout.progress()
		if !changed {
			return
		}
	}
}

func (layout *SeatLayout) getOccupiedSeatCount() int {
	count := 0

	for i := 0; i < len(layout.grid); i++ {
		for j := 0; j < len(layout.grid[0]); j++ {
			if layout.isCellOccupied(i, j) {
				count++
			}
		}
	}

	return count
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputFileContent() string {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc11 INPUT_FILE")
		os.Exit(1)
	}

	content, err := ioutil.ReadFile(os.Args[1])
	if err != nil {
		printErrorAndExit(err)
	}
	return string(content)
}

func main() {
	input := loadInputFileContent()
	layout, err := parseSeatLayoutFromString(input)
	if err != nil {
		printErrorAndExit(err)
	}
	layout.progressUntilNoChange()
	fmt.Println(layout.getOccupiedSeatCount())
}
