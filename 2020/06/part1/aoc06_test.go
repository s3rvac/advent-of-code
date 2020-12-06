package main

import "testing"

func TestSumYesAnswersForGroupReturnsCorrectSumForSinglePerson(t *testing.T) {
	yesAnswersForGroup := YesAnswersForGroup{
		YesAnswersForPerson{'a', 'b', 'c'},
	}

	sum := sumYesAnswersForGroup(yesAnswersForGroup)

	if sum != 3 {
		t.Fatalf("unpexpected sum: %v", sum)
	}
}

func TestSumYesAnswersForGroupReturnsCorrectSumForTwoPeople(t *testing.T) {
	yesAnswersForGroup := YesAnswersForGroup{
		YesAnswersForPerson{'a', 'b', 'c'},
		YesAnswersForPerson{'c', 'd'},
	}

	sum := sumYesAnswersForGroup(yesAnswersForGroup)

	if sum != 4 {
		t.Fatalf("unpexpected sum: %v", sum)
	}
}

func TestSumYesAnswersPerGroupReturnsCorrectSumForExampleFromAssignment(t *testing.T) {
	yesAnswers := []YesAnswersForGroup{
		YesAnswersForGroup{
			YesAnswersForPerson{'a', 'b', 'c'},
		},
		YesAnswersForGroup{
			YesAnswersForPerson{'a'},
			YesAnswersForPerson{'b'},
			YesAnswersForPerson{'c'},
		},
		YesAnswersForGroup{
			YesAnswersForPerson{'a', 'b'},
			YesAnswersForPerson{'b', 'c'},
		},
		YesAnswersForGroup{
			YesAnswersForPerson{'a'},
			YesAnswersForPerson{'a'},
			YesAnswersForPerson{'a'},
			YesAnswersForPerson{'a'},
		},
		YesAnswersForGroup{
			YesAnswersForPerson{'b'},
		},
	}

	sum := sumYesAnswersPerGroup(yesAnswers)

	if sum != 11 {
		t.Fatalf("unpexpected sum: %v", sum)
	}
}
