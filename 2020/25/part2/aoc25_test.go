package main

import "testing"

func TestParsePublicKeysFromStringReturnsCorrectPublicKeysForValidInput(t *testing.T) {
	cardPK, doorPK, err := parsePublicKeysFromString(
		`5764801
17807724
`,
	)

	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if cardPK != 5764801 {
		t.Fatalf("unexpected card's public key: %v", cardPK)
	}
	if doorPK != 17807724 {
		t.Fatalf("unexpected door's public key: %v", doorPK)
	}
}

func TestComputeEncryptionKeyReturnsCorrectEncryptionKeyForExampleFromAssignment(t *testing.T) {
	cardPK, doorPK, _ := parsePublicKeysFromString(
		`5764801
17807724
`,
	)

	encryptionKey := computeEncryptionKey(cardPK, doorPK)

	if encryptionKey != 14897079 {
		t.Fatalf("unexpected encryption key: %v", encryptionKey)
	}
}
