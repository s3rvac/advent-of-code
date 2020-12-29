package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

type Key int

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func parsePublicKeyFromString(s string) (Key, error) {
	key, err := strconv.Atoi(s)
	return Key(key), err
}

func parsePublicKeysFromString(s string) (Key, Key, error) {
	lines := strings.Split(strings.Trim(s, "\n"), "\n")
	if len(lines) != 2 {
		return 0, 0, errors.New(fmt.Sprintf("invalid input: %s", s))
	}

	cardPK, err := parsePublicKeyFromString(lines[0])
	if err != nil {
		return 0, 0, errors.New(fmt.Sprintf("invalid card's public key: %s", lines[0]))
	}

	doorPK, err := parsePublicKeyFromString(lines[1])
	if err != nil {
		return 0, 0, errors.New(fmt.Sprintf("invalid door's public key: %s", lines[1]))
	}

	return cardPK, doorPK, nil
}

func advanceKey(key Key, subjectNumber Key) Key {
	return key * subjectNumber % Key(20201227)
}

func computeLoopSizeForKey(publicKey Key, subjectNumber Key) int {
	loopSize := 0
	for key := Key(1); key != publicKey; loopSize++ {
		key = advanceKey(key, subjectNumber)
	}
	return loopSize
}

func computeEncryptionKey(cardPK Key, doorPK Key) Key {
	cardLoopSize := computeLoopSizeForKey(cardPK, 7)

	encryptionKey := Key(1)
	for i := 0; i < cardLoopSize; i++ {
		encryptionKey = advanceKey(encryptionKey, doorPK)
	}
	return encryptionKey
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
	cardPK, doorPK, err := parsePublicKeysFromString(input)
	if err != nil {
		printErrorAndExit(err)
	}
	encryptionKey := computeEncryptionKey(cardPK, doorPK)
	fmt.Println(encryptionKey)
}
