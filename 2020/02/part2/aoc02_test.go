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
	if passwordWithPolicy.policy.pos1 != 1 {
		t.Fatalf("unexpected first position: '%v'", passwordWithPolicy.policy.pos1)
	}
	if passwordWithPolicy.policy.pos2 != 3 {
		t.Fatalf("unexpected second position: '%v'", passwordWithPolicy.policy.pos2)
	}
}

func TestParsePasswordWithPolicyReturnsErrorWhenInputHasInvalidFormat(t *testing.T) {
	_, err := parsePasswordWithPolicy("1-3 a:")

	if err == nil {
		t.Fatalf("expected an error")
	}
}

func TestParsePasswordWithPolicyReturnsErrorWhenFirstPositionCannotBeConvertedToInt(t *testing.T) {
	_, err := parsePasswordWithPolicy("11111111111111111111111111111-3 a: abcde")

	if err == nil {
		t.Fatalf("expected an error")
	}
}

func TestParsePasswordWithPolicyReturnsErrorWhenSecondPositionCannotBeConvertedToInt(t *testing.T) {
	_, err := parsePasswordWithPolicy("1-33333333333333333333333333333 a: abcde")

	if err == nil {
		t.Fatalf("expected an error")
	}
}

func TestParsePasswordWithPolicyReturnsErrorWhenFirstPositionIsZero(t *testing.T) {
	_, err := parsePasswordWithPolicy("0-1 a: abcde")

	if err == nil {
		t.Fatalf("expected an error")
	}
}

func TestParsePasswordWithPolicyReturnsErrorWhenSecondPositionIsZero(t *testing.T) {
	_, err := parsePasswordWithPolicy("1-0 a: abcde")

	if err == nil {
		t.Fatalf("expected an error")
	}
}

func TestParsePasswordWithPolicyReturnsErrorWhenFirstPositionIsGreaterThanPasswordLength(t *testing.T) {
	_, err := parsePasswordWithPolicy("6-1 a: abcde")

	if err == nil {
		t.Fatalf("expected an error")
	}
}

func TestParsePasswordWithPolicyReturnsErrorWhenSecondPositionIsGreaterThanPasswordLength(t *testing.T) {
	_, err := parsePasswordWithPolicy("1-6 a: abcde")

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

func TestIsPasswordWithPolicyValidReturnsFalseWhenNoneOfPositionsMatch(t *testing.T) {
	isValid := isPasswordWithPolicyValid(PasswordWithPolicy{"abcd", Policy{'a', 2, 4}})

	if isValid {
		t.Fatalf("password with policy is unexpectedly valid")
	}
}

func TestIsPasswordWithPolicyValidReturnsFalseWhenBothPositionsMatch(t *testing.T) {
	isValid := isPasswordWithPolicyValid(PasswordWithPolicy{"aa", Policy{'a', 1, 2}})

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

	if validPasswordCount != 1 {
		t.Fatalf("unexpected number of valid passwords: %v", validPasswordCount)
	}
}
