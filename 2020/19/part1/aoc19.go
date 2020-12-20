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

type Rule struct {
	id       int
	subRules []RuleIds
	char     string
}

type RuleIds []int

type Rules struct {
	ruleMap map[int]Rule
}

func (rules *Rules) ruleCount() int {
	return len(rules.ruleMap)
}

type Message string

type Messages []Message

func parseRulesAndMessagesFromString(s string) (*Rules, Messages, error) {
	messages := make(Messages, 0)
	rules := Rules{make(map[int]Rule)}

	parsingMessages := false
	lines := strings.Split(s, "\n")
	for _, line := range lines {
		if len(line) == 0 {
			// We have reached the delimiter between rules and messages.
			parsingMessages = true
			continue
		} else if parsingMessages {
			message, err := parseMessagesFromString(line)
			if err != nil {
				return &rules, messages, err
			}
			messages = append(messages, message)
		} else {
			rule, err := parseRuleFromString(line)
			if err != nil {
				return &rules, messages, err
			}
			rules.ruleMap[rule.id] = rule
		}
	}

	return &rules, messages, nil
}

func parseRuleFromString(s string) (Rule, error) {
	idAndRhs := strings.Split(s, ": ")
	if len(idAndRhs) != 2 {
		return Rule{}, errors.New(fmt.Sprintf("invalid rule: %s", s))
	}

	id, err := strconv.Atoi(idAndRhs[0])
	if err != nil {
		return Rule{}, errors.New(fmt.Sprintf("invalid rule: %s", s))
	}

	rhs := idAndRhs[1]
	if rhs == "\"a\"" || rhs == "\"b\"" {
		return Rule{id, nil, string(rhs[1])}, nil
	}

	subRules := make([]RuleIds, 0)
	m := regexp.MustCompile(`^([\d ]+) \| ([\d ]+)$`).FindStringSubmatch(rhs)
	if len(m) == 3 {
		// 0: 1 2 | 3 4
		//    ^^^   ^^^
		//    m[1]  m[2]
		for _, i := range []int{1, 2} {
			subRule, err := parseSubRule(m[i])
			if err != nil {
				return Rule{}, errors.New(fmt.Sprintf("invalid rule: %s", s))
			}
			subRules = append(subRules, subRule)
		}
	} else {
		// 0: 1 2 3
		//    ^^^^^
		//     rhs
		subRule, err := parseSubRule(rhs)
		if err != nil {
			return Rule{}, errors.New(fmt.Sprintf("invalid rule: %s", s))
		}
		subRules = append(subRules, subRule)
	}

	return Rule{id, subRules, ""}, nil
}

func parseSubRule(s string) (RuleIds, error) {
	// What we are parsing in this function:
	//
	//     0: 1 2 | 3 4
	//        ^^^
	ruleIds := make(RuleIds, 0)

	rawRuleIds := strings.Split(s, " ")
	for _, rawRuleId := range rawRuleIds {
		ruleId, err := strconv.Atoi(rawRuleId)
		if err != nil {
			return nil, err
		}
		ruleIds = append(ruleIds, ruleId)
	}

	return ruleIds, nil
}

func parseMessagesFromString(s string) (Message, error) {
	if regexp.MustCompile(`^[ab]+$`).MatchString(s) {
		return Message(s), nil
	}
	return "", errors.New(fmt.Sprintf("invalid message: %s", s))
}

func joinRuleIds(ruleIds1 []int, ruleIds2 []int) []int {
	joined := make([]int, 0, len(ruleIds1)+len(ruleIds2))
	joined = append(joined, ruleIds1...)
	joined = append(joined, ruleIds2...)
	return joined
}

func (rules *Rules) matchMessageByRules(message Message, toMatch []int) bool {
	if len(message) == 0 || len(toMatch) == 0 {
		// We have reached the end (either successfully or unsuccessfully,
		// depending on if everything has been matched).
		return len(message) == 0 && len(toMatch) == 0
	}

	if len(toMatch) > len(message) {
		// There is no point in continuing as there are more rules to match
		// than the message length (and there are no erasing rules).
		return false
	}

	rule := rules.ruleMap[toMatch[0]]
	if rule.char != "" && rule.char == string(message[0]) {
		// We have successfully matched the first character. Try to match the
		// rest of the message.
		return rules.matchMessageByRules(message[1:], toMatch[1:])
	}

	for _, subRule := range rule.subRules {
		// In order for the rule to match, any of its subrules have to match.
		if rules.matchMessageByRules(message, joinRuleIds(subRule, toMatch[1:])) {
			return true
		}
	}

	return false
}

func (rules *Rules) isValidMessage(message Message) bool {
	// A valid message is the one that matches rule 0.
	return rules.matchMessageByRules(message, []int{0})
}

func (rules *Rules) computeValidMessageCount(messages Messages) int {
	count := 0
	for _, message := range messages {
		if rules.isValidMessage(message) {
			count++
		}
	}
	return count
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputFileContent() string {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc19 INPUT_FILE")
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
	rules, messages, err := parseRulesAndMessagesFromString(input)
	if err != nil {
		printErrorAndExit(err)
	}
	validMessagesCount := rules.computeValidMessageCount(messages)
	fmt.Println(validMessagesCount)
}
