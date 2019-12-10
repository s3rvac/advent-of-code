#[macro_use]
extern crate clap;
#[macro_use]
extern crate failure;

use clap::App;
use clap::Arg;
use failure::Error;
use std::convert::TryFrom;
use std::fs;
use std::path::Path;
use std::path::PathBuf;

type Result<T> = std::result::Result<T, Error>;
type Int = u64;

struct Program {
    memory: Vec<Int>,
}

impl Program {
    pub fn from_string(s: &str) -> Result<Self> {
        let mut memory = Vec::new();

        for int in s.split(',') {
            memory.push(int.parse()?);
        }

        Ok(Program { memory })
    }

    #[cfg(test)]
    pub fn to_string(&self) -> String {
        self.memory
            .iter()
            .map(|int| int.to_string())
            .collect::<Vec<String>>()
            .join(",")
    }

    pub fn output(&self) -> Int {
        // Program is always non-empty.
        self.memory[0]
    }

    pub fn restore_to_program_alarm_state(&mut self) -> Result<()> {
        // From the assignment: To restore the assist gravity program to the
        // "1202 program alarm" state, replace position 1 with the value
        // 12 and replace position 2 with the value 2.
        self.write_int_at(12, 1)?;
        self.write_int_at(2, 2)?;
        Ok(())
    }

    pub fn run(&mut self) -> Result<()> {
        let mut i = 0;
        loop {
            let opcode = self.current_opcode(i)?;
            match opcode {
                1 => {
                    // Addition.
                    i = self.perform_operation(i, |op1, op2| op1 + op2)?;
                }
                2 => {
                    // Multiplication.
                    i = self.perform_operation(i, |op1, op2| op1 * op2)?;
                }
                99 => {
                    // Halt.
                    return Ok(());
                }
                _ => {
                    return Err(format_err!("unsupported opcode: {}", opcode));
                }
            }
        }
    }

    fn current_opcode(&self, i: usize) -> Result<Int> {
        self.int_at(i)
    }

    fn perform_operation<F>(&mut self, i: usize, compute_result: F) -> Result<usize>
    where
        F: Fn(Int, Int) -> Int,
    {
        let (op1, op2) = self.operands_for_instruction_at(i)?;
        let result = compute_result(op1, op2);
        self.write_int_at(result, self.address_for_result(i)?)?;
        Ok(self.index_of_next_instruction(i))
    }

    fn operands_for_instruction_at(&self, i: usize) -> Result<(Int, Int)> {
        // Operation operands are given by the first and second integers.
        Ok((
            self.operand_for_instruction_at(i, 1)?,
            self.operand_for_instruction_at(i, 2)?,
        ))
    }

    fn operand_for_instruction_at(&self, i: usize, op: usize) -> Result<Int> {
        let addr = self.int_at(i + op)?;
        self.int_at(usize::try_from(addr)?)
    }

    fn int_at(&self, i: usize) -> Result<Int> {
        self.ensure_index_is_valid(i)?;
        Ok(self.memory[i])
    }

    fn address_for_result(&self, i: usize) -> Result<usize> {
        // Address for result is indicated by the third integer.
        Ok(usize::try_from(self.int_at(i + 3)?)?)
    }

    fn write_int_at(&mut self, int: Int, i: usize) -> Result<()> {
        self.ensure_index_is_valid(i)?;
        self.memory[i] = int;
        Ok(())
    }

    fn ensure_index_is_valid(&self, i: usize) -> Result<()> {
        if i >= self.memory.len() {
            return Err(format_err!("out-of-bounds access at index {}", i));
        }
        Ok(())
    }

    fn index_of_next_instruction(&self, i: usize) -> usize {
        // Once we are done processing an opcode, we have to move to the next
        // one by stepping forward 4 positions.
        i + 4
    }
}

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

fn read_input(input_path: &Path) -> Result<Program> {
    Program::from_string(fs::read_to_string(input_path)?.trim())
}

fn main() -> Result<()> {
    let input_file = parse_args();
    let mut program = read_input(&input_file)?;
    program.restore_to_program_alarm_state()?;
    program.run()?;
    println!("{}", program.output());
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn valid_program_from_string(s: &str) -> Program {
        Program::from_string(s).expect("The program was supposed to be valid")
    }

    fn run_valid_program_from_string(s: &str) -> String {
        let mut program = valid_program_from_string(s);
        program.run().expect("The program was supposed to be valid");
        program.to_string()
    }

    fn run_program_from_string(s: &str) -> Result<String> {
        let mut program = Program::from_string(s)?;
        program.run()?;
        Ok(program.to_string())
    }

    #[test]
    fn program_from_string_returns_correct_program_when_string_represents_valid_program() {
        let program = valid_program_from_string("1,0,0,3,99");

        assert_eq!(program.memory, vec![1, 0, 0, 3, 99]);
    }

    #[test]
    fn program_from_string_returns_error_when_string_represents_invalid_program_empty() {
        let program = Program::from_string("");

        assert!(program.is_err());
    }

    #[test]
    fn program_from_string_returns_error_when_string_represents_invalid_program_missing_int() {
        let program = Program::from_string("1,");

        assert!(program.is_err());
    }

    #[test]
    fn program_from_string_returns_error_when_string_represents_invalid_program_non_int() {
        let program = Program::from_string("x");

        assert!(program.is_err());
    }

    #[test]
    fn program_to_string_returns_correct_representation() {
        let program = valid_program_from_string("1,0,0,3,99");

        assert_eq!(program.to_string(), "1,0,0,3,99");
    }

    #[test]
    fn program_output_returns_value_at_first_address() {
        let program = valid_program_from_string("1");

        assert_eq!(program.output(), 1);
    }

    #[test]
    fn program_restore_to_program_alarm_state_correctly_modifies_program() {
        let mut program = valid_program_from_string("1,0,0,0,99");

        program
            .restore_to_program_alarm_state()
            .expect("Expected the restoration to succeed");

        assert_eq!(program.to_string(), "1,12,2,0,99");
    }

    #[test]
    fn program_restore_to_program_alarm_state_returns_error_when_no_such_position() {
        let mut program = valid_program_from_string("1");

        assert!(program.restore_to_program_alarm_state().is_err());
    }

    #[test]
    fn program_run_performs_correct_calculation() {
        assert_eq!(run_valid_program_from_string("1,0,0,0,99"), "2,0,0,0,99");
        assert_eq!(run_valid_program_from_string("2,3,0,3,99"), "2,3,0,6,99");
        assert_eq!(
            run_valid_program_from_string("2,4,4,5,99,0"),
            "2,4,4,5,99,9801"
        );
        assert_eq!(
            run_valid_program_from_string("1,1,1,4,99,5,6,0,99"),
            "30,1,1,4,2,5,6,0,99"
        );
    }

    #[test]
    fn program_run_fails_when_encountering_usupported_opcode() {
        assert!(run_program_from_string("7").is_err());
    }

    #[test]
    fn program_run_fails_when_getting_from_out_of_bounds_address() {
        assert!(run_program_from_string("1,30,0,0,99").is_err());
    }

    #[test]
    fn program_run_fails_when_writing_to_out_of_bounds_address() {
        assert!(run_program_from_string("1,0,0,30,99").is_err());
    }

    #[test]
    fn program_run_fails_when_missing_halt_instruction() {
        assert!(run_program_from_string("1,0,0,0").is_err());
    }
}
