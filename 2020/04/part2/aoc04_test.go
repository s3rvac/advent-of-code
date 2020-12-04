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

func TestPassportIsValidReturnsFalseForPassportWithByrInInvalidFormat(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:x937 iyr:2017 hgt:183cm",
		//                                          ^^^^^^^^
	)

	isValid := p.isValid()

	if isValid {
		t.Fatalf("passport unexpectedly valid")
	}
}

func TestPassportIsValidReturnsFalseForPassportWithByrThatIsTooLow(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1919 iyr:2017 hgt:183cm",
		//                                          ^^^^^^^^
	)

	isValid := p.isValid()

	if isValid {
		t.Fatalf("passport unexpectedly valid")
	}
}

func TestPassportIsValidReturnsFalseForPassportWithByrThatIsTooHigh(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:2003 iyr:2017 hgt:183cm",
		//                                          ^^^^^^^^
	)

	isValid := p.isValid()

	if isValid {
		t.Fatalf("passport unexpectedly valid")
	}
}

func TestPassportIsValidReturnsFalseForPassportWithIyrInInvalidFormat(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:x017 hgt:183cm",
		//                                                   ^^^^^^^^
	)

	isValid := p.isValid()

	if isValid {
		t.Fatalf("passport unexpectedly valid")
	}
}

func TestPassportIsValidReturnsFalseForPassportWithIyrTooLow(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2009 hgt:183cm",
		//                                                   ^^^^^^^^
	)

	isValid := p.isValid()

	if isValid {
		t.Fatalf("passport unexpectedly valid")
	}
}

func TestPassportIsValidReturnsFalseForPassportWithIyrTooHigh(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2021 hgt:183cm",
		//                                                   ^^^^^^^^
	)

	isValid := p.isValid()

	if isValid {
		t.Fatalf("passport unexpectedly valid")
	}
}

func TestPassportIsValidReturnsFalseForPassportWithEyrInInvalidFormat(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:860033327 eyr:x020 hcl:#fffffd byr:1937 iyr:2017 hgt:183cm",
		//                     ^^^^^^^^
	)

	isValid := p.isValid()

	if isValid {
		t.Fatalf("passport unexpectedly valid")
	}
}

func TestPassportIsValidReturnsFalseForPassportWithEyrTooLow(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:860033327 eyr:2019 hcl:#fffffd byr:1937 iyr:2017 hgt:183cm",
		//                     ^^^^^^^^
	)

	isValid := p.isValid()

	if isValid {
		t.Fatalf("passport unexpectedly valid")
	}
}

func TestPassportIsValidReturnsFalseForPassportWithEyrTooHigh(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:860033327 eyr:2031 hcl:#fffffd byr:1937 iyr:2017 hgt:183cm",
		//                     ^^^^^^^^
	)

	isValid := p.isValid()

	if isValid {
		t.Fatalf("passport unexpectedly valid")
	}
}

func TestPassportIsValidReturnsFalseForPassportWithHgtInInvalidUnits(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 hgt:183xx",
		//                                                            ^^^^^^^^^
	)

	isValid := p.isValid()

	if isValid {
		t.Fatalf("passport unexpectedly valid")
	}
}

func TestPassportIsValidReturnsFalseForPassportWithHgtInInvalidValue(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 hgt:x83cm",
		//                                                            ^^^^^^^^^
	)

	isValid := p.isValid()

	if isValid {
		t.Fatalf("passport unexpectedly valid")
	}
}

func TestPassportIsValidReturnsFalseForPassportWithHgtInCmTooLow(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 hgt:149cm",
		//                                                            ^^^^^^^^^
	)

	isValid := p.isValid()

	if isValid {
		t.Fatalf("passport unexpectedly valid")
	}
}

func TestPassportIsValidReturnsFalseForPassportWithHgtInCmTooHigh(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 hgt:194cm",
		//                                                            ^^^^^^^^^
	)

	isValid := p.isValid()

	if isValid {
		t.Fatalf("passport unexpectedly valid")
	}
}

func TestPassportIsValidReturnsFalseForPassportWithHgtInInTooLow(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 hgt:58in",
		//                                                            ^^^^^^^^
	)

	isValid := p.isValid()

	if isValid {
		t.Fatalf("passport unexpectedly valid")
	}
}

func TestPassportIsValidReturnsFalseForPassportWithHgtInInTooHigh(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 hgt:77in",
		//                                                            ^^^^^^^^
	)

	isValid := p.isValid()

	if isValid {
		t.Fatalf("passport unexpectedly valid")
	}
}

func TestPassportIsValidReturnsFalseForPassportWithHclInInvalidFormat(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:860033327 eyr:2020 hcl:Xfffffd byr:1937 iyr:2017 hgt:183cm",
		//                              ^^^^^^^^^^^
	)

	isValid := p.isValid()

	if isValid {
		t.Fatalf("passport unexpectedly valid")
	}
}

func TestPassportIsValidReturnsFalseForPassportWithHclTooManyCharacters(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:860033327 eyr:2020 hcl:#fffffda byr:1937 iyr:2017 hgt:183cm",
		//                              ^^^^^^^^^^^^
	)

	isValid := p.isValid()

	if isValid {
		t.Fatalf("passport unexpectedly valid")
	}
}

func TestPassportIsValidReturnsFalseForPassportWithUnsupportedEcl(t *testing.T) {
	p := passportFromString(
		"ecl:xyz pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 hgt:183cm",
		//^^^^^^
	)

	isValid := p.isValid()

	if isValid {
		t.Fatalf("passport unexpectedly valid")
	}
}

func TestPassportIsValidReturnsFalseForPassportWithPidInInvalidFormat(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:x60033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 hgt:183cm",
		//       ^^^^^^^^^^^^^
	)

	isValid := p.isValid()

	if isValid {
		t.Fatalf("passport unexpectedly valid")
	}
}

func TestPassportIsValidReturnsFalseForPassportWithPidWithTooManyDigits(t *testing.T) {
	p := passportFromString(
		"ecl:gry pid:860033327999 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 hgt:183cm",
		//       ^^^^^^^^^^^^^^^^
	)

	isValid := p.isValid()

	if isValid {
		t.Fatalf("passport unexpectedly valid")
	}
}

func TestCountValidPassportsReturnsCorrectCountForExampleFromAssignment(t *testing.T) {
	passports := []Passport{
		// Valid passports:
		passportFromString("pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2f"),
		passportFromString("eyr:2029 ecl:blu cid:129 byr:1989 iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm"),
		passportFromString("hcl:#888785 hgt:164cm byr:2001 iyr:2015 cid:88 pid:545766238 ecl:hzl eyr:2022"),
		passportFromString("iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"),
		// Invalid passports:
		passportFromString("eyr:1972 cid:100 hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926"),
		passportFromString("iyr:2019 hcl:#602927 eyr:1967 hgt:170cm ecl:grn pid:012533040 byr:1946"),
		passportFromString("hcl:dab227 iyr:2012 ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277"),
		passportFromString("hgt:59cm ecl:zzz eyr:2038 hcl:74454a iyr:2023 pid:3556412378 byr:2007"),
	}

	count := coundValidPassports(passports)

	if count != 4 {
		t.Fatalf("unexpected count: %v", count)
	}
}
