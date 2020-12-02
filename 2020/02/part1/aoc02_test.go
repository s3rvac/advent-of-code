package main

import "testing"

func TestParsePasswordWithPolicyReturnsCorrectResultWhenEverythingIsValid(t *testing.T) {
	passwordWithPolicy, err := parsePasswordWithPolicy("1-3 a: abcde")

	if err != nil {
		t.Fatalf("parsing unexpectedly failed with '%v'", err)
	}
	if passwordWithPolicy.password != "abcde" {
		t.Fatalf("unexpected password: '%v'", passwordWithPolicy.password)
	}
	if passwordWithPolicy.policy.letter != 'a' {
		t.Fatalf("unexpected policy letter: '%v'", passwordWithPolicy.policy.letter)
	}
	if passwordWithPolicy.policy.atLeast != 1 {
		t.Fatalf("unexpected lower bound: '%v'", passwordWithPolicy.policy.atLeast)
	}
	if passwordWithPolicy.policy.atMost != 3 {
		t.Fatalf("unexpected upper bound: '%v'", passwordWithPolicy.policy.atMost)
	}
}

func TestParsePasswordWithPolicyReturnsErrorWhenInputHasInvalidFormat(t *testing.T) {
	_, err := parsePasswordWithPolicy("1-3 a:")

	if err == nil {
		t.Fatalf("expected an error")
	}
}

func TestParsePasswordWithPolicyReturnsErrorWhenLowerBoundCannotBeConvertedToInt(t *testing.T) {
	_, err := parsePasswordWithPolicy("11111111111111111111111111111-3 a: abcde")

	if err == nil {
		t.Fatalf("expected an error")
	}
}

func TestParsePasswordWithPolicyReturnsErrorWhenUpperBoundCannotBeConvertedToInt(t *testing.T) {
	_, err := parsePasswordWithPolicy("1-33333333333333333333333333333 a: abcde")

	if err == nil {
		t.Fatalf("expected an error")
	}
}

func TestParsePasswordWithPolicyReturnsErrorWhenLowerBoundIsGreaterThanUpperBound(t *testing.T) {
	_, err := parsePasswordWithPolicy("3-1 a: abcde")

	if err == nil {
		t.Fatalf("expected an error")
	}
}

func TestIsPasswordWithPolicyValidReturnsTrueForValidPasswordWithPolicy(t *testing.T) {
	isValid := isPasswordWithPolicyValid(PasswordWithPolicy{"abcde", Policy{'a', 1, 3}})

	if !isValid {
		t.Fatalf("password with policy is unexpectedly invalid")
	}
}

func TestIsPasswordWithPolicyValidReturnsFalseWhenTooFewLettersInPassword(t *testing.T) {
	isValid := isPasswordWithPolicyValid(PasswordWithPolicy{"a", Policy{'a', 2, 2}})

	if isValid {
		t.Fatalf("password with policy is unexpectedly valid")
	}
}

func TestIsPasswordWithPolicyValidReturnsFalseWhenTooManyLettersInPassword(t *testing.T) {
	isValid := isPasswordWithPolicyValid(PasswordWithPolicy{"aa", Policy{'a', 1, 1}})

	if isValid {
		t.Fatalf("password with policy is unexpectedly valid")
	}
}

func TestValidatePasswordsWithPoliciesReturnsCorrectCountForInputFromAssignment(t *testing.T) {
	passwordsWithPolicies := PasswordsWithPolicies{
		PasswordWithPolicy{"abcde", Policy{'a', 1, 3}},
		PasswordWithPolicy{"cdefg", Policy{'b', 1, 3}},
		PasswordWithPolicy{"ccccccccc", Policy{'c', 2, 9}},
	}

	validPasswordCount := validatePasswordsWithPolicies(passwordsWithPolicies)

	if validPasswordCount != 2 {
		t.Fatalf("unexpected number of valid passwords: %v", validPasswordCount)
	}
}
