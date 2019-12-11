#[macro_use]
extern crate failure;
#[macro_use]
extern crate clap;

use clap::App;
use clap::Arg;

type InputRange = (u64, u64);
type Result<T> = std::result::Result<T, failure::Error>;

fn parse_args() -> Result<InputRange> {
    let matches = App::new(crate_name!())
        .arg(
            Arg::with_name("INPUT_RANGE")
                .help("Input range")
                .required(true)
                .index(1),
        )
        .get_matches();
    let input_range = matches.value_of("INPUT_RANGE").unwrap();
    parse_input_range(input_range)
}

fn parse_input_range(range_str: &str) -> Result<InputRange> {
    let range = range_str.split('-').collect::<Vec<&str>>();
    if range.len() != 2 {
        return Err(format_err!(
            "invalid input range: {} (incorrect format)",
            range_str
        ));
    }

    let begin = range[0].parse::<u64>()?;
    let end = range[1].parse::<u64>()?;
    if begin > end {
        return Err(format_err!(
            "invalid input range: {} (begin is greater than end)",
            range_str
        ));
    }
    Ok((begin, end))
}

fn password_count_in_range_satisfying_criteria(input_range: InputRange) -> u64 {
    (input_range.0..=input_range.1)
        .filter(|&password| satisfies_criteria(password))
        .count() as u64
}

fn satisfies_criteria(password: u64) -> bool {
    // Password has to be a six-digit number.
    let digits = password
        .to_string()
        .chars()
        .map(|c| c.to_digit(10).unwrap())
        .collect::<Vec<_>>();
    if digits.len() != 6 {
        return false;
    }

    // Going from left to right, the digits never decrease; they only ever
    // increase or stay the same (like 111123 or 135679).
    let mut last_digit = digits[0];
    for &digit in &digits[1..] {
        if digit < last_digit {
            return false;
        }
        last_digit = digit;
    }

    // Two adjacent digits are the same (like 22 in 122345).
    let mut last_digit = digits[0];
    let mut same_double_found = false;
    for &digit in &digits[1..] {
        if digit == last_digit {
            same_double_found = true;
            break;
        }
        last_digit = digit;
    }
    if !same_double_found {
        return false;
    }

    true
}

fn main() -> Result<()> {
    let input_range = parse_args()?;
    let password_count = password_count_in_range_satisfying_criteria(input_range);
    println!("{}", password_count);
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_input_range_returns_correct_range_when_input_is_valid() {
        assert_eq!(parse_input_range("0-10").unwrap(), (0, 10));
        assert_eq!(parse_input_range("100-100").unwrap(), (100, 100));
    }

    #[test]
    fn parse_input_range_returns_error_when_range_has_invalid_format() {
        assert!(parse_input_range("").is_err());
        assert!(parse_input_range("-").is_err());
        assert!(parse_input_range("1-").is_err());
        assert!(parse_input_range("-2").is_err());
    }

    #[test]
    fn parse_input_range_returns_error_when_beginning_of_range_is_bigger_than_end_of_range() {
        assert!(parse_input_range("2-1").is_err());
    }

    #[test]
    fn satisfies_criteria_returns_true_for_passwords_satisfying_criteria() {
        assert!(satisfies_criteria(111111));
        assert!(satisfies_criteria(113456));
        assert!(satisfies_criteria(123499));
    }

    #[test]
    fn satisfies_criteria_returns_false_for_password_that_is_too_short() {
        assert!(!satisfies_criteria(11111));
    }

    #[test]
    fn satisfies_criteria_returns_false_for_password_that_is_too_long() {
        assert!(!satisfies_criteria(1111111));
    }

    #[test]
    fn satisfies_criteria_returns_false_for_password_that_does_not_contain_pair_of_doubles() {
        assert!(!satisfies_criteria(123456));
    }

    #[test]
    fn satisfies_criteria_returns_false_for_password_that_contains_decreasing_pair() {
        assert!(!satisfies_criteria(113221));
    }

    #[test]
    fn password_count_in_range_satisfying_criteria_returns_correct_count() {
        assert_eq!(
            password_count_in_range_satisfying_criteria((111111, 111111)),
            1
        );
        assert_eq!(
            password_count_in_range_satisfying_criteria((111111, 111113)),
            3
        );
    }
}
