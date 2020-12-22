package main

import (
	"bytes"
	"errors"
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Image []string

type Tile struct {
	id    int
	image Image
	// Borders:
	left   string
	right  string
	top    string
	bottom string
}

type Tiles struct {
	grid                 []([]Tile)
	allTiles             []Tile
	allTileConfigs       map[int]([]Tile)
	tilesWithBorders     map[string]([]Tile)
	uniqueBorderCountMap map[int]([]Tile)
}

func parseTileFromLines(lines []string) (Tile, error) {
	// Each image is 10x10, with the first line containing its ID.
	if len(lines) != 11 {
		return Tile{}, errors.New(fmt.Sprintf("invalid tile lines: %v", lines))
	}

	// Parse tile ID.
	m := regexp.MustCompile(`^Tile (\d+):$`).FindStringSubmatch(lines[0])
	if len(m) != 2 {
		return Tile{}, errors.New(fmt.Sprintf("invalid tile line: %s", lines[0]))
	}
	id, err := strconv.Atoi(m[1])
	if err != nil {
		return Tile{}, errors.New(fmt.Sprintf("invalid tile line: %s", lines[0]))
	}

	// Parse the image.
	image := make(Image, 0)
	for _, line := range lines[1:] {
		if !regexp.MustCompile(`^[\.#]{10}$`).MatchString(line) {
			return Tile{}, errors.New(fmt.Sprintf("invalid image line: %s", line))
		}
		image = append(image, line)
	}
	return tileFromImage(id, image), nil
}

func tileFromImage(id int, image Image) Tile {
	left := ""
	for i := 0; i < len(image); i++ {
		left += string(image[i][0])
	}
	right := ""
	for i := 0; i < len(image); i++ {
		right += string(image[i][len(image)-1])
	}
	top := image[0]
	bottom := image[len(image)-1]

	return Tile{id, image, left, right, top, bottom}
}

func parseTilesFromString(s string) (*Tiles, error) {
	// Parse all tiles.
	tiles := make([]Tile, 0)
	tileLines := make([]string, 0)
	for _, line := range strings.Split(s, "\n") {
		if len(line) > 0 {
			tileLines = append(tileLines, line)
			continue
		}

		if len(tileLines) > 0 {
			tile, err := parseTileFromLines(tileLines)
			if err != nil {
				return nil, err
			}
			tiles = append(tiles, tile)
			tileLines = make([]string, 0)
		}
	}
	// Last tile.
	if len(tileLines) > 0 {
		tile, err := parseTileFromLines(tileLines)
		if err != nil {
			return nil, err
		}
		tiles = append(tiles, tile)
	}

	// Create the grid.
	tileCount := len(tiles)
	n := int(math.Sqrt(float64(tileCount)))
	if n*n != tileCount {
		return nil, errors.New(fmt.Sprintf("incorrect number of tiles: %v", tileCount))
	}
	allTilesConfigs := computeAllTileConfigs(tiles)
	tilesWithBorders := computeTilesWithBorders(allTilesConfigs)
	uniqueBorderCountMap := computeUniqueBorderCountMap(tiles, tilesWithBorders)
	result := Tiles{
		make([]([]Tile), 0),
		tiles,
		allTilesConfigs,
		tilesWithBorders,
		uniqueBorderCountMap,
	}
	i := 0
	for x := 0; x < n; x++ {
		row := make([]Tile, 0, n)
		for y := 0; y < n; y++ {
			row = append(row, tiles[i])
			i++
		}
		result.grid = append(result.grid, row)
	}
	return &result, nil
}

func reversed(s string) string {
	// From https://github.com/golang/example/blob/master/stringutil/reverse.go
	r := []rune(s)
	for i, j := 0, len(r)-1; i < len(r)/2; i, j = i+1, j-1 {
		r[i], r[j] = r[j], r[i]
	}
	return string(r)
}

func flipImage(image Image, flip int) Image {
	flippedImage := make(Image, 0)

	switch flip {
	case 0:
		// No flip.
		for _, row := range image {
			flippedImage = append(flippedImage, row)
		}
	case 1:
		// Flip around the horizontal axis.
		for i := len(image) - 1; i >= 0; i-- {
			flippedImage = append(flippedImage, image[i])
		}
	case 2:
		// Flip around the vertical axis.
		for _, row := range image {
			flippedImage = append(flippedImage, reversed(row))
		}
	}

	return flippedImage
}

func (tile Tile) flipped(flip int) Tile {
	return tileFromImage(tile.id, flipImage(tile.image, flip))
}

func rotatePixel(x int, y int, image Image, rotation int) (int, int) {
	switch rotation {
	case 90:
		return y, len(image) - x - 1
	case 180:
		// Double rotation by 90 degrees.
		x, y = rotatePixel(x, y, image, 90)
		x, y = rotatePixel(x, y, image, 90)
		return x, y
	case 270:
		// Triple rotation by 90 degrees.
		x, y = rotatePixel(x, y, image, 90)
		x, y = rotatePixel(x, y, image, 90)
		x, y = rotatePixel(x, y, image, 90)
		return x, y
	}

	// 0 - no rotation.
	return x, y
}

func rotateImage(image Image, rotation int) Image {
	// We need to use a rune matrix because strings are immutable.
	matrix := make([]([]rune), 0)
	for _, row := range image {
		matrix = append(matrix, []rune(row))
	}

	for x := 0; x < len(image); x++ {
		for y := 0; y < len(image); y++ {
			newX, newY := rotatePixel(x, y, image, rotation)
			matrix[newX][newY] = rune(image[x][y])
		}
	}

	// Now, we need to convert the rune matrix to an image.
	rotatedImage := make(Image, 0)
	for _, row := range matrix {
		rotatedImage = append(rotatedImage, string(row))
	}
	return rotatedImage
}

func (tile Tile) rotated(rotation int) Tile {
	return tileFromImage(tile.id, rotateImage(tile.image, rotation))
}

func (tile *Tile) allConfigs() []Tile {
	configs := make([]Tile, 0)
	for _, flip := range []int{0, 1, 2} {
		for _, rotation := range []int{0, 90, 180, 270} {
			configs = append(configs, tile.flipped(flip).rotated(rotation))
		}
	}
	return configs
}

func computeAllTileConfigs(allTiles []Tile) map[int]([]Tile) {
	configs := make(map[int]([]Tile))
	for _, tile := range allTiles {
		configs[tile.id] = tile.allConfigs()
	}
	return configs
}

func computeTilesWithBorders(allTileConfigs map[int]([]Tile)) map[string]([]Tile) {
	m := make(map[string]([]Tile))
	for _, tileConfigs := range allTileConfigs {
		for _, tile := range tileConfigs {
			m[tile.left] = append(m[tile.left], tile)
			m[tile.right] = append(m[tile.right], tile)
			m[tile.top] = append(m[tile.top], tile)
			m[tile.bottom] = append(m[tile.bottom], tile)
		}
	}
	return m
}

func computeUniqueBorderCountForTile(tile Tile, tilesWithBorders map[string]([]Tile)) int {
	count := 0
	for _, border := range []string{tile.left, tile.right, tile.top, tile.bottom} {
		isUniqueBorder := true
		for _, t := range tilesWithBorders[border] {
			if t.id != tile.id {
				isUniqueBorder = false
				break
			}
		}
		if isUniqueBorder {
			count++
		}
	}
	return count
}

func computeUniqueBorderCountMap(allTiles []Tile, tilesWithBorders map[string]([]Tile)) map[int]([]Tile) {
	m := make(map[int]([]Tile))
	for _, tile := range allTiles {
		count := computeUniqueBorderCountForTile(tile, tilesWithBorders)
		m[count] = append(m[count], tile)
	}
	return m
}

func copyTiles(row []Tile) []Tile {
	rowCopy := make([]Tile, len(row))
	copy(rowCopy, row)
	return rowCopy
}

func copyGrid(grid []([]Tile)) []([]Tile) {
	gridCopy := make([]([]Tile), 0)
	for _, row := range grid {
		gridCopy = append(gridCopy, copyTiles(row))
	}
	return gridCopy
}

func emptyGrid(n int) []([]Tile) {
	grid := make([]([]Tile), n)
	for i := 0; i < n; i++ {
		grid[i] = make([]Tile, n)
	}
	return grid
}

func tilesToMap(tiles []Tile) map[int]Tile {
	m := make(map[int]Tile)
	for _, tile := range tiles {
		m[tile.id] = tile
	}
	return m
}

func tilesMapWithout(tilesMap map[int]Tile, tileIdToRemove int) map[int]Tile {
	m := make(map[int]Tile)
	for tileId, tile := range tilesMap {
		if tileId != tileIdToRemove {
			m[tileId] = tile
		}
	}
	return m
}

func printGrid(grid []([]Tile)) {
	for x := 0; x < len(grid); x++ {
		for y := 0; y < len(grid); y++ {
			fmt.Printf("%10d", grid[x][y].id)
		}
		fmt.Println()
	}
	fmt.Println()
}

func tileWouldFit(grid []([]Tile), tile Tile, x int, y int) bool {
	// Top border:
	if x > 0 && grid[x-1][y].id != 0 {
		if tile.top != grid[x-1][y].bottom {
			return false
		}
	}

	// Left border:
	if y > 0 && grid[x][y-1].id != 0 {
		if tile.left != grid[x][y-1].right {
			return false
		}
	}

	// Right border:
	if y < len(grid)-1 && grid[x][y+1].id != 0 {
		if tile.right != grid[x][y+1].left {
			return false
		}
	}

	// Bottom border:
	if x < len(grid)-1 && grid[x+1][y].id != 0 {
		if tile.bottom != grid[x+1][y].top {
			return false
		}
	}

	return true
}

func (tiles *Tiles) isUniqueBorder(tileId int, border string) bool {
	for _, tile := range tiles.tilesWithBorders[border] {
		if tile.id != tileId {
			return false
		}
	}
	return true
}

func (tiles *Tiles) hasUniqueBorders(tile Tile, borderPositions []string) bool {
	for _, borderPos := range borderPositions {
		switch borderPos {
		case "left":
			if !tiles.isUniqueBorder(tile.id, tile.left) {
				return false
			}
		case "top":
			if !tiles.isUniqueBorder(tile.id, tile.top) {
				return false
			}
		case "right":
			if !tiles.isUniqueBorder(tile.id, tile.right) {
				return false
			}
		case "bottom":
			if !tiles.isUniqueBorder(tile.id, tile.bottom) {
				return false
			}
		}
	}
	return true
}

func (tiles *Tiles) findTileThatFitsOnPositionAndBacktrack(grid []([]Tile), unusedTiles map[int]Tile,
	x int, y int, uniqueBorderPositions []string, uniqueBorderCount int) (bool, []([]Tile)) {

	for _, tile := range tiles.uniqueBorderCountMap[uniqueBorderCount] {
		if _, unused := unusedTiles[tile.id]; !unused {
			continue
		}

		for _, tileConfig := range tiles.allTileConfigs[tile.id] {
			if !tiles.hasUniqueBorders(tileConfig, uniqueBorderPositions) {
				continue
			} else if !tileWouldFit(grid, tileConfig, x, y) {
				continue
			}

			newGrid := copyGrid(grid)
			newGrid[x][y] = tileConfig
			newUnusedTiles := tilesMapWithout(unusedTiles, tile.id)
			success, finalGrid := tiles.assembleByBacktracking(newGrid, newUnusedTiles)
			if success {
				return true, finalGrid
			}
		}
	}

	return false, nil
}

func (tiles *Tiles) assembleByBacktracking(grid []([]Tile), unusedTiles map[int]Tile) (bool, []([]Tile)) {
	// We assemble the tiles by backtracking. To speed up the backtracking, we
	// use the following fact from the assignment:
	//
	//     Tiles at the edge of the image also have this border, but the
	//     outermost edges won't line up with any other tiles.
	//
	// Hence, we start by (1) matching corners as there are only 4 possible
	// tiles. Then, we (2) continue with edges, and finish (3) by filling the
	// remaining tiles inside.

	// 1) Match corners.
	// Top left:
	if grid[0][0].id == 0 {
		return tiles.findTileThatFitsOnPositionAndBacktrack(
			grid,
			unusedTiles,
			0,
			0,
			[]string{"top", "left"},
			2,
		)
	}
	// Top right:
	if grid[0][len(grid)-1].id == 0 {
		return tiles.findTileThatFitsOnPositionAndBacktrack(
			grid,
			unusedTiles,
			0,
			len(grid)-1,
			[]string{"top", "right"},
			2,
		)
	}
	// Bottom right:
	if grid[len(grid)-1][len(grid)-1].id == 0 {
		return tiles.findTileThatFitsOnPositionAndBacktrack(
			grid,
			unusedTiles,
			len(grid)-1,
			len(grid)-1,
			[]string{"bottom", "right"},
			2,
		)
	}
	// Bottom left:
	if grid[len(grid)-1][0].id == 0 {
		return tiles.findTileThatFitsOnPositionAndBacktrack(
			grid,
			unusedTiles,
			len(grid)-1,
			0,
			[]string{"bottom", "left"},
			2,
		)
	}

	// 2) Match edges.
	// Top:
	for y := 1; y < len(grid)-1; y++ {
		x := 0
		if grid[x][y].id == 0 {
			return tiles.findTileThatFitsOnPositionAndBacktrack(
				grid,
				unusedTiles,
				x,
				y,
				[]string{"top"},
				1,
			)
		}
	}
	// Right:
	for x := 1; x < len(grid)-1; x++ {
		y := len(grid) - 1
		if grid[x][y].id == 0 {
			return tiles.findTileThatFitsOnPositionAndBacktrack(
				grid,
				unusedTiles,
				x,
				y,
				[]string{"right"},
				1,
			)
		}
	}
	// Bottom:
	for y := 1; y < len(grid)-1; y++ {
		x := len(grid) - 1
		if grid[x][y].id == 0 {
			return tiles.findTileThatFitsOnPositionAndBacktrack(
				grid,
				unusedTiles,
				x,
				y,
				[]string{"bottom"},
				1,
			)
		}
	}
	// Left:
	for x := 1; x < len(grid)-1; x++ {
		y := 0
		if grid[x][y].id == 0 {
			return tiles.findTileThatFitsOnPositionAndBacktrack(
				grid,
				unusedTiles,
				x,
				y,
				[]string{"left"},
				1,
			)
		}
	}

	// 3) Match the inner part of the grid.
	for x := 1; x < len(grid)-1; x++ {
		for y := 1; y < len(grid)-1; y++ {
			if grid[x][y].id == 0 {
				return tiles.findTileThatFitsOnPositionAndBacktrack(
					grid,
					unusedTiles,
					x,
					y,
					[]string{},
					0,
				)
			}
		}
	}

	return len(unusedTiles) == 0, grid
}

func (tiles *Tiles) assemble() error {
	success, assembledGrid := tiles.assembleByBacktracking(
		emptyGrid(len(tiles.grid)),
		tilesToMap(tiles.allTiles),
	)
	if !success {
		return errors.New("tiles cannot be assembled")
	}
	tiles.grid = assembledGrid
	return nil
}

func (tiles *Tiles) multipleIdsOfCornerTiles() int {
	n := len(tiles.grid)
	return tiles.grid[0][0].id * tiles.grid[0][n-1].id *
		tiles.grid[n-1][0].id * tiles.grid[n-1][n-1].id
}

func (tiles *Tiles) exportImage() Image {
	n := len(tiles.grid)

	imageGrid := make([]([]Image), n)
	for i := 0; i < n; i++ {
		imageGrid[i] = make([]Image, n)
	}

	// 1) Remove borders around all images and create a grid of them.
	for x := 0; x < n; x++ {
		for y := 0; y < n; y++ {
			imageGrid[x][y] = tiles.grid[x][y].image.withoutBorders()
		}
	}

	// 2) Merge the images in the grid together.
	singleImageLen := len(imageGrid[0][0])
	image := make(Image, len(imageGrid)*singleImageLen)
	i := 0
	for x := 0; x < n; x++ {
		for j := 0; j < singleImageLen; j++ {
			for y := 0; y < n; y++ {
				image[i] += imageGrid[x][y][j]
			}
			i++
		}
	}
	return image
}

func (img Image) withoutBorders() Image {
	result := make(Image, len(img)-2)

	for i := 1; i < len(img)-1; i++ {
		result[i-1] = img[i][1 : len(img)-1]
	}

	return result
}

func (img Image) toString() string {
	var b bytes.Buffer

	for _, line := range img {
		b.WriteString(line)
		b.WriteString("\n")
	}

	return b.String()
}

func imageContainsSeaMonsterOnPosition(img []([]rune), x int, y int) bool {
	//            10 -->
	//  01234567890123456789
	// 0                  #
	// 1#    ##    ##    ###
	// 2 #  #  #  #  #  #

	//     0
	return containsHashSymbolOnPosition(img, x+0, y+18) &&
		// 1
		containsHashSymbolOnPosition(img, x+1, y+0) &&
		containsHashSymbolOnPosition(img, x+1, y+5) &&
		containsHashSymbolOnPosition(img, x+1, y+6) &&
		containsHashSymbolOnPosition(img, x+1, y+11) &&
		containsHashSymbolOnPosition(img, x+1, y+12) &&
		containsHashSymbolOnPosition(img, x+1, y+17) &&
		containsHashSymbolOnPosition(img, x+1, y+18) &&
		containsHashSymbolOnPosition(img, x+1, y+19) &&
		// 2
		containsHashSymbolOnPosition(img, x+2, y+1) &&
		containsHashSymbolOnPosition(img, x+2, y+4) &&
		containsHashSymbolOnPosition(img, x+2, y+7) &&
		containsHashSymbolOnPosition(img, x+2, y+10) &&
		containsHashSymbolOnPosition(img, x+2, y+13) &&
		containsHashSymbolOnPosition(img, x+2, y+16)
}

func containsHashSymbolOnPosition(img []([]rune), x int, y int) bool {
	return x >= 0 && y >= 0 && x < len(img) && y < len(img) && img[x][y] == '#'
}

func writeSeaMonsterInImageOnPosition(img []([]rune), x int, y int) {
	//            10 -->
	//  01234567890123456789
	// 0                  #
	// 1#    ##    ##    ###
	// 2 #  #  #  #  #  #

	// 0
	img[x+0][y+18] = 'O'
	// 1
	img[x+1][y+0] = 'O'
	img[x+1][y+5] = 'O'
	img[x+1][y+6] = 'O'
	img[x+1][y+11] = 'O'
	img[x+1][y+12] = 'O'
	img[x+1][y+17] = 'O'
	img[x+1][y+18] = 'O'
	img[x+1][y+19] = 'O'
	// 2
	img[x+2][y+1] = 'O'
	img[x+2][y+4] = 'O'
	img[x+2][y+7] = 'O'
	img[x+2][y+10] = 'O'
	img[x+2][y+13] = 'O'
	img[x+2][y+16] = 'O'
}

func findAndWriteSeaMonsterInImageOnPosition(img []([]rune), x int, y int) bool {
	if imageContainsSeaMonsterOnPosition(img, x, y) {
		writeSeaMonsterInImageOnPosition(img, x, y)
		return true
	}
	return false
}

func (img Image) determineWaterRoughness() int {
	monsterFound := false

	// Since strings are immutable, we have to use a rune matrix because we
	// need to modify it.
	matrix := make([]([]rune), len(img))
	for i := 0; i < len(img); i++ {
		matrix[i] = []rune(img[i])
	}

	for x := 0; x < len(img); x++ {
		for y := 0; y < len(img); y++ {
			found := findAndWriteSeaMonsterInImageOnPosition(matrix, x, y)
			if found {
				monsterFound = true
			}
		}
	}

	if !monsterFound {
		return 0
	}

	waterRoughness := 0
	for x := 0; x < len(matrix); x++ {
		for y := 0; y < len(matrix); y++ {
			if matrix[x][y] == '#' {
				waterRoughness++
			}
		}
	}
	return waterRoughness
}

func (img Image) determineMaxWaterRoughness() int {
	maxWaterRoughness := 0

	// Try all possible flips and rotations.
	for _, flip := range []int{0, 1, 2} {
		for _, rotation := range []int{0, 90, 180, 270} {
			image := rotateImage(flipImage(img, flip), rotation)
			waterRoughness := image.determineWaterRoughness()
			if waterRoughness > maxWaterRoughness {
				maxWaterRoughness = waterRoughness
			}
		}
	}

	return maxWaterRoughness
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputFileContent() string {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc20 INPUT_FILE")
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
	tiles, err := parseTilesFromString(input)
	if err != nil {
		printErrorAndExit(err)
	}
	err = tiles.assemble()
	if err != nil {
		printErrorAndExit(err)
	}
	image := tiles.exportImage()
	waterRoughness := image.determineMaxWaterRoughness()
	fmt.Println(waterRoughness)
}
