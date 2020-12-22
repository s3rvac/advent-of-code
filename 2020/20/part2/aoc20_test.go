package main

import "testing"

const tilesFromAssignment = `Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
`

func TestParseTilesFromStringReturnsCorrectTilesForValidString(t *testing.T) {
	tiles, err := parseTilesFromString(tilesFromAssignment)

	if err != nil {
		t.Fatalf("unexpectedly failed: %v", err)
	}
	if len(tiles.grid) != 3 {
		t.Fatalf("unexpected grid size: %v", len(tiles.grid))
	}
	img := tiles.grid[0][0]
	// Tile 2311:
	// ..##.#..#.
	// ##..#.....
	// #...##..#.
	// ####.#...#
	// ##.##.###.
	// ##...#.###
	// .#.#.#..##
	// ..#....#..
	// ###...#.#.
	// ..###..###
	if img.id != 2311 || len(img.image) != 10 || len(img.image[0]) != 10 ||
		img.image[0][0] != '.' || img.image[0][2] != '#' ||
		img.left != ".#####..#." || img.right != "...#.##..#" ||
		img.top != "..##.#..#." || img.bottom != "..###..###" {
		t.Fatalf("unexpected first image in the grid: %v", img)
	}
}

func TestTileFlippedReturnsCorrectTileAfterNoFlip(t *testing.T) {
	tile, _ := parseTileFromLines([]string{
		"Tile 2311:",
		"..##.#..#.",
		"##..#.....",
		"#...##..#.",
		"####.#...#",
		"##.##.###.",
		"##...#.###",
		".#.#.#..##",
		"..#....#..",
		"###...#.#.",
		"..###..###",
	})

	fTile := tile.flipped(0)

	if fTile.id != tile.id ||
		fTile.left != ".#####..#." || fTile.right != "...#.##..#" ||
		fTile.top != "..##.#..#." || fTile.bottom != "..###..###" {
		t.Fatalf("unexpected flipped tile: %v", fTile)
	}
}

func TestTileFlippedReturnsCorrectTileAfterHorizontalFlip(t *testing.T) {
	tile, _ := parseTileFromLines([]string{
		"Tile 2311:",
		"..##.#..#.",
		"##..#.....",
		"#...##..#.",
		"####.#...#",
		"##.##.###.",
		"##...#.###",
		".#.#.#..##",
		"..#....#..",
		"###...#.#.",
		"..###..###",
	})

	fTile := tile.flipped(1)

	if fTile.id != tile.id ||
		fTile.left != ".#..#####." || fTile.right != "#..##.#..." ||
		fTile.top != "..###..###" || fTile.bottom != "..##.#..#." {
		t.Fatalf("unexpected flipped tile: %v", fTile)
	}
}

func TestTileFlippedReturnsCorrectTileAfterVerticalFlip(t *testing.T) {
	tile, _ := parseTileFromLines([]string{
		"Tile 2311:",
		"..##.#..#.",
		"##..#.....",
		"#...##..#.",
		"####.#...#",
		"##.##.###.",
		"##...#.###",
		".#.#.#..##",
		"..#....#..",
		"###...#.#.",
		"..###..###",
	})

	fTile := tile.flipped(2)

	if fTile.id != tile.id ||
		fTile.left != "...#.##..#" || fTile.right != ".#####..#." ||
		fTile.top != ".#..#.##.." || fTile.bottom != "###..###.." {
		t.Fatalf("unexpected flipped tile: %v", fTile)
	}
}

func TestTileRotatedReturnsCorrectTileAfterNoRotation(t *testing.T) {
	tile, _ := parseTileFromLines([]string{
		"Tile 2311:",
		"..##.#..#.",
		"##..#.....",
		"#...##..#.",
		"####.#...#",
		"##.##.###.",
		"##...#.###",
		".#.#.#..##",
		"..#....#..",
		"###...#.#.",
		"..###..###",
	})

	fTile := tile.rotated(0)

	if fTile.id != tile.id ||
		fTile.left != ".#####..#." || fTile.right != "...#.##..#" ||
		fTile.top != "..##.#..#." || fTile.bottom != "..###..###" {
		t.Fatalf("unexpected rotated tile: %v", fTile)
	}
}

