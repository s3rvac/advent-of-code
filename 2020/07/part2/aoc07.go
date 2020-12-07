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

func (rules *BagRules) getBagColorCount() int {
	// There is a rule for each bag, so it suffices to return the rule count.
	return rules.getRuleCount()
}

func (rules *BagRules) getDirectContainmentCount(outerBagColor string, innerBagColor string) int {
	return rules.m[outerBagColor][innerBagColor]
}

func (rules *BagRules) howManyBagsAreRequiredIn(requestedBagColor string) int {
	counts := make(map[string]int)

	// Iteratively compute the counts until we have all of them.
	for len(counts) < rules.getBagColorCount() {
		for outerBagColor, innerBagColors := range rules.m {
			// No contained bags:
			if len(innerBagColors) == 0 {
				counts[outerBagColor] = 0
			}

			// With contained bags:
			outerBagHasAllColorCountsComputed := true
			totalCountForOuterBag := 0
			for innerBagColor, innerBagCount := range innerBagColors {
				count, hasCount := counts[innerBagColor]
				if hasCount {
					// Direct bags:
					totalCountForOuterBag += innerBagCount
					// Indirect bags from inner bag:
					totalCountForOuterBag += innerBagCount * count
				} else {
					outerBagHasAllColorCountsComputed = false
				}
			}
			if outerBagHasAllColorCountsComputed {
				counts[outerBagColor] = totalCountForOuterBag
			}
		}
	}

	return counts[requestedBagColor]
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
	count := bagRules.howManyBagsAreRequiredIn("shiny gold")
	fmt.Println(count)
}
