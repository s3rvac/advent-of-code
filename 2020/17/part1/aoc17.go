package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"strings"
)

type Coords struct {
	x, y, z int
}

type PocketDimension struct {
	// Store only coordinates of active cubes to save space.
	// Go does not have a set, so use a map.
	grid map[Coords]bool
}

func parsePocketDimensionFromInputString(s string) (*PocketDimension, error) {
	grid := make(map[Coords]bool)

	lines := strings.Split(s, "\n")
	for x, line := range lines {
		for y, c := range line {
			if c == '#' {
				grid[Coords{x, y, 0}] = true
			} else if c != '.' {
				return nil, errors.New(fmt.Sprintf("invalid character: %c", c))
			}
		}
	}

	return &PocketDimension{grid}, nil
}

func (pocketDimension *PocketDimension) isCubeOnCoordsActive(coords Coords) bool {
	// map[] returns the zero value when the given key does not exist.
	return pocketDimension.grid[coords]
}

func (pocketDimension *PocketDimension) getCubeNeighbors(coords Coords) []Coords {
	neighbors := make([]Coords, 0)

	for _, xDiff := range []int{-1, 0, +1} {
		for _, yDiff := range []int{-1, 0, +1} {
			for _, zDiff := range []int{-1, 0, +1} {
				neighbor := Coords{
					coords.x + xDiff,
					coords.y + yDiff,
					coords.z + zDiff,
				}
				if neighbor != coords {
					neighbors = append(neighbors, neighbor)
				}
			}
		}
	}

	return neighbors
}

func (pocketDimension *PocketDimension) getActiveNeighborsCount(coords Coords) int {
	count := 0

	neighborCoords := pocketDimension.getCubeNeighbors(coords)
	for _, neighbor := range neighborCoords {
		if pocketDimension.isCubeOnCoordsActive(neighbor) {
			count++
		}
	}

	return count
}

func (pocketDimension *PocketDimension) shouldCubeBecomeActive(coords Coords) bool {
	isCubeActive := pocketDimension.isCubeOnCoordsActive(coords)
	activeNeighbors := pocketDimension.getActiveNeighborsCount(coords)
	if isCubeActive && (activeNeighbors == 2 || activeNeighbors == 3) {
		return true
	} else if !isCubeActive && activeNeighbors == 3 {
		return true
	} else {
		return false
	}
}

func (pocketDimension *PocketDimension) runCycle() {
	// Obtain coords of all cubes for which we should compute their status in
	// the new grid.
	coordsToCompute := make(map[Coords]bool)
	for coords := range pocketDimension.grid {
		// Currently active cubes.
		coordsToCompute[coords] = true

		// Cubes that are in the direct neighborhood of the active cube
		// (those are the only one that can potentially change).
		neighborCoords := pocketDimension.getCubeNeighbors(coords)
		for _, neighbor := range neighborCoords {
			coordsToCompute[neighbor] = true
		}
	}

	// Compute the new status of all cubes.
	newGrid := make(map[Coords]bool)
	for coords := range coordsToCompute {
		if pocketDimension.shouldCubeBecomeActive(coords) {
			newGrid[coords] = true
		}
	}
	pocketDimension.grid = newGrid
}

func (pocketDimension *PocketDimension) runCycles(cycleCount int) {
	for i := 0; i < cycleCount; i++ {
		pocketDimension.runCycle()
	}
}

func (pocketDimension *PocketDimension) getActiveCubeCount() int {
	// The grid only stores active cubes.
	return len(pocketDimension.grid)
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputFileContent() string {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc17 INPUT_FILE")
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
	pocketDimension, err := parsePocketDimensionFromInputString(input)
	if err != nil {
		printErrorAndExit(err)
	}
	pocketDimension.runCycles(6)
	activeCubeCount := pocketDimension.getActiveCubeCount()
	fmt.Println(activeCubeCount)
}
