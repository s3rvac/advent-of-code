package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"strconv"
)

type Deck []int

func parseDecksFromString(s string) (Deck, Deck, error) {
	parsingDeck := 1
	deck1 := make(Deck, 0)
	deck2 := make(Deck, 0)

	for _, line := range strings.Split(s, "\n") {
		if len(line) == 0 {
			// Separator between decks.
			parsingDeck = 2
			continue
		} else if strings.HasPrefix(line, "Player ") {
			continue
		}

		card, err := strconv.Atoi(line)
		if err != nil {
			return nil, nil, errors.New(fmt.Sprintf("invalid card: %s", line))
		}

		if parsingDeck == 1 {
			deck1 = append(deck1, card)
		} else {
			deck2 = append(deck2, card)
		}
	}

	return deck1, deck2, nil
}

func (deck Deck) copy() Deck {
	deckCopy := make(Deck, len(deck))
	copy(deckCopy, deck)
	return deckCopy
}

func (deck Deck) computeScore() int {
	score := 0
	for i := 0; i < len(deck); i++ {
		score += deck[i] * (len(deck) - i)
	}
	return score
}

func (deck Deck) getAndRemoveTopCard() (int, Deck) {
	topCard := deck[0]
	return topCard, deck[1:]
}

func (deck Deck) placeCardsToBottom(card1 int, card2 int) Deck {
	return append(deck, card1, card2)
}

func playRound(deck1 Deck, deck2 Deck, playedDecks map[string]bool) (int, Deck, Deck) {
	decksConfig := fmt.Sprintf("%v:%v", deck1, deck2)
	if _, exists := playedDecks[decksConfig]; exists {
		// There was a round with exactly the same configurations of decks. The
		// game instantly ends with a win for player 1.
		return 1, deck1, deck2
	}
	playedDecks[decksConfig] = true

	top1, deck1 := deck1.getAndRemoveTopCard()
	top2, deck2 := deck2.getAndRemoveTopCard()

	winnerOfRound := 0
	if len(deck1) >= top1 && len(deck2) >= top2 {
		// Play a recursive game to determine the winner of the round.
		winnerOfRound, _ = playGame(deck1[:top1].copy(), deck2[:top2].copy())
	} else {
		// It is a regular round.
		if top1 > top2 {
			winnerOfRound = 1
		} else {
			winnerOfRound = 2
		}
	}

	if winnerOfRound == 1 {
		deck1 = deck1.placeCardsToBottom(top1, top2)
	} else {
		deck2 = deck2.placeCardsToBottom(top2, top1)
	}

	return 0, deck1, deck2
}

func playGame(deck1 Deck, deck2 Deck) (int, int) {
	winner := 0
	playedDecks := make(map[string]bool)

	for len(deck1) != 0 && len(deck2) != 0 && winner == 0 {
		winner, deck1, deck2 = playRound(deck1, deck2, playedDecks)
	}

	if winner == 1 || len(deck2) == 0 {
		return 1, deck1.computeScore()
	} else {
		return 2, deck2.computeScore()
	}
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputFileContent() string {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc22 INPUT_FILE")
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
	deck1, deck2, err := parseDecksFromString(input)
	if err != nil {
		printErrorAndExit(err)
	}
	_, winningScore := playGame(deck1, deck2)
	fmt.Println(winningScore)
}
