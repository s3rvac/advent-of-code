package main

import "testing"

func TestParseAdapterJoltagesFromStringReturnsCorrectValueWhenInputStringIsValid(t *testing.T) {
	adapterJoltages, err := parseJoltagesFromString("1\n2\n3")

	if err != nil {
		t.Fatalf("unexpectedly failed: %s", err)
	}
	if len(adapterJoltages) != 3 || adapterJoltages[0] != 1 || adapterJoltages[1] != 2 || adapterJoltages[2] != 3 {
		t.Fatalf("unexpected adapter joltages: %v", adapterJoltages)
	}
}

func TestParseAdapterJoltagesFromStringReturnsErrorWhenInputStringIsInvalid(t *testing.T) {
	_, err := parseJoltagesFromString("xxx")

	if err == nil {
		t.Fatalf("unexpectedly succeeded")
	}
}

func TestFindChainThatUsesAllAdaptersReturnsCorrectResultForExampleFromAssignment(t *testing.T) {
	adapterJoltages, _ := parseJoltagesFromString(
		`16
10
15
5
1
11
7
19
6
12
4`,
	)

	chain := findChainThatUsesAllAdapters(adapterJoltages)

	if len(chain) != 13 {
		t.Fatalf("unexpected chain: %v", chain)
	}
	if chain[0] != 0 || chain[1] != 1 || chain[2] != 4 || chain[3] != 5 || chain[4] != 6 ||
		chain[5] != 7 || chain[6] != 10 || chain[7] != 11 || chain[8] != 12 || chain[9] != 15 ||
		chain[10] != 16 || chain[11] != 19 || chain[12] != 22 {
		t.Fatalf("unexpected chain: %v", chain)
	}
}

func TestCountAllDistinctAdapterArrangementsReturnsCorrectResultForFirstExampleFromAssignment(t *testing.T) {
	adapterJoltages, _ := parseJoltagesFromString(
		`16
10
15
5
1
11
7
19
6
12
4`,
	)
	chain := findChainThatUsesAllAdapters(adapterJoltages)

	result := countAllDistinctAdapterArrangements(chain)

	if result != 8 {
		t.Fatalf("unexpected result: %v", result)
	}
}

func TestCountAllDistinctAdapterArrangementsReturnsCorrectResultForSecondExampleFromAssignment(t *testing.T) {
	adapterJoltages, _ := parseJoltagesFromString(
		`28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3`,
	)
	chain := findChainThatUsesAllAdapters(adapterJoltages)

	result := countAllDistinctAdapterArrangements(chain)

	if result != 19208 {
		t.Fatalf("unexpected result: %v", result)
	}
}
