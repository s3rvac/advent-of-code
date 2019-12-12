#[macro_use]
extern crate failure;
#[macro_use]
extern crate clap;
#[cfg(test)]
#[macro_use]
extern crate maplit;

use clap::App;
use clap::Arg;
use std::collections::HashMap;
use std::collections::HashSet;
use std::fs;
use std::path::Path;
use std::path::PathBuf;

type Result<T> = std::result::Result<T, failure::Error>;

fn parse_args() -> PathBuf {
    let matches = App::new(crate_name!())
        .arg(
            Arg::with_name("INPUT_FILE")
                .help("Input file")
                .required(true)
                .index(1),
        )
        .get_matches();
    matches.value_of("INPUT_FILE").unwrap().into()
}

type SpaceObject = String;

struct OrbitMap {
    // Mapping of space objects to their direct orbits. Every object in space
    // is in direct orbit around exactly one other object (except for COM).
    // In the map, an entry (x, y) means that x directly orbits around y.
    orbit_map: HashMap<SpaceObject, SpaceObject>,
}

impl OrbitMap {
    pub fn from_string(s: &str) -> Result<Self> {
        let mut orbit_map = HashMap::new();
        for line in s.split('\n') {
            let line = line.trim();
            if line.is_empty() {
                continue;
            }

            let orbit_entry = line.split(')').collect::<Vec<_>>();
            if orbit_entry.len() != 2 {
                return Err(format_err!("invalid orbit map entry: {}", line));
            }

            // AAA)BBB means that BBB orbits around AAA. Every object in space
            // is in orbit around exactly one other object (except for COM).
            // Store AAA)BBB into the map as (BBB, AAA) because map keys have
            // to be unique.
            orbit_map.insert(orbit_entry[1].to_owned(), orbit_entry[0].to_owned());
        }

        Ok(OrbitMap { orbit_map })
    }

    #[cfg(test)]
    pub fn object_names(&self) -> HashSet<SpaceObject> {
        let mut object_names = HashSet::new();
        for (x, y) in &self.orbit_map {
            object_names.insert(x.clone());
            object_names.insert(y.clone());
        }
        object_names
    }

    pub fn total_orbit_count(&self) -> usize {
        // In what follows, (x, y) means that x orbits (either directly or
        // indirectly) around y.
        let mut orbits = HashSet::new();

        // Direct orbits.
        for (x, y) in &self.orbit_map {
            orbits.insert((x, y));
        }

        // Indirect orbits. Keep iterating over orbits and adding new indirect
        // orbits until the set is unchanged (i.e. until we reach a fixed
        // point).
        loop {
            let orig_orbits = orbits.clone();

            for (x, y) in &orig_orbits {
                // x orbits around y (either directly or indirectly). Get a
                // different object z around which y orbits (if any) and add
                // (x, z) into the set of orbits.
                // Graphically: z ) y ) x
                if let Some(z) = self.orbit_map.get(*y) {
                    orbits.insert((x, z));
                };
            }

            if orbits.len() == orig_orbits.len() {
                // We have reached a fixed point.
                break;
            }
        }

        orbits.len()
    }
}

fn read_input_file(file_path: &Path) -> Result<OrbitMap> {
    let s = fs::read_to_string(file_path)?;
    OrbitMap::from_string(&s)
}

fn main() -> Result<()> {
    let input_file = parse_args();
    let orbit_map = read_input_file(&input_file)?;
    println!("{}", orbit_map.total_orbit_count());
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn orbit_map_from_string_returns_correct_orbit_map_for_valid_string() {
        let orbit_map = OrbitMap::from_string(
            r#"
            COM)B
            B)C
            C)D
            D)E
            E)F
            B)G
            G)H
            D)I
            E)J
            J)K
            K)L
            "#,
        )
        .expect("OrbitMap should be valid");

        assert_eq!(
            orbit_map.object_names(),
            hashset! {
                "COM".to_owned(),
                "B".to_owned(),
                "C".to_owned(),
                "D".to_owned(),
                "E".to_owned(),
                "F".to_owned(),
                "G".to_owned(),
                "H".to_owned(),
                "I".to_owned(),
                "J".to_owned(),
                "K".to_owned(),
                "L".to_owned()
            }
        );
    }

    fn total_orbit_count_for_map(s: &str) -> usize {
        let orbit_map = OrbitMap::from_string(s).expect("OrbitMap should be valid");
        orbit_map.total_orbit_count()
    }

    #[test]
    fn total_orbit_count_returns_correct_value_for_custom_examples() {
        assert_eq!(
            total_orbit_count_for_map(
                r#"
                COM)A
                "#
            ),
            1
        );
        assert_eq!(
            total_orbit_count_for_map(
                r#"
                COM)A
                COM)B
                "#
            ),
            2
        );
        assert_eq!(
            total_orbit_count_for_map(
                r#"
                COM)A
                A)B
                "#
            ),
            3
        );
        assert_eq!(
            total_orbit_count_for_map(
                r#"
                COM)A
                A)B
                B)C
                "#
            ),
            6
        );
        assert_eq!(
            total_orbit_count_for_map(
                r#"
                COM)A
                A)B
                B)C
                COM)D
                "#
            ),
            7
        );
    }

    #[test]
    fn total_orbit_count_returns_correct_value_for_example_from_assignment() {
        assert_eq!(
            total_orbit_count_for_map(
                r#"
                COM)B
                B)C
                C)D
                D)E
                E)F
                B)G
                G)H
                D)I
                E)J
                J)K
                K)L
                "#
            ),
            42
        );
    }
}
