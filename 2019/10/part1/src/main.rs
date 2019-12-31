use approx::relative_eq;
use clap::crate_name;
use clap::App;
use clap::Arg;
use failure::format_err;
use std::cmp::max;
use std::cmp::min;
use std::f64;
use std::fmt;
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

#[derive(Debug, Eq, PartialEq, Clone, Copy)]
enum Place {
    Empty,
    Asteroid,
}

type Pos = (usize, usize);

#[derive(Debug)]
struct Map {
    map: Vec<Vec<Place>>,
    positions: Vec<Pos>,
}

impl Map {
    pub fn from_string(s: &str) -> Result<Map> {
        let mut map: Vec<Vec<Place>> = Vec::new();
        for line in s.trim().split('\n') {
            let mut row = Vec::new();
            for c in line.trim().chars() {
                let place = match c {
                    '.' => Place::Empty,
                    '#' => Place::Asteroid,
                    _ => return Err(format_err!("unexpected char: {}", c)),
                };
                row.push(place);
            }
            if row.is_empty() {
                return Err(format_err!("row in map cannot be empty"));
            } else if !map.is_empty() && map[0].len() != row.len() {
                return Err(format_err!("each row in map must have the same length"));
            }
            map.push(row);
        }

        if map.is_empty() {
            return Err(format_err!("map cannot be empty"));
        }

        let mut positions = Vec::new();
        for row in 0..map.len() {
            for col in 0..map[0].len() {
                positions.push((row, col));
            }
        }
        Ok(Map { map, positions })
    }

    pub fn asteroid_count_from_best_location(&self) -> u64 {
        let mut best_asteroid_count = 0;

        for &pos in &self.positions {
            // A monitoring station can be placed only on an asteroid.
            if !self.contains_asteroid(pos) {
                continue;
            }

            let asteroid_count = self.asteroid_count_from_place(pos);
            if asteroid_count > best_asteroid_count {
                best_asteroid_count = asteroid_count;
            }
        }

        best_asteroid_count
    }

    fn contains_asteroid(&self, pos: Pos) -> bool {
        self.get(pos) == Place::Asteroid
    }

    fn get(&self, pos: Pos) -> Place {
        self.map[pos.0][pos.1]
    }

    fn asteroid_count_from_place(&self, src: Pos) -> u64 {
        let mut asteroid_count = 0;

        for &dst in &self.positions {
            // Do not count the place where are checking (the place
            // from which we are observing is an asteroid).
            if dst == src {
                continue;
            }

            if self.has_asteroid_observable_from(src, dst) {
                asteroid_count += 1;
            }
        }

        asteroid_count
    }

    // Does `dst` contain an asteroid observable from `src`?
    fn has_asteroid_observable_from(&self, src: Pos, dst: Pos) -> bool {
        if !self.contains_asteroid(dst) {
            return false;
        }

        // We need to check all places observable from `src` on a line to
        // `dst`. If there is an asteroid on at least one of these places, the
        // asteroid on `dst` is not observable.
        for &between in &self.positions {
            if !self.contains_asteroid(between) || between == src || between == dst {
                continue;
            }

            // There is an asteroid on `between`. Check if it blocks the view
            // from `src` by checking whether `between` is on a line from `src`
            // to `dst`.
            if self.are_on_line(src, between, dst) {
                return false;
            }
        }

        true
    }

    // Checks if the three given positions are on the same line.
    fn are_on_line(&self, pos1: Pos, pos2: Pos, pos3: Pos) -> bool {
        // https://en.wikipedia.org/wiki/Triangle_inequality
        // pos1------pos2------pos3
        let dst1 = self.distance(pos1, pos2) + self.distance(pos2, pos3);
        let dst2 = self.distance(pos1, pos3);
        // Since dst1 and dst2 are floats, we have to compare them on "almost
        // identity".
        return relative_eq!(dst1, dst2, max_relative = 1e-10);
    }

