#[macro_use]
extern crate failure;
#[macro_use]
extern crate clap;
#[macro_use]
extern crate maplit;

use clap::App;
use clap::Arg;
use std::collections::HashMap;
#[cfg(test)]
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

    // Returns the minimum number of orbital transfers between the object `a`
    // orbits and the one `b` orbits.
    pub fn minimum_orbital_transfers_between(&self, a: &str, b: &str) -> usize {
        // First, find the number of orbital transfers needed to separately
        // reach `a` and `b` from COM. This gives us a mapping between a space
        // object and the number of orbital transfers needed to reach `a` or
        // `b` from it.
        let a_transfers = self.get_orbital_transfers_for(a);
        let b_transfers = self.get_orbital_transfers_for(b);

        // Go over both orbital transfers and find an object with the minimum
        // sum of orbital transfers to both `a` and `b`. This is the minimum
        // number of orbital transfers from `a` to `b`.
        let mut distance_sums = Vec::new();
        for (obj, distance_to_a) in a_transfers {
            if let Some(distance_to_b) = b_transfers.get(&obj) {
                distance_sums.push(distance_to_a + distance_to_b);
            }
        }
        let min = distance_sums.iter().min().expect("invalid orbital map");

        // We need to subtract 2 because the assignment asks for the minimum
        // number of orbital transfers from the object around which `a` and `b`
        // orbit, not from the object themselves.
        min - 2
    }

    // Returns a mapping of how many orbital transfers are needed from a space
    // object to reach the given object `obj`. Only space objects on the path
    // from COM to `obj` are included.
    fn get_orbital_transfers_for(&self, obj: &str) -> HashMap<SpaceObject, usize> {
        // Simply go from the given object towards COM. As all objects orbit
        // around exactly one other object (except for COM), there is no
        // possibility of looping because the orbit map is a tree.

        // Start from the object itself.
        let mut curr_obj = obj;
        let mut orbital_transfers = hashmap! {curr_obj.to_owned() => 0};
        let mut step_counter = 1;

        // Continue until we reach COM.
        while curr_obj != "COM" {
            curr_obj = self.orbit_map.get(curr_obj).expect("invalid orbital map");
            orbital_transfers.insert(curr_obj.to_owned(), step_counter);
            step_counter += 1;
        }

        orbital_transfers
    }
}

fn read_input_file(file_path: &Path) -> Result<OrbitMap> {
    let s = fs::read_to_string(file_path)?;
    OrbitMap::from_string(&s)
}

fn main() -> Result<()> {
    let input_file = parse_args();
    let orbit_map = read_input_file(&input_file)?;
    let transfer_count = orbit_map.minimum_orbital_transfers_between("YOU", "SAN");
    println!("{}", transfer_count);
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
            K)YOU
            I)SAN
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
                "L".to_owned(),
                "YOU".to_owned(),
                "SAN".to_owned(),
            }
        );
    }

    fn minimum_orbital_transfers_between(orbit_map_str: &str, a: &str, b: &str) -> usize {
        let orbit_map = OrbitMap::from_string(orbit_map_str).expect("OrbitMap should be valid");
        orbit_map.minimum_orbital_transfers_between(a, b)
    }

    #[test]
    fn minimum_orbital_transfers_between_returns_correct_value_for_custom_examples() {
        assert_eq!(
            minimum_orbital_transfers_between(
                r#"
                COM)A
                A)B
            "#,
                "B",
                "COM",
            ),
            0
        );
        assert_eq!(
            minimum_orbital_transfers_between(
                r#"
                COM)A
                A)B
                B)C
            "#,
                "C",
                "COM",
            ),
            1
        );
    }

    #[test]
    fn minimum_orbital_transfers_between_returns_correct_value_for_example_from_assignment() {
        assert_eq!(
            minimum_orbital_transfers_between(
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
                K)YOU
                I)SAN
            "#,
                "YOU",
                "SAN",
            ),
            4
        );
    }
}
