package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"regexp"
	"strings"
	"sort"
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

func computeIngredientAlergenMap(foods Foods) map[string]string {
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

	// Compute a map between ingredients and their corresponding alergens
	// (`i2a` - ingredient to allergen).
	i2a := make(map[string]string)
	for len(i2a) != len(ap) {
		// Assign allergens to ingredients in cases when there is only a single
		// possibility remaining.
		for allergen, possibilities := range ap {
			if len(possibilities) == 1 {
				ingredient := possibilities[0]
				i2a[ingredient] = allergen
				continue
			}
		}

		// Remove already assigned ingredients from the `ap` map.
		for ingredient := range i2a {
			for a := range ap {
				ap[a] = removeIngredient(ingredient, ap[a])
			}
		}
	}
	return i2a
}

func computeCanonicalDangerousIngredientList(ingredientAlergenMap map[string]string) string {
	// From the assignment: To produce the canonical dangerous ingredient list,
	// arrange the ingredients alphabetically by their allergen and separate
	// them by commas.

	// First, order all allergens alphabetically.
	allergens := make([]string, 0)
	for _, allergen := range ingredientAlergenMap {
		allergens = append(allergens, allergen)
	}
	sort.Strings(allergens)

	// Next, compute the ingredient list based on the computed order.
	ingredientList := make([]string, 0)
	for _, allergen := range allergens {
		for ingredient, otherAllergen := range ingredientAlergenMap {
			if allergen == otherAllergen {
				ingredientList = append(ingredientList, ingredient)
				break
			}
		}
	}

	// Finally, join all the ingredients with a comma.
	return strings.Join(ingredientList, ",")
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
	m := computeIngredientAlergenMap(foods)
	ingredientList := computeCanonicalDangerousIngredientList(m)
	fmt.Println(ingredientList)
}
