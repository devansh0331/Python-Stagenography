from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def encrypt_message(key: bytes, plaintext: str, associated_data: bytes = None):
    # Generate a 96-bit (12-byte) nonce
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), associated_data)
    return nonce, ciphertext

def decrypt_message(key: bytes, nonce: bytes, ciphertext: bytes, associated_data: bytes = None):
    aesgcm = AESGCM(key)
    decrypted_text = aesgcm.decrypt(nonce, ciphertext, associated_data)
    return decrypted_text.decode()

if __name__ == "__main__":
    # AES-256 requires a 32-byte key (AES-128 -> 16 bytes, AES-192 -> 24 bytes)
    key = AESGCM.generate_key(bit_length=256)

    message = "Hello, AES-GCM encryption!"
  
    # Encrypt
    print("Original message:", message)
    print("--------------------------")
    print("Encrypting...")
    nonce, ciphertext = encrypt_message(key, message, None)
    print("Nonce:", nonce.hex())
    print("Ciphertext:", ciphertext.hex())
    print("--------------------------")
    # Decrypt
    print("Decrypting...")
    decrypted = decrypt_message(key, nonce, ciphertext, None)
    print("Decrypted:", decrypted)