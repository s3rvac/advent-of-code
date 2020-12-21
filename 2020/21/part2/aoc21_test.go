package main

import "testing"

func TestParseFoodsFromStringReturnsCorrectRepresentationForValidFoodList(t *testing.T) {
	foods, err := parseFoodsFromString(
		`mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
`,
	)

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(foods) != 4 || len(foods[0].ingredients) != 4 || len(foods[0].knownAllergens) != 2 ||
		foods[0].knownAllergens[0] != "dairy" || foods[0].knownAllergens[1] != "fish" {
		t.Fatalf("unexpected foods: %v", foods)
	}
}

func TestComputeIngredientAlergenMapReturnsCorrectMapForExampleFromAssignment(t *testing.T) {
	foods, _ := parseFoodsFromString(
		`mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
`,
	)

	m := computeIngredientAlergenMap(foods)

	if len(m) != 3 || m["mxmxvkd"] != "dairy" || m["sqjhc"] != "fish" || m["fvjkl"] != "soy" {
		t.Fatalf("unexpected map: %v", m)
	}
}

func TestComputeCanonicalDangerousIngredientListReturnsCorrectListForExampleFromAssignment(t *testing.T) {
	foods, _ := parseFoodsFromString(
		`mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
`,
	)
	m := computeIngredientAlergenMap(foods)

	ingredientList := computeCanonicalDangerousIngredientList(m)

	if ingredientList != "mxmxvkd,sqjhc,fvjkl" {
		t.Fatalf("unexpected list: %v", ingredientList)
	}
}
