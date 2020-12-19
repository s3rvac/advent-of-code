package main

import "testing"

func TestParseExpressionFromStringCorrectlyParsesValidExpression(t *testing.T) {
	expr, err := parseExpressionFromString("1 * (3 + 4)")

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(expr) != 7 || expr[0].value != 1 || expr[1].sym != "*" ||
		expr[2].sym != "(" || expr[3].value != 3 || expr[4].sym != "+" ||
		expr[5].value != 4 || expr[6].sym != ")" {
		t.Fatalf("unexpected expression: %v", expr)
	}
}

func TestParseExpressionCorrectlyReturnsErrorForInvalidExpression(t *testing.T) {
	_, err := parseExpressionFromString("1 + x")

	if err == nil {
		t.Fatalf("unexpectedly succeeded")
	}
}

func TestParseExpressionsFromStringCorrectlyParsesValidExpressions(t *testing.T) {
	exprs, err := parseExpressionsFromString(
		`1 * (3 + 4)
1 + 2
`,
	)

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(exprs) != 2 {
		t.Fatalf("unexpected expressions: %v", exprs)
	}
}

func scenarioEvaluatesToCorrectResult(t *testing.T, exprString string, expectedResult int) {
	expr, err := parseExpressionFromString(exprString)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	result := evaluateExpression(expr)

	if result != expectedResult {
		t.Fatalf("unexpected result: %v (expected: %v)", result, expectedResult)
	}
}

func TestEvaluateExpressionReturnsCorrectResult(t *testing.T) {
	scenarioEvaluatesToCorrectResult(t, "1", 1)
	scenarioEvaluatesToCorrectResult(t, "((1))", 1)
	scenarioEvaluatesToCorrectResult(t, "1 + 1", 2)
	scenarioEvaluatesToCorrectResult(t, "1 * 2", 2)
	scenarioEvaluatesToCorrectResult(t, "1 + (2 * 3)", 7)
	scenarioEvaluatesToCorrectResult(t, "(1 + 2) * 3", 9)
	scenarioEvaluatesToCorrectResult(t, "((1 + 2) * 3) * 2", 18)
	scenarioEvaluatesToCorrectResult(t, "(1 + 2) * (1 + 3)", 12)
	scenarioEvaluatesToCorrectResult(t, "1 + 2 * 3 + 4 * 5 + 6", 231)
	scenarioEvaluatesToCorrectResult(t, "1 + (2 * 3) + (4 * (5 + 6))", 51)
	scenarioEvaluatesToCorrectResult(t, "2 * 3 + (4 * 5)", 46)
	scenarioEvaluatesToCorrectResult(t, "5 + (8 * 3 + 9 + 3 * 4 * 3)", 1445)
	scenarioEvaluatesToCorrectResult(t, "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 669060)
	scenarioEvaluatesToCorrectResult(t, "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 23340)
}

func TestEvaluateExpressionsAndSumTheirResultsReturnsCorrectSum(t *testing.T) {
	expr1, _ := parseExpressionFromString("1 + 2")
	expr2, _ := parseExpressionFromString("3 + 4")
	exprs := Expressions{expr1, expr2}

	sum := evaluateExpressionsAndSumTheirResults(exprs)

	if sum != 10 {
		t.Fatalf("unexpected sum: %v", sum)
	}
}
