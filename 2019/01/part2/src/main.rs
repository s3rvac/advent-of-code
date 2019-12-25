use clap::crate_name;
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
        result.push(mass);
    }
    Ok(result)
}

fn fuel_for_module(mut mass: Mass) -> Fuel {
    let mut total_fuel = 0;
    loop {
        let div = mass / 3;
        if div <= 2 {
            break;
        }
        let fuel = div - 2;
        total_fuel += fuel;
        mass = fuel;
    }
    total_fuel
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
    fn test_fuel_for_module_returns_correct_value() {
        assert_eq!(fuel_for_module(0), 0);
        assert_eq!(fuel_for_module(14), 2);
        assert_eq!(fuel_for_module(1969), 966);
        assert_eq!(fuel_for_module(100756), 50346);
    }

    #[test]
    fn test_total_fuel_for_modules_returns_correct_value_when_there_are_no_modules() {
        assert_eq!(total_fuel_for_modules(&[]), 0);
    }

    #[test]
    fn test_total_fuel_for_modules_returns_correct_value_when_there_are_modules() {
        assert_eq!(total_fuel_for_modules(&[14, 1969, 100756]), 51314);
    }
}
