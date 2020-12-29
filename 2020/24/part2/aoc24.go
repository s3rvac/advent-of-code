package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"strings"
)

type TileDirection string

type TileDirections []TileDirection

type TilesDirections []TileDirections

type TileCoords struct {
	x int
	y int
}

type Grid struct {
	// Since Go does not have sets, we use a map that will store the position
	// of every *black* tile.
	blackTiles map[TileCoords]bool
}

func parseTileDirectionsFromString(s string) (TileDirections, error) {
	tileDirections := make(TileDirections, 0)

	for i := 0; i < len(s); i++ {
		switch s[i] {
		case 'e', 'w':
			tileDirection := TileDirection(s[i])
			tileDirections = append(tileDirections, tileDirection)
			continue
		case 's', 'n':
			if i < len(s)-1 && (s[i+1] == 'e' || s[i+1] == 'w') {
				tileDirection := TileDirection(fmt.Sprintf("%c%c", s[i], s[i+1]))
				tileDirections = append(tileDirections, tileDirection)
				i++
				continue
			}
		}

		return nil, errors.New(fmt.Sprintf("invalid tile directions: %s", tileDirections))
	}

	return tileDirections, nil
}

func parseTilesDirectionsFromString(s string) (TilesDirections, error) {
	tilesDirections := make(TilesDirections, 0)

	lines := strings.Split(s, "\n")
	for _, line := range lines {
		if len(line) == 0 {
			continue
		}

		tileDirections, err := parseTileDirectionsFromString(line)
		if err != nil {
			return nil, err
		}
		tilesDirections = append(tilesDirections, tileDirections)
	}

	return tilesDirections, nil
}

func createNewGrid() *Grid {
	return &Grid{make(map[TileCoords]bool)}
}

func copyTileCoordsMap(m map[TileCoords]bool) map[TileCoords]bool {
	newMap := make(map[TileCoords]bool)
	for k, v := range m {
		newMap[k] = v
	}
	return newMap
}

func (grid *Grid) flipTileByDirections(tileDirections TileDirections) {
	// Every directions start from a reference tile in the center of the room.
	x := 0
	y := 0

	// In a hexagonal grid:
	//
	//        e
	//    ne     se
	//        *
	//    nw     sw
	//        w
	//
	// Transformed into a square grid (this is what we use to navigate between
	// tiles):
	//
	//                  ^ y
	//      e se        |
	//     ne *  sw     |
	//        nw  w     +-----> x

	for _, dir := range tileDirections {
		switch dir {
		case "e":
			x -= 1
			y += 1
		case "se":
			y += 1
		case "sw":
			x += 1
		case "w":
			x += 1
			y -= 1
		case "nw":
			y -= 1
		case "ne":
			x -= 1
		}
	}

	coords := TileCoords{x, y}
	if _, exists := grid.blackTiles[coords]; exists {
		// Black tile -> white tile.
		delete(grid.blackTiles, coords)
	} else {
		// White tile -> black tile.
		grid.blackTiles[coords] = true
	}
}

func (grid *Grid) flipTilesByDirections(tilesDirections TilesDirections) {
	for _, tileDirections := range tilesDirections {
		grid.flipTileByDirections(tileDirections)
	}
}

func getNeighborCoords(coords TileCoords) []TileCoords {
	return []TileCoords{
		// e
		TileCoords{coords.x - 1, coords.y + 1},
		// se
		TileCoords{coords.x, coords.y + 1},
		// sw
		TileCoords{coords.x + 1, coords.y},
		// w
		TileCoords{coords.x + 1, coords.y - 1},
		// nw
		TileCoords{coords.x, coords.y - 1},
		// ne
		TileCoords{coords.x - 1, coords.y},
	}
}

func (grid *Grid) isBlackTile(coords TileCoords) bool {
	_, exists := grid.blackTiles[coords]
	return exists
}

func (grid *Grid) isWhiteTile(coords TileCoords) bool {
	return !grid.isBlackTile(coords)
}

func (grid *Grid) getBlackNeighborCount(coords TileCoords) int {
	count := 0
	for _, neighborCoords := range getNeighborCoords(coords) {
		if grid.isBlackTile(neighborCoords) {
			count++
		}
	}
	return count
}

func (grid *Grid) flipTilesByRules() {
	// Rules:
	// - Any black tile with zero or more than 2 black tiles immediately
	//   adjacent to it is flipped to white.
	// - Any white tile with exactly 2 black tiles immediately adjacent to it
	//   is flipped to black.
	// The rules are applied simultaneously to every tile.

	// Compute the coordinates of all tiles that we need to check. We need to
	// check all black tiles as well as their neighbors.
	coordsToCheck := make(map[TileCoords]bool)
	for coords, _ := range grid.blackTiles {
		coordsToCheck[coords] = true
		for _, neighborCoords := range getNeighborCoords(coords) {
			coordsToCheck[neighborCoords] = true
		}
	}

	// Compute the new black tiles according to the rules above.
	newBlackTiles := copyTileCoordsMap(grid.blackTiles)
	for coords, _ := range coordsToCheck {
		blackNeighborCount := grid.getBlackNeighborCount(coords)
		if grid.isBlackTile(coords) && (blackNeighborCount == 0 || blackNeighborCount > 2) {
			// Black -> white.
			delete(newBlackTiles, coords)
		} else if grid.isWhiteTile(coords) && blackNeighborCount == 2 {
			// White -> black.
			newBlackTiles[coords] = true
		}
	}
	grid.blackTiles = newBlackTiles
}

func (grid *Grid) flipTilesByRulesForDays(dayCount int) {
	for i := 0; i < dayCount; i++ {
		grid.flipTilesByRules()
	}
}

func (grid *Grid) countBlackTiles() int {
	return len(grid.blackTiles)
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputFileContent() string {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc24 INPUT_FILE")
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
	tilesDirections, err := parseTilesDirectionsFromString(input)
	if err != nil {
		printErrorAndExit(err)
	}
	grid := createNewGrid()
	grid.flipTilesByDirections(tilesDirections)
	grid.flipTilesByRulesForDays(100)
	count := grid.countBlackTiles()
	fmt.Println(count)
}
