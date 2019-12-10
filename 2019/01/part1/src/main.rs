#[macro_use]
extern crate failure;
#[macro_use]
extern crate clap;

use clap::App;
use clap::Arg;
use failure::Error;
use std::fs::File;
use std::io::BufRead;
use std::io::BufReader;
use std::path::Path;
use std::path::PathBuf;

type Result<T> = std::result::Result<T, Error>;
type Mass = u64;
type Fuel = u64;

const MIN_MASS: u64 = 6;

fn parse_args() -> PathBuf {
    let matches = App::new(crate_name!())
        .arg(
            Arg::with_name("INPUT")
                .help("Path to the input file")
                .required(true)
                .index(1),
        )
        .get_matches();
    matches.value_of("INPUT").unwrap().into()
}

fn read_input(input_path: &Path) -> Result<Vec<Mass>> {
    let f = File::open(input_path)?;
    let reader = BufReader::new(&f);

    let mut result = Vec::new();
    for line in reader.lines() {
        let mass = line?.parse()?;
        if mass < MIN_MASS {
            return Err(format_err!("minimal mass is {}, got {}", MIN_MASS, mass));
        }
        result.push(mass);
    }
    Ok(result)
}

fn fuel_for_module(mass: Mass) -> Fuel {
    assert!(
        mass >= MIN_MASS,
        format!("minimal mass is {}, got {}", MIN_MASS, mass)
    );
    mass / 3 - 2
}

fn total_fuel_for_modules(masses: &[Mass]) -> Fuel {
    masses.iter().cloned().map(fuel_for_module).sum()
}

fn main() -> Result<()> {
    let input_file = parse_args();
    let masses = read_input(&input_file)?;
    let total_fuel = total_fuel_for_modules(&masses);
    println!("{}", total_fuel);
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[should_panic(expected = "minimal mass is 6, got 5")]
    fn test_fuel_for_module_asserts_when_mass_is_too_low() {
        fuel_for_module(5);
    }

    #[test]
    fn test_fuel_for_module_returns_correct_value() {
        assert_eq!(fuel_for_module(6), 0);
        assert_eq!(fuel_for_module(12), 2);
        assert_eq!(fuel_for_module(14), 2);
        assert_eq!(fuel_for_module(1969), 654);
        assert_eq!(fuel_for_module(100756), 33583);
    }

    #[test]
    fn test_total_fuel_for_modules_returns_correct_value_when_there_are_no_modules() {
        assert_eq!(total_fuel_for_modules(&[]), 0);
    }

    #[test]
    fn test_total_fuel_for_modules_returns_correct_value_when_there_are_modules() {
        assert_eq!(total_fuel_for_modules(&[12, 14, 1969]), 658);
    }
}
