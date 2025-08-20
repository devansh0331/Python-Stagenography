# Steganography App

This is a Python-based steganography web application that allows users to encode and decode secret messages within image files. The application uses Flask for the backend and provides a modern web interface for user interaction.

## Features

- **Encode Messages**: Hide a secret message inside an image file.
- **Decode Messages**: Extract a hidden message from an encoded image file.
- **AES-256 Encryption**: Optionally encrypt messages for added security.
- **Modern Web Interface**: Intuitive and responsive UI with real-time feedback.
- **Downloadable Results**: Save encoded images directly from the browser.

## Requirements

- Python 3.x
- Required Python libraries:
  - `Flask`
  - `Pillow`
  - `cryptography`

## Installation

1. Clone or download this repository to your local machine.
2. Install the required Python libraries using pip:
   ```bash
   pip install flask pillow cryptography
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
4. Open your browser and navigate to `http://127.0.0.1:5000`.


## Usage

### Encoding
1. Upload an image file.
2. Enter the secret message.
3. (Optional) Enable encryption and provide a key or let the app generate one.
4. Click **Encrypt & Hide** to encode the message.
5. Download the encoded image.

### Decoding
1. Upload an encoded image file.
2. (Optional) Provide the encryption key if the message was encrypted.
3. Click **Extract Secret** to decode the message.

## How It Works

### Encoding
The application converts the message into binary format and embeds it into the least significant bits (LSBs) of the image's pixel data. If encryption is enabled, the message is encrypted using AES-256 before embedding.

### Decoding
The application reads the LSBs of the pixel data to reconstruct the binary message. If the message is encrypted, the provided key is used to decrypt it.

## File Structure

```
Steganography App/
├── app.py                # Flask application backend
├── steganography.py      # Core steganography logic
├── templates/
│   └── index.html        # HTML template for the web interface
├── static/
│   ├── css/
│   │   └── style.css     # Styles for the web interface
│   ├── js/
│   │   └── script.js     # JavaScript for interactivity
│   └── images/
│       └── favicon.ico   # Favicon for the web app
├── uploads/              # Directory for uploaded and processed files
├── Readme.md             # Project documentation
```

## Example

### Encoding
1. Upload an image file (e.g., `example.png`).
2. Enter a secret message (e.g., `Hello, World!`).
3. Enable encryption and save the generated key.
4. Download the encoded image (e.g., `encoded_example.png`).

### Decoding
1. Upload the encoded image (e.g., `encoded_example.png`).
2. Provide the encryption key if applicable.
3. Extract and view the hidden message.

## Limitations

- The size of the message is limited by the number of pixels in the image.
- Only supports images in formats compatible with the Pillow library (e.g., PNG, JPEG).

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Cryptography Documentation](https://cryptography.io/)
