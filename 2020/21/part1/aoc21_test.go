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

func TestGetIngredientsWithoutAllergensReturnsCorrectIngredientsForExampleFromAssignment(t *testing.T) {
	foods, _ := parseFoodsFromString(
		`mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
`,
	)

	ingredientsWithoutAllergens := getIngredientsWithoutAllergens(foods)

	if len(ingredientsWithoutAllergens) != 4 {
		t.Fatalf("unexpected ingredients: %v", ingredientsWithoutAllergens)
	}
	for _, ingredient := range ingredientsWithoutAllergens {
		if ingredient != "kfcds" && ingredient != "nhms" && ingredient != "sbzzf" && ingredient != "trh" {
			t.Fatalf("unexpected ingredient: %v", ingredient)
		}
	}
}

func TestComputeOccurrenceCountOfIngredientsReturnsCorrectCountForExampleFromAssignment(t *testing.T) {
	foods, _ := parseFoodsFromString(
		`mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
`,
	)

	count := computeOccurrenceCountOfIngredients(foods, []string{"kfcds", "nhms", "sbzzf", "trh"})

	if count != 5 {
		t.Fatalf("unexpected count: %v", count)
	}
}
