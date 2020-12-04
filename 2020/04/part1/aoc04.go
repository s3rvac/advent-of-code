package main

import (
	"bufio"
	"bytes"
	"fmt"
	"os"
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

func (p *Passport) isValid() bool {
	// A passport is valid when it has either all the fields or when the only
	// missing field is cid.
	return p.byr != "" &&
		p.iyr != "" &&
		p.eyr != "" &&
		p.hgt != "" &&
		p.hcl != "" &&
		p.ecl != "" &&
		p.pid != ""
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