func TestTileRotatedReturnsCorrectTileAfterRotationBy90(t *testing.T) {
	tile, _ := parseTileFromLines([]string{
		"Tile 2311:",
		"..##.#..#.",
		"##..#.....",
		"#...##..#.",
		"####.#...#",
		"##.##.###.",
		"##...#.###",
		".#.#.#..##",
		"..#....#..",
		"###...#.#.",
		"..###..###",
	})

	fTile := tile.rotated(90)

	if fTile.id != tile.id ||
		fTile.left != "..###..###" || fTile.right != "..##.#..#." ||
		fTile.top != ".#..#####." || fTile.bottom != "#..##.#..." {
		t.Fatalf("unexpected rotated tile: %v", fTile)
	}
}

func TestTileRotatedReturnsCorrectTileAfterRotationBy180(t *testing.T) {
	tile, _ := parseTileFromLines([]string{
		"Tile 2311:",
		"..##.#..#.",
		"##..#.....",
		"#...##..#.",
		"####.#...#",
		"##.##.###.",
		"##...#.###",
		".#.#.#..##",
		"..#....#..",
		"###...#.#.",
		"..###..###",
	})

	fTile := tile.rotated(180)

	if fTile.id != tile.id ||
		fTile.left != "#..##.#..." || fTile.right != ".#..#####." ||
		fTile.top != "###..###.." || fTile.bottom != ".#..#.##.." {
		t.Fatalf("unexpected rotated tile: %v", fTile)
	}
}

func TestMultipleIdsOfCornerTilesReturnsCorrectValueForExampleFromAssignment(t *testing.T) {
	tiles, _ := parseTilesFromString(tilesFromAssignment)

	result := tiles.multipleIdsOfCornerTiles()

	if result != 2311*1171*2971*3079 {
		t.Fatalf("unexpected result: %v", result)
	}
}

func TestMultipleIdsOfCornerTilesAfterAssembleReturnsCorrectValueForExampleFromAssignment(t *testing.T) {
	tiles, _ := parseTilesFromString(tilesFromAssignment)

	err := tiles.assemble()
	result := tiles.multipleIdsOfCornerTiles()

	if err != nil {
		t.Fatalf("unexpectedly failed: %v", err)
	}
	if result != 20899048083289 {
		t.Fatalf("unexpected result: %v", result)
	}
}

func TestExportImageAfterAssembleReturnsCorrectImageForExampleFromAssignment(t *testing.T) {
	tiles, _ := parseTilesFromString(tilesFromAssignment)
	expectedImage := Image{
		".####...#####..#...###..",
		"#####..#..#.#.####..#.#.",
		".#.#...#.###...#.##.##..",
		"#.#.##.###.#.##.##.#####",
		"..##.###.####..#.####.##",
		"...#.#..##.##...#..#..##",
		"#.##.#..#.#..#..##.#.#..",
		".###.##.....#...###.#...",
		"#.####.#.#....##.#..#.#.",
		"##...#..#....#..#...####",
		"..#.##...###..#.#####..#",
		"....#.##.#.#####....#...",
		"..##.##.###.....#.##..#.",
		"#...#...###..####....##.",
		".#.##...#.##.#.#.###...#",
		"#.###.#..####...##..#...",
		"#.###...#.##...#.######.",
		".###.###.#######..#####.",
		"..##.#..#..#.#######.###",
		"#.#..##.########..#..##.",
		"#.#####..#.#...##..#....",
		"#....##..#.#########..##",
		"#...#.....#..##...###.##",
		"#..###....##.#...##.##.#",
	}

	err := tiles.assemble()
	image := tiles.exportImage()

	if err != nil {
		t.Fatalf("unexpectedly failed: %v", err)
	}
	if len(image) != 24 || len(image[0]) != 24 {
		t.Fatalf("unexpected image size: %v x %v", len(image), len(image[0]))
	}
	if image.toString() != expectedImage.toString() {
		t.Fatalf("unexpected image:\n%v", image.toString())
	}
}

func TestDetermineMaxWaterRoughnessReturnsCorrectResultForExampleFromAssignment(t *testing.T) {
	tiles, _ := parseTilesFromString(tilesFromAssignment)
	tiles.assemble()
	image := tiles.exportImage()

	waterRoughness := image.determineMaxWaterRoughness()

	if waterRoughness != 273 {
		t.Fatalf("unexpected water roughness: %v", waterRoughness)
	}
}
