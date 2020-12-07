package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type BagRules struct {
	// outer bag -> (inner bag -> occurrence count)
	m map[string]map[string]int
}

func createBagRulesFromString(s string) (*BagRules, error) {
	rules := BagRules{make(map[string]map[string]int)}

	lines := strings.Split(s, "\n")
	for _, line := range lines {
		if len(line) > 0 {
			err := rules.addRuleFromString(line)
			if err != nil {
				return &rules, err
			}
		}
	}

	return &rules, nil
}

func (rules *BagRules) addRuleFromString(s string) error {
	m := regexp.MustCompile(`^([a-z ]+) bags contain (.+)\.$`).FindStringSubmatch(s)
	if len(m) != 3 {
		return errors.New(fmt.Sprintf("invalid bag rule: %s", s))
	}

	outerBagColor := m[1]
	rules.m[outerBagColor] = make(map[string]int)

	innerBagSpecs := strings.Split(m[2], ", ")
	if len(innerBagSpecs) == 1 && innerBagSpecs[0] == "no other bags" {
		return nil
	}

	for _, innerBagSpec := range innerBagSpecs {
		m := regexp.MustCompile(`^(\d+) ([a-z ]+) bags?$`).FindStringSubmatch(innerBagSpec)
		if len(m) != 3 {
			return errors.New(fmt.Sprintf("invalid bag rule: %s", s))
		}
		innerBagCount, err := strconv.Atoi(m[1])
		if err != nil {
			return errors.New(fmt.Sprintf("invalid bag rule: %s", s))
		}
		innerBagColor := m[2]
		rules.m[outerBagColor][innerBagColor] = innerBagCount
	}
	return nil
}

func (rules *BagRules) getRuleCount() int {
	return len(rules.m)
}

func (rules *BagRules) getDirectContainmentCount(outerBagColor string, innerBagColor string) int {
	return rules.m[outerBagColor][innerBagColor]
}

func (rules *BagRules) howManyBagsCanContainBag(requestedBagColor string) int {
	// Go does not have sets, so we have to use a map.
	canContainRequestedBag := make(map[string]bool)

	// Iteratively compute the possibilities until a fixed point is reached.
	for {
		origBagCount := len(canContainRequestedBag)

		for outerBagColor, innerBagColors := range rules.m {
			for innerBagColor, _ := range innerBagColors {
				// Direct containment.
				if innerBagColor == requestedBagColor {
					canContainRequestedBag[outerBagColor] = true
				}
				// Indirect containment.
				if _, ok := canContainRequestedBag[innerBagColor]; ok {
					canContainRequestedBag[outerBagColor] = true
				}
			}
		}

		if len(canContainRequestedBag) == origBagCount {
			// We have reached a fixed point.
			break
		}
	}

	return len(canContainRequestedBag)
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputFileContent() string {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc07 INPUT_FILE")
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
	bagRules, err := createBagRulesFromString(input)
	if err != nil {
		printErrorAndExit(err)
	}
	count := bagRules.howManyBagsCanContainBag("shiny gold")
	fmt.Println(count)
}
