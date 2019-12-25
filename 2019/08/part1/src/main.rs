use clap::crate_name;
use clap::App;
use clap::Arg;
use failure::format_err;
use std::fmt;
use std::fs;
use std::path::Path;
use std::path::PathBuf;
use std::str;

type Result<T> = std::result::Result<T, failure::Error>;
type PixelColor = u8;

struct Layer {
    layer: Vec<PixelColor>,
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

        let mut layer = Vec::new();
        for c in s.chars() {
            layer.push(
                c.to_digit(10)
                    .ok_or_else(|| format_err!("cannot convert {} to digit", c))?
                    as PixelColor,
            );
        }
        Ok(Layer { layer })
    }

    // Returns the number of pixels in the layer having the given color.
    pub fn pixel_color_count(&self, pixel_color: PixelColor) -> usize {
        bytecount::count(&self.layer, pixel_color)
    }
}

impl fmt::Display for Layer {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for pixel_color in &self.layer {
            write!(f, "{}", pixel_color.to_string())?;
        }
        Ok(())
    }
}

struct Image {
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
        Ok(Image { layers })
    }

    // Computes the checksum of the image. From the assignment:
    // To make sure the image wasn't corrupted during transmission, the Elves
    // would like you to find the layer that contains the fewest 0 digits. On
    // that layer, what is the number of 1 digits multiplied by the number of 2
    // digits?
    pub fn checksum(&self) -> usize {
        let mut layer_index_with_fewest_zeros = 0;
        let mut zero_count_in_layer_with_fewest_zeros = self.layers[0].pixel_color_count(0);

        for (i, layer) in self.layers[1..].iter().enumerate() {
            let zero_count = layer.pixel_color_count(0);
            if zero_count < zero_count_in_layer_with_fewest_zeros {
                layer_index_with_fewest_zeros = i + 1;
                zero_count_in_layer_with_fewest_zeros = zero_count;
            }
        }

        let ones = self.layers[layer_index_with_fewest_zeros].pixel_color_count(1);
        let twos = self.layers[layer_index_with_fewest_zeros].pixel_color_count(2);
        ones * twos
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
    println!("{}", image.checksum());
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn layer_from_string_creates_correct_layer_when_layer_repr_is_valid() {
        let layer_string = "123456";
        let layer = Layer::from_string(layer_string, 3, 2).unwrap();

        assert_eq!(layer.to_string(), layer_string);
    }

    #[test]
    fn layer_from_string_returns_error_when_string_is_too_short() {
        assert!(Layer::from_string("12345", 3, 2).is_err());
    }

    #[test]
    fn layer_from_string_returns_error_when_string_is_too_long() {
        assert!(Layer::from_string("1234567", 3, 2).is_err());
    }

    #[test]
    fn layer_from_string_returns_error_when_string_contains_non_digit_character() {
        assert!(Layer::from_string("12345x", 3, 2).is_err());
    }

    #[test]
    fn layer_pixel_color_count_returns_correct_number() {
        let layer = Layer::from_string("010100", 3, 2).unwrap();

        assert_eq!(layer.pixel_color_count(0), 4);
    }

    #[test]
    fn image_from_string_returns_correct_image_when_image_repr_is_valid() {
        let image_string = "123456789012";
        let image = Image::from_string(image_string, 3, 2).unwrap();

        assert_eq!(image.to_string(), image_string);
    }

    #[test]
    fn image_from_string_returns_error_when_image_is_too_short() {
        assert!(Image::from_string("12345678901", 3, 2).is_err());
    }

    #[test]
    fn image_from_string_returns_error_when_image_is_too_long() {
        assert!(Image::from_string("1234567890123", 3, 2).is_err());
    }

    #[test]
    fn image_checksum_returns_correct_number_when_image_has_single_layer() {
        let image = Image::from_string("111222", 3, 2).unwrap();

        assert_eq!(image.checksum(), 9);
    }

    #[test]
    fn image_checksum_returns_correct_number_when_image_has_multiple_layers() {
        let image = Image::from_string("009999122210", 3, 2).unwrap();

        assert_eq!(image.checksum(), 6);
    }
}
