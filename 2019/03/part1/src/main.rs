#[macro_use]
extern crate failure;
#[macro_use]
extern crate clap;

use clap::App;
use clap::Arg;
use failure::Error;
use std::collections::HashSet;
use std::fs::File;
use std::io::BufRead;
use std::io::BufReader;
use std::path::Path;
use std::path::PathBuf;

type Result<T> = std::result::Result<T, Error>;

#[derive(Debug, Eq, PartialEq, Copy, Clone)]
struct WireMove {
    pub dx: i64,
    pub dy: i64,
}

impl WireMove {
    pub fn new(dx: i64, dy: i64) -> Self {
        assert!(
            dx == 0 || dy == 0,
            format!("invalid move: ({}, {})", dx, dy)
        );
        WireMove { dx, dy }
    }

    pub fn can_make_step(self) -> bool {
        self.dx != 0 || self.dy != 0
    }

    pub fn make_step(&mut self, pos: GridPos) -> GridPos {
        if self.dx > 0 {
            self.dx -= 1;
            (pos.0 + 1, pos.1)
        } else if self.dx < 0 {
            self.dx += 1;
            (pos.0 - 1, pos.1)
        } else if self.dy > 0 {
            self.dy -= 1;
            (pos.0, pos.1 + 1)
        } else if self.dy < 0 {
            self.dy += 1;
            (pos.0, pos.1 - 1)
        } else {
            pos
        }
    }

    pub fn from_string(s: &str) -> Result<Self> {
        let b = s.as_bytes();
        if b.len() < 2 {
            return Err(format_err!("invalid WireMove string: {}", s));
        }

        let n = std::str::from_utf8(&b[1..])?.parse::<i64>()?;
        if n < 0 {
            return Err(format_err!("invalid WireMove string: {}", s));
        }

        let (dx, dy) = match b[0] {
            b'R' => (n, 0),
            b'L' => (-n, 0),
            b'U' => (0, n),
            b'D' => (0, -n),
            _ => {
                return Err(format_err!("incorrect WireMove string: {}", s));
            }
        };

        Ok(WireMove::new(dx, dy))
    }
}

#[derive(Debug, Eq, PartialEq)]
struct WirePath {
    path: Vec<WireMove>,
}

impl WirePath {
    pub fn new(path: Vec<WireMove>) -> Self {
        WirePath { path }
    }

    pub fn from_string(s: &str) -> Result<Self> {
        let mut path = Vec::new();
        for mov in s.split(',') {
            path.push(WireMove::from_string(mov)?);
        }
        Ok(WirePath::new(path))
    }
}

impl IntoIterator for WirePath {
    type Item = WireMove;
    type IntoIter = WirePathIterator;

    fn into_iter(self) -> Self::IntoIter {
        WirePathIterator {
            wire_path: self,
            i: 0,
        }
    }
}

struct WirePathIterator {
    wire_path: WirePath,
    i: usize,
}

impl Iterator for WirePathIterator {
    type Item = WireMove;

    fn next(&mut self) -> Option<Self::Item> {
        if self.i < self.wire_path.path.len() {
            let curr_i = self.i;
            self.i += 1;
            Some(self.wire_path.path[curr_i])
        } else {
            None
        }
    }
}

type GridPos = (i64, i64);

const ORIGIN: GridPos = (0, 0);

#[derive(Debug, Default)]
struct Grid {
    wire_positions: [HashSet<GridPos>; 2],
}

impl Grid {
    pub fn new() -> Self {
        Grid::default()
    }

    pub fn run_wires_and_get_shortest_cross_distance(
        &mut self,
        wire_path1: WirePath,
        wire_path2: WirePath,
    ) -> Option<i64> {
        self.init();
        self.run_wire(wire_path1, 0);
        self.run_wire(wire_path2, 1);
        self.shortest_intersection_distance()
    }

    fn init(&mut self) {
        self.wire_positions[0].clear();
        self.wire_positions[1].clear();
    }

    fn run_wire(&mut self, wire_path: WirePath, idx: usize) {
        let mut pos = ORIGIN;
        for mut wire_move in wire_path {
            while wire_move.can_make_step() {
                pos = wire_move.make_step(pos);
                if pos != ORIGIN {
                    self.wire_positions[idx].insert(pos);
                }
            }
        }
    }

    pub fn shortest_intersection_distance(&self) -> Option<i64> {
        self.crosses()
            .into_iter()
            .map(|cross| self.manhattan_distance_from_origin(cross))
            .min()
    }

    fn crosses(&self) -> Vec<GridPos> {
        self.wire_positions[0]
            .intersection(&self.wire_positions[1])
            .map(|pos| (pos.0, pos.1))
            .collect()
    }

    fn manhattan_distance_from_origin(&self, cross: GridPos) -> i64 {
        // https://en.wikipedia.org/wiki/Taxicab_geometry
        (ORIGIN.0 - cross.0).abs() + (ORIGIN.1 - cross.1).abs()
    }
}

fn parse_args() -> Result<PathBuf> {
    let matches = App::new(crate_name!())
        .arg(
            Arg::with_name("INPUT")
                .help("Path to the input file")
                .required(true)
                .index(1),
        )
        .get_matches();
    Ok(matches.value_of("INPUT").unwrap().into())
}

