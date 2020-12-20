package main

import "testing"

func TestParseRulesAndMessagesFromStringCorrectlyParsesValidInputString(t *testing.T) {
	rules, messages, err := parseRulesAndMessagesFromString(
		`0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
`,
	)

	if err != nil {
		t.Fatalf("unexpectedly failed: %v", err)
	}
	if rules.ruleCount() != 6 {
		t.Fatalf("invalid rules: %v", rules)
	}
	if len(messages) != 5 || messages[0] != "ababbb" || messages[4] != "aaaabbb" {
		t.Fatalf("invalid messages: %v", messages)
	}
}

func TestIsValidMessageReturnsTrueForValidMessage(t *testing.T) {
	rules, messages, _ := parseRulesAndMessagesFromString(
		`0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
`,
	)

	if !rules.isValidMessage(messages[0]) {
		t.Fatalf("message %s unexpectedly determined as invalid", messages[0])
	}
	if !rules.isValidMessage(messages[2]) {
		t.Fatalf("message %s unexpectedly determined as invalid", messages[2])
	}
}

func TestIsValidMessageReturnsFalseForInvalidMessage(t *testing.T) {
	rules, messages, _ := parseRulesAndMessagesFromString(
		`0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
`,
	)

	if rules.isValidMessage(messages[1]) {
		t.Fatalf("message %s unexpectedly determined as valid", messages[0])
	}
	if rules.isValidMessage(messages[3]) {
		t.Fatalf("message %s unexpectedly determined as valid", messages[2])
	}
	if rules.isValidMessage(messages[4]) {
		t.Fatalf("message %s unexpectedly determined as valid", messages[4])
	}
}

func TestComputeValidMessageCountReturnsCorrectCountForExampleFromAssignment(t *testing.T) {
	rules, messages, _ := parseRulesAndMessagesFromString(
		`0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
`,
	)

	count := rules.computeValidMessageCount(messages)

	if count != 2 {
		t.Fatalf("unexpected count: %v", count)
	}
}
