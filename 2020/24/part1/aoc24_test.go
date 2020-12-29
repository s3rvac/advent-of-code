package main

import "testing"

func TestParseTilesDirectionsFromStringReturnsCorrectRepresentation(t *testing.T) {
	tilesDirections, err := parseTilesDirectionsFromString(
		`esesww
nwne
`,
	)

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(tilesDirections) != 2 || len(tilesDirections[0]) != 4 ||
		tilesDirections[0][0] != "e" || len(tilesDirections[1]) != 2 || tilesDirections[1][0] != "nw" {
		t.Fatalf("unexpected tiles directions: %v", tilesDirections)
	}
}

func TestFlipTilesByDirectionsAndCountBlackTilesReturnsCorrectCountForExampleFromAssignment(t *testing.T) {
	tilesDirections, _ := parseTilesDirectionsFromString(
		`sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
`,
	)
	grid := createNewGrid()

	grid.flipTilesByDirections(tilesDirections)
	count := grid.countBlackTiles()

	if count != 10 {
		t.Fatalf("unexpected count: %v", count)
	}
}
