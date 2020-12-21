package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"regexp"
	"strings"
)

type Food struct {
	ingredients    []string
	knownAllergens []string
}

type Foods []Food

func parseFoodFromString(s string) (Food, error) {
	// Example: "mxmxvkd kfcds sqjhc nhms (contains dairy, fish)"
	m := regexp.MustCompile(`^([a-z ]+) \(contains ([a-z, ]+)\)$`).FindStringSubmatch(s)
	if len(m) != 3 {
		return Food{}, errors.New(fmt.Sprintf("invalid food: %s", s))
	}

	ingredients := strings.Split(m[1], " ")
	knownAllergens := strings.Split(m[2], ", ")
	return Food{ingredients, knownAllergens}, nil
}

func parseFoodsFromString(s string) (Foods, error) {
	foods := make(Foods, 0)

	lines := strings.Split(s, "\n")
	for _, line := range lines {
		if len(line) > 0 {
			food, err := parseFoodFromString(line)
			if err != nil {
				return nil, err
			}
			foods = append(foods, food)
		}
	}

	return foods, nil
}

func containsIngredient(toFind string, ingredients []string) bool {
	for _, ingredient := range ingredients {
		if ingredient == toFind {
			return true
		}
	}
	return false
}

func removeIngredient(toRemove string, ingredients []string) []string {
	result := make([]string, 0)
	for _, ingredient := range ingredients {
		if ingredient != toRemove {
			result = append(result, ingredient)
		}
	}
	return result
}

func copyIngredients(ingredients []string) []string {
	result := make([]string, len(ingredients))
	copy(result, ingredients)
	return result
}

func ingredientsIntersection(ingredientLists []([]string)) []string {
	// Start with all ingredients.
	intersection := make([]string, 0)
	for _, possibility := range ingredientLists {
		for _, ingredient := range possibility {
			if !containsIngredient(ingredient, intersection) {
				intersection = append(intersection, ingredient)
			}
		}
	}

	// Remove ingredients that do not appear in all possibilities.
	for _, ingredient := range copyIngredients(intersection) {
		for _, possibility := range ingredientLists {
			if !containsIngredient(ingredient, possibility) {
				intersection = removeIngredient(ingredient, intersection)
			}
		}
	}

	return intersection
}

func getIngredientsWithoutAllergens(foods Foods) []string {
	// A mapping between an allergen to possible lists of ingredients
	// (`a2i` - allergen to ingredients map).
	a2i := make(map[string]([][]string))
	for _, food := range foods {
		for _, allergen := range food.knownAllergens {
			a2i[allergen] = append(a2i[allergen], food.ingredients)
		}
	}

	// Compute possibilities for each allergen
	// (`ap` = allergen possibilities).
	ap := make(map[string]([]string))
	for allergen, possibilities := range a2i {
		ap[allergen] = ingredientsIntersection(possibilities)
	}

	// Compute ingredients that cannot contain an allergen.
	ingredientsWithoutAllergens := make([]string, 0)
	for _, food := range foods {
		for _, ingredient := range food.ingredients {
			isWithoutAllergen := true
			for _, possibleAllergens := range ap {
				for _, possibleAllergen := range possibleAllergens {
					if ingredient == possibleAllergen {
						isWithoutAllergen = false
						break
					}
				}
			}
			if isWithoutAllergen && !containsIngredient(ingredient, ingredientsWithoutAllergens) {
				ingredientsWithoutAllergens = append(ingredientsWithoutAllergens, ingredient)
			}
		}
	}
	return ingredientsWithoutAllergens
}

func computeOccurrenceCountOfIngredients(foods Foods, ingredientsToCount []string) int {
	count := 0

	for _, food := range foods {
		for _, ingredient := range food.ingredients {
			for _, ingredientToCount := range ingredientsToCount {
				if ingredient == ingredientToCount {
					count++
				}
			}
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
		fmt.Fprintln(os.Stderr, "usage: aoc21 INPUT_FILE")
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
	foods, err := parseFoodsFromString(input)
	if err != nil {
		printErrorAndExit(err)
	}
	ingredientsWithoutAllergens := getIngredientsWithoutAllergens(foods)
	count := computeOccurrenceCountOfIngredients(foods, ingredientsWithoutAllergens)
	fmt.Println(count)
}
