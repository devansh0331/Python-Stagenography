from PIL import Image
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def generate_aes_key():
    return AESGCM.generate_key(bit_length=256)

def encrypt_message(key: bytes, plaintext: str):
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
    return nonce + ciphertext  # Combine nonce and ciphertext for easier handling

def decrypt_message(key: bytes, encrypted_data: bytes):
    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None).decode()

def encode_image(image_path, message, output_path, key=None):
    img = Image.open(image_path)
    if img.mode not in ('RGB', 'RGBA'):
        img = img.convert('RGB')
    
    # Encrypt the message if a key is provided
    if key:
        encrypted_data = encrypt_message(key, message)
        # Convert the encrypted bytes to binary string
        binary_msg = ''.join(format(byte, '08b') for byte in encrypted_data)
    else:
        binary_msg = ''.join(format(ord(c), '08b') for c in message)
    
    binary_msg += '1111111111111110'  # Add delimiter
    
    if len(binary_msg) > img.width * img.height * 3:
        raise ValueError("Message too large for image!")
    
    pixels = list(img.getdata())
    new_pixels = []
    msg_index = 0
    
    for pixel in pixels:
        if msg_index < len(binary_msg):
            new_pixel = list(pixel)
            for i in range(3):
                if msg_index < len(binary_msg):
                    new_pixel[i] = new_pixel[i] & ~1 | int(binary_msg[msg_index])
                    msg_index += 1
            new_pixels.append(tuple(new_pixel))
        else:
            new_pixels.append(pixel)
    
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_pixels)
    new_img.save(output_path, format='PNG')

def decode_image(image_path, key=None):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    binary_msg = ""
    
    for pixel in pixels:
        for channel in pixel[:3]:  # R, G, B channels
            binary_msg += str(channel & 1)
    
    delimiter = '1111111111111110'
    if delimiter in binary_msg:
        msg_bits = binary_msg.split(delimiter)[0]
        
        if key:
            # Convert binary string back to bytes
            encrypted_bytes = bytes(int(msg_bits[i:i+8], 2) for i in range(0, len(msg_bits), 8))
            try:
                message = decrypt_message(key, encrypted_bytes)
                return message
            except Exception as e:
                return f"Decryption failed: {str(e)}"
        else:
            # Original decoding for unencrypted messages
            message = ""
            for i in range(0, len(msg_bits), 8):
                byte = msg_bits[i:i+8]
                message += chr(int(byte, 2))
            return message
    return "No hidden message found"