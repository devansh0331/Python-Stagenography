# Steganography App

This is a simple Python-based steganography application that allows users to encode and decode secret messages within image files. The application provides a graphical user interface (GUI) built using Tkinter.

## Features

- **Encode Messages**: Hide a secret message inside an image file.
- **Decode Messages**: Extract a hidden message from an encoded image file.
- **User-Friendly Interface**: Simple and intuitive GUI for encoding and decoding operations.

## Requirements

- Python 3.x
- Required Python libraries:
  - `tkinter` (for GUI)
  - `Pillow` (for image processing)

## Installation

1. Clone or download this repository to your local machine.
2. Install the required Python libraries using pip:
   ```bash
   pip install pillow
   ```

## Usage

1. Run the application:
   ```bash
   python gui.py
   ```
2. Use the GUI to:
   - Enter a message in the "Message" field.
   - Click **Encode** to hide the message in an image file.
   - Click **Decode** to extract a hidden message from an encoded image file.

## How It Works

### Encoding
The application converts the message into binary format and embeds it into the least significant bits (LSBs) of the image's pixel data. A delimiter (`1111111111111110`) is added to mark the end of the message.

### Decoding
The application reads the LSBs of the pixel data to reconstruct the binary message. It stops reading when it encounters the delimiter and converts the binary data back into text.

## File Structure

```
Steganography App/
├── gui.py         # Main application file with GUI and steganography logic
├── Readme.md      # Project documentation
```

## Example

1. **Encoding**:
   - Select an image file.
   - Enter a secret message.
   - Save the encoded image.

2. **Decoding**:
   - Select an encoded image file.
   - View the extracted message.

## Limitations

- The size of the message is limited by the number of pixels in the image.
- Only supports images in formats compatible with the Pillow library (e.g., PNG, JPEG).

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
