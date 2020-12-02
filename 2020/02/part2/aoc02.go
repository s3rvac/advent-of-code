package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"regexp"
	"strconv"
	// "strings"
)

type Password string

// The password policy describes that the given letter has to appear in a
// password at either the first position or the second position.
//
// The positions are 1-based, not 0-based (i.e. 1 means the first letter in a
// string).
type Policy struct {
	letter rune
	pos1   int
	pos2   int
}

type PasswordWithPolicy struct {
	password Password
	policy   Policy
}

type PasswordsWithPolicies []PasswordWithPolicy

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func parsePositionInPasswordPolicy(rawPos string, password Password) (int, error) {
	pos, err := strconv.Atoi(rawPos)
	if err != nil {
		return 0, errors.New("failed to parse position as int")
	} else if pos == 0 || pos > len(password) {
		return 0, errors.New("position is invalid")
	}
	return pos, nil
}

func parsePasswordWithPolicy(input string) (PasswordWithPolicy, error) {
	// Expected input format: "$pos1-$pos2 $letter: $password"
	match := regexp.MustCompile(`^(\d+)-(\d+) ([a-z]): ([a-z]+)$`).FindStringSubmatch(input)
	if len(match) != 5 {
		return PasswordWithPolicy{}, errors.New("input has invalid format")
	}

	password := Password(match[4])

	pos1, err := parsePositionInPasswordPolicy(match[1], password)
	if err != nil {
		return PasswordWithPolicy{}, err
	}

	pos2, err := parsePositionInPasswordPolicy(match[2], password)
	if err != nil {
		return PasswordWithPolicy{}, err
	}

	letter := []rune(match[3])[0]

	return PasswordWithPolicy{password, Policy{letter, pos1, pos2}}, nil
}

func loadInput() PasswordsWithPolicies {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc02 INPUT_FILE")
		os.Exit(1)
	}

	file, err := os.Open(os.Args[1])
	if err != nil {
		printErrorAndExit(err)
	}
	defer file.Close()

	var input PasswordsWithPolicies
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		passwordWithPolicy, err := parsePasswordWithPolicy(line)
		if err != nil {
			printErrorAndExit(err)
		}
		input = append(input, passwordWithPolicy)
	}
	return input
}

func isPasswordWithPolicyValid(passwordWithPolicy PasswordWithPolicy) bool {
	password := []rune(string(passwordWithPolicy.password))
	policy := passwordWithPolicy.policy
	pos1Matches := password[policy.pos1-1] == policy.letter
	pos2Matches := password[policy.pos2-1] == policy.letter
	// Either of the two positions has to match, but not both.
	return pos1Matches != pos2Matches
}

func validatePasswordsWithPolicies(passwordsWithPolicies PasswordsWithPolicies) int {
	validPasswordCount := 0
	for _, passwordWithPolicy := range passwordsWithPolicies {
		if isPasswordWithPolicyValid(passwordWithPolicy) {
			validPasswordCount++
		}
	}
	return validPasswordCount
}

func main() {
	passwordsWithPolicies := loadInput()
	validPasswordCount := validatePasswordsWithPolicies(passwordsWithPolicies)
	fmt.Println(validPasswordCount)
}
