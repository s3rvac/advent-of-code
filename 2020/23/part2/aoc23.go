package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

type Cup int

type Cups []Cup

// For performance reasons, we use two cup buffers, and switch between them
// during each round. This allows us to use a fixed amount of memory, without a
// need to create new slices.
type Game struct {
	// The currently used buffer.
	cups Cups
	// The next buffer to use.
	nextCups Cups
	// The total number of cups in the buffers.
	cupCount int
	// The current cup (label).
	currCup Cup
	// The index of the current cup.
	currCupIdx int
	// Minimal cup (label).
	minCup Cup
	// Maximal cup (label).
	maxCup Cup
}

const noCup = Cup(0)

func parseGameFromString(s string) (Game, error) {
	game := Game{}

	for _, c := range strings.Trim(s, "\n") {
		c, err := strconv.Atoi(string(c))
		if err != nil {
			return game, errors.New(fmt.Sprintf("invalid string: %s", s))
		}
		game.addCup(Cup(c))
	}

	return game, nil
}

func (game *Game) padCupsWithCupNumbersUpTo(n Cup) {
	for c := game.maxCup + 1; c <= n; c++ {
		game.addCup(c)
	}
}

func (game *Game) addCup(cup Cup) {
	if game.minCup == 0 || cup < game.minCup {
		game.minCup = cup
	}
	if game.maxCup == 0 || cup > game.maxCup {
		game.maxCup = cup
	}
	game.cups = append(game.cups, cup)
	game.nextCups = append(game.nextCups, cup)
	if game.currCup == 0 {
		game.currCupIdx = 0
		game.currCup = game.cups[0]
	}
	game.cupCount++
}

func (game *Game) nextIndexFrom(i int) int {
	return (i + 1) % game.cupCount
}

func (game *Game) findCupIndex(cupToFind Cup) int {
	for i := 0; i < game.cupCount; i++ {
		if game.cups[i] == cupToFind {
			return i
		}
	}
	return -1
}

func (game *Game) performMove() {
	// Take 3 cups.
	takenCups := [3]Cup{noCup, noCup, noCup}
	i := game.currCupIdx
	j := 0
	for x := 0; x < 3; x++ {
		i = game.nextIndexFrom(i)
		takenCup := game.cups[i]
		game.cups[i] = noCup
		takenCups[j] = takenCup
		j++
	}

	// Select a destination cup.
	destinationCup := game.currCup
	for {
		destinationCup -= 1
		if destinationCup < game.minCup {
			destinationCup = game.maxCup
		}

		if destinationCup != takenCups[0] &&
			destinationCup != takenCups[1] &&
			destinationCup != takenCups[2] {
			break
		}
	}

	// Place the taken cups after the destination cup in the new buffer.
	destinationCupIdx := game.findCupIndex(destinationCup)
	// Order:
	// 1) Cups up to the destination cup (including).
	dst := 0
	for src := 0; src <= destinationCupIdx; src++ {
		cup := game.cups[src]
		if cup != noCup {
			game.nextCups[dst] = cup
			dst++
		}
	}
	// 2) Taken cups.
	for i := 0; i < len(takenCups); i++ {
		game.nextCups[dst] = takenCups[i]
		dst++
	}
	// 3) Cups after the destination cup.
	for src := destinationCupIdx + 1; src < game.cupCount; src++ {
		cup := game.cups[src]
		if cup != noCup {
			game.nextCups[dst] = cup
			dst++
		}
	}

	// Switch to the next buffer.
	game.cups, game.nextCups = game.nextCups, game.cups

	// Select a new current cup.
	game.currCupIdx = game.nextIndexFrom(game.findCupIndex(game.currCup))
	game.currCup = game.cups[game.currCupIdx]
}

func (game *Game) performMoves(moveCount int) {
	for n := 0; n < moveCount; n++ {
		game.performMove()
	}
}

func (game *Game) multiplyTwoCupLabelsAfterGivenCup(cup Cup) Cup {
	i := game.findCupIndex(cup)
	i = game.nextIndexFrom(i)
	first := game.cups[i]
	i = game.nextIndexFrom(i)
	second := game.cups[i]
	return first * second
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputFileContent() string {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc23 INPUT_FILE")
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
	game, err := parseGameFromString(input)
	if err != nil {
		printErrorAndExit(err)
	}
	game.padCupsWithCupNumbersUpTo(1_000_000)
	game.performMoves(10_000_000)
	result := game.multiplyTwoCupLabelsAfterGivenCup(1)
	fmt.Println(result)
}
