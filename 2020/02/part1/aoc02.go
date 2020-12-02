package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Password string

// The password policy indicates the lowest and highest number of times a given
// letter must appear for the password to be valid.
type Policy struct {
	letter  rune
	atLeast int
	atMost  int
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

func parsePasswordWithPolicy(input string) (PasswordWithPolicy, error) {
	// Expected input format: "$atLeast-$atMost $letter: $password"
	match := regexp.MustCompile(`^(\d+)-(\d+) ([a-z]): ([a-z]+)$`).FindStringSubmatch(input)
	if len(match) != 5 {
		return PasswordWithPolicy{}, errors.New("input has invalid format")
	}

	atLeast, err := strconv.Atoi(match[1])
	if err != nil {
		return PasswordWithPolicy{}, errors.New("failed to parse the lower bound as int")
	}

	atMost, err := strconv.Atoi(match[2])
	if err != nil {
		return PasswordWithPolicy{}, errors.New("failed to parse the upper bound as int")
	}

	if atMost < atLeast {
		return PasswordWithPolicy{}, errors.New("upper bound cannot be greater than lower bound")
	}

	letter := []rune(match[3])[0]
	password := Password(match[4])
	policy := Policy{letter, atLeast, atMost}
	return PasswordWithPolicy{password, policy}, nil
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
	password := passwordWithPolicy.password
	policy := passwordWithPolicy.policy
	letterCount := strings.Count(string(password), string(policy.letter))
	return letterCount >= policy.atLeast && letterCount <= policy.atMost
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
