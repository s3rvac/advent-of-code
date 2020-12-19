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

// Go does not have sum types, so use this poor-man's alternative.
type Token struct {
	sym   string // +, *, (, )
	value int
}

type TokenSymPair struct {
	x string
	y string
}

type Expression []Token

type Expressions []Expression

func parseExpressionFromString(s string) (Expression, error) {
	// First, ensure that the whole string is valid.
	if !regexp.MustCompile(`^(\+|\*|\d+|\(|\)| )+$`).MatchString(s) {
		return nil, errors.New(fmt.Sprintf("invalid expression: %s", s))
	}

	// Parse the expression into tokens.
	expr := make(Expression, 0)
	matches := regexp.MustCompile(`\+|\*|\d+|\(|\)`).FindAllString(s, -1)
	for _, t := range matches {
		switch t {
		// sym
		case "+", "*", "(", ")":
			expr = append(expr, Token{t, 0})
		// value
		default:
			value, err := strconv.Atoi(t)
			if err != nil {
				return nil, errors.New(fmt.Sprintf("invalid expression: %s", s))
			}
			expr = append(expr, Token{"i", value})
		}
	}
	return expr, nil
}

func parseExpressionsFromString(s string) (Expressions, error) {
	exprs := make(Expressions, 0)

	lines := strings.Split(s, "\n")
	for _, line := range lines {
		if len(line) > 0 {
			expr, err := parseExpressionFromString(line)
			if err != nil {
				return nil, err
			}
			exprs = append(exprs, expr)
		}
	}

	return exprs, nil
}

func peekTopmostTerminalOnStack(stack []Token) Token {
	i := len(stack) - 1
	for stack[i].sym == "E" {
		i--
	}
	return stack[i]
}

func pushToStack(token Token, stack *[]Token) {
	*stack = append(*stack, token)
}

func appendTokenAfterTopmostTerminalOnStack(token Token, stack *[]Token) {
	for i := len(*stack) - 1; i >= 0; i-- {
		if (*stack)[i].sym != "E" {
			*stack = append((*stack)[:i+1], (*stack)[i:]...)
			(*stack)[i+1] = token
			return
		}
	}
}

func computeRuleRighHandSideOnStack(stack *[]Token) {
	// Find the position of the last "<" on the stack.
	i := len(*stack) - 1
	for (*stack)[i].sym != "<" {
		i--
	}

	ruleRhs := (*stack)[i+1:]

	// Remove "<" and everything after it on the stack.
	*stack = (*stack)[:i]

	// Compute the new token to push on the stack.
	ruleLhs := Token{"", 0}
	if len(ruleRhs) == 3 {
		if ruleRhs[1].sym == "+" {
			// E -> E + E
			ruleLhs = Token{"E", ruleRhs[0].value + ruleRhs[2].value}
		} else if ruleRhs[1].sym == "*" {
			// E -> E * E
			ruleLhs = Token{"E", ruleRhs[0].value * ruleRhs[2].value}
		} else {
			// E -> (E)
			ruleLhs = Token{"E", ruleRhs[1].value}
		}
	} else {
		// E -> value
		ruleLhs = Token{"E", ruleRhs[0].value}
	}

	pushToStack(ruleLhs, stack)
}

func evaluateExpression(expr Expression) int {
	// Operator precedence parser.
	//
	// Grammar:
	//
	//    E -> E + E
	//    E -> E * E
	//    E -> (E)
	//    E -> value
	//

	// Per the assignment, both + and * have the same precedence.
	precedenceTable := map[TokenSymPair]string{
		TokenSymPair{"+", "+"}: ">",
		TokenSymPair{"*", "+"}: ">",
		TokenSymPair{"(", "+"}: "<",
		TokenSymPair{")", "+"}: ">",
		TokenSymPair{"i", "+"}: ">",
		TokenSymPair{"$", "+"}: "<",

		TokenSymPair{"+", "*"}: ">", // Change: > instead of <.
		TokenSymPair{"*", "*"}: ">",
		TokenSymPair{"(", "*"}: "<",
		TokenSymPair{")", "*"}: ">",
		TokenSymPair{"i", "*"}: ">",
		TokenSymPair{"$", "*"}: "<",

		TokenSymPair{"+", "("}: "<",
		TokenSymPair{"*", "("}: "<",
		TokenSymPair{"(", "("}: "<",
		TokenSymPair{"$", "("}: "<",

		TokenSymPair{"+", ")"}: ">",
		TokenSymPair{"*", ")"}: ">",
		TokenSymPair{"(", ")"}: "=",
		TokenSymPair{")", ")"}: ">",
		TokenSymPair{"i", ")"}: ">",

		TokenSymPair{"+", "i"}: "<",
		TokenSymPair{"*", "i"}: "<",
		TokenSymPair{"(", "i"}: "<",
		TokenSymPair{"$", "i"}: "<",

		TokenSymPair{"+", "$"}: ">",
		TokenSymPair{"*", "$"}: ">",
		TokenSymPair{")", "$"}: ">",
		TokenSymPair{"i", "$"}: ">",
	}

	// Initialize the stack.
	stack := make([]Token, 0)
	stack = append(stack, Token{"$", 0})

	// Append a terminator ("$") after the expression to simplify the algorithm.
	exprWithTerminator := make(Expression, len(expr))
	copy(exprWithTerminator, expr)
	exprWithTerminator = append(exprWithTerminator, Token{"$", 0})
	expr = exprWithTerminator

	i := 0
	for i < len(expr)-1 || len(stack) != 2 {
		a := expr[i]
		b := peekTopmostTerminalOnStack(stack)
		entry := precedenceTable[TokenSymPair{b.sym, a.sym}]
		switch entry {
		case "=":
			pushToStack(a, &stack)
			i++
		case "<":
			appendTokenAfterTopmostTerminalOnStack(Token{"<", 0}, &stack)
			pushToStack(a, &stack)
			i++
		case ">":
			computeRuleRighHandSideOnStack(&stack)
		}
	}

	return stack[1].value
}

func evaluateExpressionsAndSumTheirResults(exprs Expressions) int {
	sum := 0
	for _, expr := range exprs {
		sum += evaluateExpression(expr)
	}
	return sum
}

func printErrorAndExit(err error) {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}

func loadInputFileContent() string {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: aoc18 INPUT_FILE")
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
	expressions, err := parseExpressionsFromString(input)
	if err != nil {
		printErrorAndExit(err)
	}
	sum := evaluateExpressionsAndSumTheirResults(expressions)
	fmt.Println(sum)
}
