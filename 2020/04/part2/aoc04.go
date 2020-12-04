package main

import (
	"bufio"
	"bytes"
	"errors"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Passport struct {
	byr string // Birth Year
	iyr string // Issue Year
	eyr string // Expiration Year
	hgt string // Height
	hcl string // Hair Color
	ecl string // Eye Color
	pid string // Passport ID
	cid string // Country ID
}

func passportFromString(s string) Passport {
	var p Passport
	keysValues := strings.Split(s, " ")
	for _, keyValue := range keysValues {
		split := strings.Split(keyValue, ":")
		if len(split) != 2 {
			continue
		}

		key := split[0]
		value := split[1]

		switch key {
		case "byr":
			p.byr = value
		case "iyr":
			p.iyr = value
		case "eyr":
			p.eyr = value
		case "hgt":
			p.hgt = value
		case "hcl":
			p.hcl = value
		case "ecl":
			p.ecl = value
		case "pid":
			p.pid = value
		case "cid":
			p.cid = value
		}
	}
	return p
}

func appendSpaceSeparatedKeyValuePairIfNonEmpty(b *bytes.Buffer, k string, v string) {
	if v != "" {
		b.WriteString(fmt.Sprintf(" %s:%s", k, v))
	}
}

func (p *Passport) toString() string {
	var b bytes.Buffer
	appendSpaceSeparatedKeyValuePairIfNonEmpty(&b, "byr", p.byr)
	appendSpaceSeparatedKeyValuePairIfNonEmpty(&b, "iyr", p.iyr)
	appendSpaceSeparatedKeyValuePairIfNonEmpty(&b, "eyr", p.eyr)
	appendSpaceSeparatedKeyValuePairIfNonEmpty(&b, "hgt", p.hgt)
	appendSpaceSeparatedKeyValuePairIfNonEmpty(&b, "hcl", p.hcl)
	appendSpaceSeparatedKeyValuePairIfNonEmpty(&b, "ecl", p.ecl)
	appendSpaceSeparatedKeyValuePairIfNonEmpty(&b, "pid", p.pid)
	appendSpaceSeparatedKeyValuePairIfNonEmpty(&b, "cid", p.cid)
	return strings.TrimLeft(b.String(), " ")
}

func parseStringAsYear(s string) (int, error) {
	m := regexp.MustCompile(`^\d{4}$`).FindStringSubmatch(s)
	if m == nil {
		return 0, errors.New("invalid format")
	}
	return strconv.Atoi(m[0])
}

func (p *Passport) isValid() bool {
	// byr (Birth Year) - four digits; at least 1920 and at most 2002.
	byr, err := parseStringAsYear(p.byr)
	if err != nil || byr < 1920 || byr > 2002 {
		return false
	}

	// iyr (Issue Year) - four digits; at least 2010 and at most 2020.
	iyr, err := parseStringAsYear(p.iyr)
	if err != nil || iyr < 2010 || iyr > 2020 {
		return false
	}

	// eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
	eyr, err := parseStringAsYear(p.eyr)
	if err != nil || eyr < 2020 || eyr > 2030 {
		return false
	}

	// hgt (Height) - a number followed by either cm or in:
	// - If cm, the number must be at least 150 and at most 193.
	// - If in, the number must be at least 59 and at most 76.
	ghtM := regexp.MustCompile(`^(\d{2,3})(cm|in)$`).FindStringSubmatch(p.hgt)
	if ghtM == nil {
		return false
	}
	height, _ := strconv.Atoi(ghtM[1])
	unit := ghtM[2]
	switch unit {
	case "cm":
		if height < 150 || height > 193 {
			return false
		}
	case "in":
		if height < 59 || height > 76 {
			return false
		}
	}

	// hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
	if !regexp.MustCompile(`^#[0-9a-f]{6}$`).MatchString(p.hcl) {
		return false
	}

	// ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
	if !regexp.MustCompile(`^(amb|blu|brn|gry|grn|hzl|oth)$`).MatchString(p.ecl) {
		return false
	}

	// pid (Passport ID) - a nine-digit number, including leading zeroes.
	if !regexp.MustCompile(`^\d{9}$`).MatchString(p.pid) {
		return false
	}

	// cid (Country ID) - ignored, missing or not.
	return true
}

func coundValidPassports(passports []Passport) int {
	count := 0
	for _, p := range passports {
		if p.isValid() {
			count++
		}
	}
	return count
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputPassports() []Passport {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc04 INPUT_FILE")
		os.Exit(1)
	}

	file, err := os.Open(os.Args[1])
	if err != nil {
		printErrorAndExit(err)
	}
	defer file.Close()

	passports := make([]Passport, 0)
	scanner := bufio.NewScanner(file)
	var b bytes.Buffer
	for scanner.Scan() {
		line := scanner.Text()
		if line != "" {
			if b.Len() > 0 {
				b.WriteString(" ")
			}
			b.WriteString(line)
		} else {
			passport := passportFromString(b.String())
			passports = append(passports, passport)
			b.Reset()
		}
	}
	if b.Len() > 0 {
		// The last passport before the end of file.
		passport := passportFromString(b.String())
		passports = append(passports, passport)
	}
	return passports
}

func main() {
	passports := loadInputPassports()
	validPassportCount := coundValidPassports(passports)
	fmt.Println(validPassportCount)
}
