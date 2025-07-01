import cv2
import numpy as np
import os

class ImageEncryption:
    def __init__(self):
        self.image = None
        self.encrypted_image = None
        self.key = None

    def load_image(self, image_path):
        """Load an image from path"""
        if not os.path.exists(image_path):
            raise FileNotFoundError("Image file not found")
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError("Failed to load image")
        return True

    def encrypt_image(self):
        """Encrypt the loaded image"""
        if self.image is None:
            raise ValueError("No image loaded")
            
        # Generate a random key
        self.key = np.random.randint(0, 256, self.image.shape, dtype=np.uint8)
        # Encrypt the image
        self.encrypted_image = cv2.bitwise_xor(self.image, self.key)
        return True

    def decrypt_image(self, encrypted_image=None, key=None):
        """Decrypt an image using the key"""
        if encrypted_image is not None:
            self.encrypted_image = encrypted_image
        if key is not None:
            self.key = key
            
        if self.encrypted_image is None or self.key is None:
            raise ValueError("No encrypted image or key available")
            
        # Decrypt the image using XOR operation
        decrypted_image = cv2.bitwise_xor(self.encrypted_image, self.key)
        return decrypted_image

    def save_image(self, image, filepath):
        """Save an image to filepath"""
        if image is None:
            raise ValueError("No image to save")
        return cv2.imwrite(filepath, image)

    def save_key(self, filepath):
        """Save the encryption key"""
        if self.key is None:
            raise ValueError("No key to save")
        return np.save(filepath, self.key)

    def load_key(self, filepath):
        """Load an encryption key"""
        if not os.path.exists(filepath):
            raise FileNotFoundError("Key file not found")
        self.key = np.load(filepath)
        return True

if __name__ == '__main__':
    # Example usage
    encryptor = ImageEncryption()
    
    try:
        # Load and encrypt an image
        encryptor.load_image("example.jpg")
        encryptor.encrypt_image()
        
        # Save encrypted image and key
        encryptor.save_image(encryptor.encrypted_image, "encrypted.jpg")
        encryptor.save_key("key.npy")
        
        # Decrypt and save the result
        decrypted = encryptor.decrypt_image()
        encryptor.save_image(decrypted, "decrypted.jpg")
        
        print("Image encryption/decryption completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")