    // Returns the distance between `a` and `b` in 2D Euclidean space.
    fn distance(&self, a: Pos, b: Pos) -> f64 {
        // https://en.wikipedia.org/wiki/Euclidean_distance
        // Subtract the bigger value from the smaller to prevent subtract with overflow.
        let (x1, x2) = (max(a.0, b.0), min(a.0, b.0));
        let (y1, y2) = (max(a.1, b.1), min(a.1, b.1));
        f64::sqrt((x1 - x2).pow(2) as f64 + (y1 - y2).pow(2) as f64)
    }
}

impl fmt::Display for Map {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for row in &self.map {
            for place in row {
                let c = match place {
                    Place::Empty => '.',
                    Place::Asteroid => '#',
                };
                write!(f, "{}", c)?;
            }
            write!(f, "\n")?;
        }
        Ok(())
    }
}

fn read_input_file(file_path: &Path) -> Result<String> {
    Ok(fs::read_to_string(file_path)?)
}

fn main() -> Result<()> {
    let input_file = parse_args();
    let input = read_input_file(&input_file)?;
    let map = Map::from_string(&input)?;
    let asteroid_count = map.asteroid_count_from_best_location();
    println!("{}", asteroid_count);
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn map_from_string_returns_correct_map() {
        let map = Map::from_string(
            r#"
                .#..#
                .....
                #####
                ....#
                ...##
            "#,
        )
        .unwrap();

        assert_eq!(
            map.to_string(),
            ".#..#\n\
             .....\n\
             #####\n\
             ....#\n\
             ...##\n"
        );
    }

    #[test]
    fn map_from_string_returns_error_when_map_is_empty() {
        assert!(Map::from_string("").is_err());
    }

    #[test]
    fn map_from_string_returns_error_when_map_contains_unsupported_character() {
        assert!(Map::from_string("x").is_err());
    }

    #[test]
    fn map_from_string_returns_error_when_map_contains_rows_with_different_length() {
        assert!(Map::from_string("..\n.\n").is_err());
    }

    fn asteroid_count_from_best_location_for_map(s: &str) -> u64 {
        let map = Map::from_string(s).unwrap();
        map.asteroid_count_from_best_location()
    }

    #[test]
    fn map_asteroid_count_from_best_location_returns_correct_value() {
        assert_eq!(asteroid_count_from_best_location_for_map("#"), 0);
        assert_eq!(
            asteroid_count_from_best_location_for_map(
                r#"
                    .#..#
                    .....
                    #####
                    ....#
                    ...##
                "#,
            ),
            8
        );
        assert_eq!(
            asteroid_count_from_best_location_for_map(
                r#"
                    ......#.#.
                    #..#.#....
                    ..#######.
                    .#.#.###..
                    .#..#.....
                    ..#....#.#
                    #..#....#.
                    .##.#..###
                    ##...#..#.
                    .#....####
                "#,
            ),
            33
        );
        assert_eq!(
            asteroid_count_from_best_location_for_map(
                r#"
                    #.#...#.#.
                    .###....#.
                    .#....#...
                    ##.#.#.#.#
                    ....#.#.#.
                    .##..###.#
                    ..#...##..
                    ..##....##
                    ......#...
                    .####.###.
                "#,
            ),
            35
        );
        assert_eq!(
            asteroid_count_from_best_location_for_map(
                r#"
                    .#..#..###
                    ####.###.#
                    ....###.#.
                    ..###.##.#
                    ##.##.#.#.
                    ....###..#
                    ..#.#..#.#
                    #..#.#.###
                    .##...##.#
                    .....#.#..
                "#,
            ),
            41
        );
        assert_eq!(
            asteroid_count_from_best_location_for_map(
                r#"
                    .#..##.###...#######
                    ##.############..##.
                    .#.######.########.#
                    .###.#######.####.#.
                    #####.##.#.##.###.##
                    ..#####..#.#########
                    ####################
                    #.####....###.#.#.##
                    ##.#################
                    #####.##.###..####..
                    ..######..##.#######
                    ####.##.####...##..#
                    .#####..#.######.###
                    ##...#.##########...
                    #.##########.#######
                    .####.#.###.###.#.##
                    ....##.##.###..#####
                    .#.#.###########.###
                    #.#.#.#####.####.###
                    ###.##.####.##.#..##
                "#,
            ),
            210
        );
    }
}
