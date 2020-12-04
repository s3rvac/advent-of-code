package main

import "testing"

func TestPassportFromStringReturnsCorrectPassportFromEmptyLine(t *testing.T) {
	p := passportFromString("")

	if p.toString() != "" {
		t.Fatalf("invalid parse: %v", p.toString())
	}
}

func TestPassportFromStringReturnsCorrectPassportFromFullLine(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 cid:147 hgt:183cm",
	)

	if p.toString() != "byr:1937 iyr:2017 eyr:2020 hgt:183cm hcl:#fffffd ecl:gry pid:860033327 cid:147" {
		t.Fatalf("invalid parse: %v", p.toString())
	}
}

func TestPassportIsValidReturnsTrueForPassportHavingAllFields(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 cid:147 hgt:183cm",
	)

	isValid := p.isValid()

	if !isValid {
		t.Fatalf("passport unexpectedly invalid")
	}
}

func TestPassportIsValidReturnsTrueForPassportHavingAllFieldsButCid(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 hgt:183cm",
	)

	isValid := p.isValid()

	if !isValid {
		t.Fatalf("passport unexpectedly invalid")
	}
}

func TestPassportIsValidReturnsFalseForPassportNotHavingMandatoryField(t *testing.T) {
	// ecl is missing
	p := passportFromString(
		"pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 cid:147 hgt:183cm",
	)

	isValid := p.isValid()

	if isValid {
		t.Fatalf("passport unexpectedly valid")
	}
}

func TestCountValidPassportsReturnsCorrectCountForExampleFromAssignemtn(t *testing.T) {
	passports := []Passport{
		passportFromString("ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 cid:147 hgt:183cm"),
		passportFromString("iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884 hcl:#cfa07d byr:1929"),
		passportFromString("hcl:#ae17e1 iyr:2013 eyr:2024 ecl:brn pid:760753108 byr:1931 hgt:179cm"),
		passportFromString("hcl:#cfa07d eyr:2025 pid:166559648 iyr:2011 ecl:brn hgt:59in"),
	}

	count := coundValidPassports(passports)

	if count != 2 {
		t.Fatalf("unexpected count: %v", count)
	}
}
