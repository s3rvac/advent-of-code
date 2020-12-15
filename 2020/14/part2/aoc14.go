package main

import (
	"bytes"
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type AddressSpace map[int64]int64

type Instruction struct {
	mask    string
	address int64
	value   int64
}

type Program []Instruction

func parseProgramFromString(s string) (Program, error) {
	program := make(Program, 0)
	currentMask := "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

	lines := strings.Split(s, "\n")
	for _, line := range lines {
		if len(line) == 0 {
			continue
		}

		// Mask.
		maskMatch := regexp.MustCompile(`^mask = ([X01]{36})$`).FindStringSubmatch(line)
		if len(maskMatch) == 2 {
			currentMask = maskMatch[1]
			continue
		}

		// Value update.
		updateMatch := regexp.MustCompile(`^mem\[(\d+)\] = (\d+)$`).FindStringSubmatch(line)
		if len(updateMatch) != 3 {
			return Program{}, errors.New(fmt.Sprintf("invalid instruction: %s", line))
		}

		address, err := strconv.ParseInt(updateMatch[1], 10, 64)
		if err != nil {
			return Program{}, errors.New(fmt.Sprintf("invalid instruction (address conversion failed): %s", line))
		}

		value, err := strconv.ParseInt(updateMatch[2], 10, 64)
		if err != nil {
			return Program{}, errors.New(fmt.Sprintf("invalid instruction (value conversion failed): %s", line))
		}

		instr := Instruction{currentMask, address, value}
		program = append(program, instr)
	}

	return program, nil
}

func decodeAddress(address int64, mask string) []int64 {
	// decimal -> binary
	binaryAddress := fmt.Sprintf("%036b", address)

	computedBinaryAddresses := make([]bytes.Buffer, 1)
	for i, maskBit := range mask {
		// We need to iterate over indexes as we want to modify the buffers
		// during iteration (and not their copies).
		for j := range computedBinaryAddresses {
			switch maskBit {
			case '0':
				computedBinaryAddresses[j].WriteByte(binaryAddress[i])
			case '1':
				computedBinaryAddresses[j].WriteRune('1')
			case 'X':
				// We will need to consider both addresses with '0' and '1' as
				// the next bit.
				// 0 (new address)
				var newAddress bytes.Buffer
				newAddress.WriteString(computedBinaryAddresses[j].String())
				newAddress.WriteRune('0')
				computedBinaryAddresses = append(computedBinaryAddresses, newAddress)
				// 1 (re-use the existing address)
				computedBinaryAddresses[j].WriteByte('1')
			}
		}
	}

	addresses := make([]int64, 0)
	for _, computedBinaryAddress := range computedBinaryAddresses {
		// binary -> decimal
		address, _ := strconv.ParseInt(computedBinaryAddress.String(), 2, 64)
		addresses = append(addresses, address)
	}
	return addresses
}

func runProgram(program Program, addressSpace *AddressSpace) {
	for _, instr := range program {
		value := instr.value
		addresses := decodeAddress(instr.address, instr.mask)
		for _, address := range addresses {
			if value != 0 {
				(*addressSpace)[address] = value
			} else {
				// Remove zero values from the map to save space.
				delete(*addressSpace, address)
			}
		}
	}
}

func sumNonZeroValuesInAddressSpace(addressSpace *AddressSpace) int64 {
	sum := int64(0)

	for _, value := range *addressSpace {
		if value != 0 {
			sum += value
		}
	}

	return sum
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputFileContent() string {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc14 INPUT_FILE")
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
	program, err := parseProgramFromString(input)
	if err != nil {
		printErrorAndExit(err)
	}
	addressSpace := make(AddressSpace)
	runProgram(program, &addressSpace)
	sum := sumNonZeroValuesInAddressSpace(&addressSpace)
	fmt.Println(sum)
}
