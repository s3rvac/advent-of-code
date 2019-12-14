#[macro_use]
extern crate failure;
#[macro_use]
extern crate clap;

use clap::App;
use clap::Arg;
use std::char;
use std::fmt;
use std::fs;
use std::path::Path;
use std::path::PathBuf;
use std::str;

type Result<T> = std::result::Result<T, failure::Error>;
type PixelColor = u8;

struct Layer {
    data: Vec<PixelColor>,
}

impl Layer {
    pub fn from_string(s: &str, width: usize, height: usize) -> Result<Self> {
        assert!(!s.is_empty(), "layer cannot be empty");
        assert!(width > 0, "width has to be positive");
        assert!(height > 0, "height has to be positive");

        if s.len() != width * height {
            return Err(format_err!(
                "layer '{}' has invalid length for width {} and height {}",
                s,
                width,
                height,
            ));
        }

        let mut data = Vec::new();
        for c in s.chars() {
            let pixel_color = c
                .to_digit(10)
                .ok_or_else(|| format_err!("cannot convert {} to digit", c))?;
            // Supported colors are 0, 1, 2.
            if pixel_color > 2 {
                return Err(format_err!("unsupported pixel color: {}", pixel_color));
            }
            data.push(pixel_color as PixelColor);
        }
        Ok(Layer { data })
    }
}

impl fmt::Display for Layer {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for pixel_color in &self.data {
            write!(f, "{}", pixel_color.to_string())?;
        }
        Ok(())
    }
}

struct Image {
    width: usize,
    height: usize,
    layers: Vec<Layer>,
}

impl Image {
    pub fn from_string(s: &str, width: usize, height: usize) -> Result<Self> {
        assert!(!s.is_empty(), "image cannot be empty");
        assert!(width > 0, "width has to be positive");
        assert!(height > 0, "height has to be positive");

        if s.len() % (width * height) != 0 {
            return Err(format_err!(
                "image '{}' has invalid length for width {} and height {}",
                s,
                width,
                height,
            ));
        }

        let mut layers = Vec::new();
        for layer_repr in s.as_bytes().chunks(width * height) {
            let layer_repr = str::from_utf8(layer_repr)?;
            layers.push(Layer::from_string(layer_repr, width, height)?);
        }
        Ok(Image {
            width,
            height,
            layers,
        })
    }

    pub fn decode(&self) -> String {
        let mut result = String::new();
        for row in 0..self.height {
            for col in 0..self.width {
                result.push(self.pixel_color_in_pos(self.width * row + col));
            }
            result.push('\n')
        }
        result
    }

    fn pixel_color_in_pos(&self, pos: usize) -> char {
        // From the assignment:
        // 0 is black, 1 is white, and 2 is transparent.
        let mut pixel_color = 2;
        for layer in self.layers.iter().rev() {
            pixel_color = match layer.data[pos] {
                0 => 0,
                1 => 1,
                2 => pixel_color,
                n => panic!("encountered an unsupported pixel color: {}", n),
            };
        }
        char::from_digit(pixel_color, 10).unwrap()
    }
}

impl fmt::Display for Image {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for layer in &self.layers {
            write!(f, "{}", layer.to_string())?;
        }
        Ok(())
    }
}

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

fn read_image_from_file(file_path: &Path, width: usize, height: usize) -> Result<Image> {
    let image_string = fs::read_to_string(file_path)?;
    Image::from_string(image_string.trim_end(), width, height)
}

fn main() -> Result<()> {
    let input_file = parse_args();
    // From the assignment:
    // The image you received is 25 pixels wide and 6 pixels tall.
    let image = read_image_from_file(&input_file, /*width*/ 25, /*height*/ 6)?;
    let decoded_image = image.decode();
    // Before printing the decoded message, replace zeros with a blank and ones
    // with '#' to make the message more readable.
    print!("{}", decoded_image.replace("0", " ").replace("1", "#"));
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn layer_from_string_creates_correct_layer_when_layer_repr_is_valid() {
        let layer_string = "111000";
        let layer = Layer::from_string(layer_string, 3, 2).unwrap();

        assert_eq!(layer.to_string(), layer_string);
    }

    #[test]
    fn layer_from_string_returns_error_when_string_is_too_short() {
        assert!(Layer::from_string("11111", 3, 2).is_err());
    }

    #[test]
    fn layer_from_string_returns_error_when_string_is_too_long() {
        assert!(Layer::from_string("1111111", 3, 2).is_err());
    }

    #[test]
    fn layer_from_string_returns_error_when_string_contains_non_digit_character() {
        assert!(Layer::from_string("11111x", 3, 2).is_err());
    }

    #[test]
    fn layer_from_string_returns_error_when_string_contains_unsupported_digit() {
        assert!(Layer::from_string("111113", 3, 2).is_err());
    }

    #[test]
    fn image_from_string_returns_correct_image_when_image_repr_is_valid() {
        let image_string = "111111222222";
        let image = Image::from_string(image_string, 3, 2).unwrap();

        assert_eq!(image.to_string(), image_string);
    }

    #[test]
    fn image_from_string_returns_error_when_image_is_too_short() {
        assert!(Image::from_string("11111111111", 3, 2).is_err());
    }

    #[test]
    fn image_from_string_returns_error_when_image_is_too_long() {
        assert!(Image::from_string("1111111111111", 3, 2).is_err());
    }

    fn decode_image(s: &str, width: usize, height: usize) -> String {
        Image::from_string(s, width, height).unwrap().decode()
    }

    #[test]
    fn image_decode_produces_correct_image() {
        assert_eq!(decode_image("000111", 3, 2), "000\n111\n");
        assert_eq!(decode_image("222222000111", 3, 2), "000\n111\n");
        assert_eq!(decode_image("000111222222", 3, 2), "000\n111\n");
        assert_eq!(decode_image("111111000000", 3, 2), "111\n111\n");
    }
}
