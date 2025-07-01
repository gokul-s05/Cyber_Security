"""
A simple Caesar cipher implementation for the Streamlit Cybersecurity Tools Demo.
This module provides encryption and decryption functionality using the Caesar cipher algorithm.
No GUI dependencies required - designed to work with Streamlit's web interface.
"""

def caesar_cipher_encrypt_decrypt(text, shift, mode):
    """
    Encrypt or decrypt text using Caesar cipher
    :param text: Text to encrypt/decrypt
    :param shift: Number of positions to shift
    :param mode: 'encrypt' or 'decrypt'
    :return: Encrypted/decrypted text
    """
    result = ''
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift if mode == 'encrypt' else ord(char) - shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            result += chr(shifted)
        else:
            result += char
    return result

if __name__ == '__main__':
    # Example usage
    text = "Hello, World!"
    shift = 3
    encrypted = caesar_cipher_encrypt_decrypt(text, shift, 'encrypt')
    decrypted = caesar_cipher_encrypt_decrypt(encrypted, shift, 'decrypt')
    print(f"Original: {text}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
