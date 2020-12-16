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

type Interval struct {
	from int
	to   int
}

type Intervals []Interval

type Ticket []int

type Tickets []Ticket

type Location string

type Rules map[Location]Intervals

type InputInfo struct {
	rules         Rules
	myTicket      Ticket
	nearbyTickets Tickets
}

type FieldsOrder []Location

type TicketValuesMap map[Location]int

func parseTicketFromString(s string) (Ticket, error) {
	ticket := make(Ticket, 0)

	for _, item := range strings.Split(s, ",") {
		n, err := strconv.Atoi(item)
		if err != nil {
			return nil, errors.New(fmt.Sprintf("unexpected number in a ticket: %s", s))
		}
		ticket = append(ticket, n)
	}

	return ticket, nil
}

func parseInputInfoFromString(s string) (*InputInfo, error) {
	rules := make(map[Location]Intervals)
	myTicket := make(Ticket, 0)
	nearbyTickets := make(Tickets, 0)

	phase := "rules"
	lines := strings.Split(s, "\n")
	for _, line := range lines {
		if len(line) == 0 {
			continue
		} else if line == "your ticket:" {
			phase = "my ticket"
			continue
		} else if line == "nearby tickets:" {
			phase = "nearby tickets"
			continue
		}

		if phase == "rules" {
			m := regexp.MustCompile(`^([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)$`).FindStringSubmatch(line)
			if len(m) != 6 {
				return nil, errors.New(fmt.Sprintf("invalid line (rule parsing error): %s", line))
			}

			location := Location(m[1])
			intervals := make(Intervals, 0, 2)

			for _, i := range []int{2, 4} {
				from, err := strconv.Atoi(m[i])
				if err != nil {
					return nil, errors.New(fmt.Sprintf("invalid line (int parsing error): %s", line))
				}

				to, err := strconv.Atoi(m[i+1])
				if err != nil {
					return nil, errors.New(fmt.Sprintf("invalid line (int parsing error): %s", line))
				}
				intervals = append(intervals, Interval{from, to})
			}

			rules[location] = intervals
		} else if phase == "my ticket" {
			ticket, err := parseTicketFromString(line)
			if err != nil {
				return nil, errors.New(fmt.Sprintf("invalid line (ticket parsing error): %s", line))
			}
			myTicket = ticket
		} else { // Nearby ticket.
			ticket, err := parseTicketFromString(line)
			if err != nil {
				return nil, errors.New(fmt.Sprintf("invalid line (ticket parsing error): %s", line))
			}
			nearbyTickets = append(nearbyTickets, ticket)
		}
	}

	return &InputInfo{rules, myTicket, nearbyTickets}, nil
}

func fitsIntoIntervals(value int, intervals Intervals) bool {
	return (value >= intervals[0].from && value <= intervals[0].to) ||
		(value >= intervals[1].from && value <= intervals[1].to)
}

func isValidTicketValue(value int, rules Rules) bool {
	for _, intervals := range rules {
		if fitsIntoIntervals(value, intervals) {
			return true
		}
	}
	return false
}

func isValidTicket(ticket Ticket, rules Rules) bool {
	for _, value := range ticket {
		if !isValidTicketValue(value, rules) {
			return false
		}
	}

	return true
}

func (info *InputInfo) removeInvalidNearbyTickets() {
	validNearbyTickets := make(Tickets, 0)

	for _, ticket := range info.nearbyTickets {
		if isValidTicket(ticket, info.rules) {
			validNearbyTickets = append(validNearbyTickets, ticket)
		}
	}

	info.nearbyTickets = validNearbyTickets
}

func removeElementFromSlice(toRemove int, slice []int) []int {
	result := make([]int, 0)
	for _, element := range slice {
		if element != toRemove {
			result = append(result, element)
		}
	}
	return result
}

func (info *InputInfo) determineFieldsOrder() FieldsOrder {
	// Initialize all possibilities.
	possibilities := make(map[Location]([]int))
	for location, _ := range info.rules {
		for i := 0; i < len(info.rules); i++ {
			possibilities[location] = append(possibilities[location], i)
		}
	}

	// Remove impossibilities.
	for _, ticket := range info.nearbyTickets {
		for i, value := range ticket {
			for location, intervals := range info.rules {
				if !fitsIntoIntervals(value, intervals) {
					possibilities[location] = removeElementFromSlice(i, possibilities[location])
				}
			}
		}
	}

	// Compute the order.
	orderMap := make(map[Location]int)
	for len(possibilities) > 0 {
		for location, indexes := range possibilities {
			if len(indexes) == 1 {
				i := indexes[0]
				orderMap[location] = i
				delete(possibilities, location)
				for location, _ := range possibilities {
					possibilities[location] = removeElementFromSlice(i, possibilities[location])
				}
				break
			}
		}
	}

	// Convert the order from a map to a slice.
	order := make(FieldsOrder, len(info.rules))
	for location, i := range orderMap {
		order[i] = location
	}
	return order
}

func (info *InputInfo) mapLocationsToMyTicketValues(fieldsOrder FieldsOrder) TicketValuesMap {
	m := make(TicketValuesMap)

	for i, value := range info.myTicket {
		m[fieldsOrder[i]] = value
	}

	return m
}

func multiplyValuesForLocationsStartingWith(ticketValuesMap TicketValuesMap, prefix string) int {
	result := 1

	for location, value := range ticketValuesMap {
		if strings.HasPrefix(string(location), prefix) {
			result *= value
		}
	}

	return result
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputFileContent() string {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc16 INPUT_FILE")
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
	inputInfo, err := parseInputInfoFromString(input)
	if err != nil {
		printErrorAndExit(err)
	}
	inputInfo.removeInvalidNearbyTickets()
	fieldsOrder := inputInfo.determineFieldsOrder()
	ticketValuesMap := inputInfo.mapLocationsToMyTicketValues(fieldsOrder)
	result := multiplyValuesForLocationsStartingWith(ticketValuesMap, "departure")
	fmt.Println(result)
}
