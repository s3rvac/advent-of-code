package main

import "testing"

func TestCreateBagRulesFromStringReturnsErrorWhenBagRuleIsInvalid(t *testing.T) {
	_, err := createBagRulesFromString("xxx")

	if err == nil {
		t.Fatalf("unexpectedly succeeded")
	}
}

func TestCreateBagRulesFromStringReturnsCorrectBagRulesForEmptyString(t *testing.T) {
	bagRules, err := createBagRulesFromString("")

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	ruleCount := bagRules.getRuleCount()
	if ruleCount != 0 {
		t.Fatalf("unexpected rule count: %v", ruleCount)
	}
}

func TestCreateBagRulesFromStringReturnsCorrectBagRulesForSingleBagContainingSingleBag(t *testing.T) {
	bagRules, err := createBagRulesFromString("bright white bags contain 1 shiny gold bag.")

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	ruleCount := bagRules.getRuleCount()
	if ruleCount != 1 {
		t.Fatalf("unexpected rule count: %v", ruleCount)
	}
	n := bagRules.getDirectContainmentCount("bright white", "shiny gold")
	if n != 1 {
		t.Fatalf("unexpected number of bags: %v", n)
	}
}

func TestCreateBagRulesFromStringReturnsCorrectBagRulesForSingleBagContainingMultipleBags(t *testing.T) {
	bagRules, err := createBagRulesFromString("dark orange bags contain 3 bright white bags, 4 muted yellow bags.")

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	ruleCount := bagRules.getRuleCount()
	if ruleCount != 1 {
		t.Fatalf("unexpected rule count: %v", ruleCount)
	}
	m := bagRules.getDirectContainmentCount("dark orange", "bright white")
	if m != 3 {
		t.Fatalf("unexpected number of bags: %v", m)
	}
	n := bagRules.getDirectContainmentCount("dark orange", "muted yellow")
	if n != 4 {
		t.Fatalf("unexpected number of bags: %v", n)
	}
}

func TestCreateBagRulesFromStringReturnsCorrectBagRulesForSingleBagContainingNoBags(t *testing.T) {
	bagRules, err := createBagRulesFromString("faded blue bags contain no other bags.")

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	ruleCount := bagRules.getRuleCount()
	if ruleCount != 1 {
		t.Fatalf("unexpected rule count: %v", ruleCount)
	}
	n := bagRules.getDirectContainmentCount("faded blue", "shiny gold")
	if n != 0 {
		t.Fatalf("unexpected number of bags: %v", n)
	}
}

func TestCreateBagRulesFromStringReturnsCorrectBagRulesForExampleFromAssignment(t *testing.T) {
	bagRules, err := createBagRulesFromString(
		`light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.`,
	)

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	ruleCount := bagRules.getRuleCount()
	if ruleCount != 9 {
		t.Fatalf("unexpected rule count: %v", ruleCount)
	}
	// Check just one of the rules.
	n := bagRules.getDirectContainmentCount("vibrant plum", "dotted black")
	if n != 6 {
		t.Fatalf("unexpected number of bags: %v", n)
	}
}

func TestHowManyBagsAreRequiredInReturnsCorrectResultWhenThereAreNoBags(t *testing.T) {
	bagRules, err := createBagRulesFromString("")

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	count := bagRules.howManyBagsAreRequiredIn("light red")
	if count != 0 {
		t.Fatalf("unexpected count: %v", count)
	}
}

func TestHowManyBagsAreRequiredInReturnsCorrectResultWhenBagDoesNotHaveToContainAnyOtherBags(t *testing.T) {
	bagRules, err := createBagRulesFromString("dark violet bags contain no other bags.")

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	count := bagRules.howManyBagsAreRequiredIn("dark violet")
	if count != 0 {
		t.Fatalf("unexpected count: %v", count)
	}
}

func TestHowManyBagsAreRequiredInReturnsCorrectResultWhenBagNeedsToContainOneBagWithNoDependencies(t *testing.T) {
	bagRules, err := createBagRulesFromString(
		`pale blue bags contain 1 dark violet bag.
dark violet bags contain no other bags.`,
	)

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	count := bagRules.howManyBagsAreRequiredIn("pale blue")
	if count != 1 {
		t.Fatalf("unexpected count: %v", count)
	}
}

func TestHowManyBagsAreRequiredInReturnsCorrectResultForExampleFromAssignment(t *testing.T) {
	bagRules, err := createBagRulesFromString(
		`shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.`,
	)

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	count := bagRules.howManyBagsAreRequiredIn("shiny gold")
	if count != 126 {
		t.Fatalf("unexpected count: %v", count)
	}
}