fn read_input(input_path: &Path) -> Result<(WirePath, WirePath)> {
    let f = File::open(input_path)?;
    let reader = BufReader::new(&f);

    let mut wire_paths = Vec::new();
    for line in reader.lines() {
        wire_paths.push(WirePath::from_string(&line?)?);
    }
    if wire_paths.len() != 2 {
        return Err(format_err!("expected two wires, got {}", wire_paths.len()));
    }
    Ok((wire_paths.remove(0), wire_paths.remove(0)))
}

fn main() -> Result<()> {
    let input_file = parse_args()?;
    let (wire_path1, wire_path2) = read_input(&input_file)?;
    let mut grid = Grid::new();
    match grid.run_wires_and_get_shortest_cross_distance(wire_path1, wire_path2) {
        Some(distance) => println!("{}", distance),
        None => eprintln!("no cross"),
    };
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn wire_move_can_make_step_returns_true_when_can_make_step() {
        assert!(WireMove::new(1, 0).can_make_step());
        assert!(WireMove::new(0, -1).can_make_step());
    }

    #[test]
    fn wire_move_can_make_step_returns_false_when_cannot_make_step() {
        assert!(!WireMove::new(0, 0).can_make_step());
    }

    #[test]
    fn wire_move_make_step_returns_correct_new_pos() {
        assert_eq!(WireMove::new(1, 0).make_step((0, 0)), (1, 0));
        assert_eq!(WireMove::new(0, 1).make_step((0, 0)), (0, 1));
        assert_eq!(WireMove::new(-1, 0).make_step((0, 0)), (-1, 0));
        assert_eq!(WireMove::new(0, -1).make_step((0, 0)), (0, -1));
    }

    #[test]
    fn wire_move_make_step_adjust_stored_step_count_upon_each_call() {
        let mut wire_move = WireMove::new(2, 0);

        assert_eq!(wire_move.make_step((0, 0)), (1, 0));
        assert_eq!(wire_move.make_step((1, 0)), (2, 0));
        assert_eq!(wire_move.make_step((2, 0)), (2, 0)); // No more steps.
    }

    #[test]
    fn wire_move_make_step_returns_passed_pos_when_step_count_is_zero() {
        let mut wire_move = WireMove::new(0, 0);

        let step = wire_move.make_step((1, 1));

        assert_eq!(step, (1, 1));
    }

    #[test]
    fn wire_move_from_string_returns_correct_wire_move_for_valid_representation_single_digit() {
        assert_eq!(WireMove::from_string("R2").unwrap(), WireMove::new(2, 0));
        assert_eq!(WireMove::from_string("L2").unwrap(), WireMove::new(-2, 0));
        assert_eq!(WireMove::from_string("U2").unwrap(), WireMove::new(0, 2));
        assert_eq!(WireMove::from_string("D2").unwrap(), WireMove::new(0, -2));
    }

    #[test]
    fn wire_move_from_string_returns_correct_wire_move_for_valid_representation_mult_digits() {
        assert_eq!(
            WireMove::from_string("R100").unwrap(),
            WireMove::new(100, 0)
        );
        assert_eq!(
            WireMove::from_string("L100").unwrap(),
            WireMove::new(-100, 0)
        );
        assert_eq!(
            WireMove::from_string("U100").unwrap(),
            WireMove::new(0, 100)
        );
        assert_eq!(
            WireMove::from_string("D100").unwrap(),
            WireMove::new(0, -100)
        );
    }

    #[test]
    fn wire_move_from_string_returns_errors_for_invalid_representation() {
        assert!(WireMove::from_string("").is_err());
        assert!(WireMove::from_string("L").is_err());
        assert!(WireMove::from_string("X1").is_err());
        assert!(WireMove::from_string("D-").is_err());
    }

    #[test]
    fn wire_path_from_string_returns_correct_path_for_valid_representation() {
        assert_eq!(
            WirePath::from_string("L1,U2").unwrap(),
            WirePath::new(vec![WireMove::new(-1, 0), WireMove::new(0, 2)])
        );
    }

    fn shortest_intersection_distance_for_wire_paths(
        wire_path1: &str,
        wire_path2: &str,
    ) -> Option<i64> {
        let mut grid = Grid::new();
        grid.run_wires_and_get_shortest_cross_distance(
            WirePath::from_string(wire_path1).unwrap(),
            WirePath::from_string(wire_path2).unwrap(),
        )
    }

    #[test]
    fn grid_run_wire_paths_returns_correct_distance() {
        assert_eq!(
            shortest_intersection_distance_for_wire_paths("R8,U5,L5,D3", "U7,R6,D4,L4"),
            Some(6)
        );
        assert_eq!(
            shortest_intersection_distance_for_wire_paths(
                "R75,D30,R83,U83,L12,D49,R71,U7,L72",
                "U62,R66,U55,R34,D71,R55,D58,R83"
            ),
            Some(159)
        );
        assert_eq!(
            shortest_intersection_distance_for_wire_paths(
                "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
                "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
            ),
            Some(135)
        );
    }
}
