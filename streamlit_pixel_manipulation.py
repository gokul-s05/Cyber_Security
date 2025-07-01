import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# Helper functions for session state

def get_state():
    if 'pixel_manipulation_state' not in st.session_state:
        st.session_state.pixel_manipulation_state = {
            'original_image': None,
            'encrypted_image': None,
            'key': None,
            'image_uploaded': False,
            'key_uploaded': False
        }
    return st.session_state.pixel_manipulation_state

class StreamlitPixelManipulation:
    def load_image(self, uploaded_file):
        state = get_state()
        try:
            image = Image.open(uploaded_file).convert('L')  # Always grayscale
            state['original_image'] = np.array(image)
            state['encrypted_image'] = None
            state['key'] = None
            state['image_uploaded'] = True
            state['key_uploaded'] = False
            return True
        except Exception as e:
            st.error(f"Error loading image: {e}")
            return False

    def load_encrypted_image(self, uploaded_file):
        state = get_state()
        try:
            image = Image.open(uploaded_file).convert('L')  # Always grayscale
            arr = np.array(image)
            state['encrypted_image'] = arr.astype(float) / 255.0
            state['original_image'] = None
            state['image_uploaded'] = True
            return True
        except Exception as e:
            st.error(f"Error loading encrypted image: {e}")
            return False

    def load_key(self, uploaded_file):
        state = get_state()
        try:
            key = np.load(uploaded_file)
            state['key'] = key
            state['key_uploaded'] = True
            return True
        except Exception as e:
            st.error(f"Error loading key: {e}")
            return False

    def encrypt_image(self):
        state = get_state()
        if state['original_image'] is None:
            st.error("Please upload an image first!")
            return False
        if state['encrypted_image'] is not None and state['key'] is not None:
            st.info("Image is already encrypted.")
            return True
        try:
            img = state['original_image']
            # Ensure grayscale uint8
            if img.dtype != np.uint8:
                img = img.astype(np.uint8)
            height, width = img.shape
            key = np.random.randint(0, 256, (height, width), dtype=np.uint8)
            encrypted_image = np.bitwise_xor(img, key)
            state['encrypted_image'] = encrypted_image
            state['key'] = key
            state['key_uploaded'] = False
            return True
        except Exception as e:
            st.error(f"Error encrypting image: {e}")
            return False

    def decrypt_image(self):
        state = get_state()
        if state['encrypted_image'] is None or state['key'] is None:
            st.error("No encrypted image or key available!")
            return None
        # Check shape match
        if state['encrypted_image'].shape != state['key'].shape:
            st.error(f"Shape mismatch: Encrypted image shape {state['encrypted_image'].shape} and key shape {state['key'].shape} do not match. Make sure you are using the correct key for this image.")
            return None
        try:
            decrypted_image = np.bitwise_xor(state['encrypted_image'], state['key'])
            return decrypted_image
        except Exception as e:
            st.error(f"Error decrypting image: {e}")
            return None

    def get_image_display(self, image_array):
        if image_array is None:
            return None
        if len(image_array.shape) == 2:
            pil_image = Image.fromarray(image_array.astype(np.uint8), mode='L')
        else:
            pil_image = Image.fromarray(image_array.astype(np.uint8))
        return pil_image

    def save_image(self, image_array):
        try:
            if len(image_array.shape) == 2:
                pil_image = Image.fromarray(image_array.astype(np.uint8), mode='L')
            else:
                pil_image = Image.fromarray(image_array.astype(np.uint8))
            buffer = io.BytesIO()
            pil_image.save(buffer, format='PNG')
            buffer.seek(0)
            return buffer
        except Exception as e:
            st.error(f"Error saving image: {e}")
            return None

    def save_key(self, key):
        try:
            buffer = io.BytesIO()
            np.save(buffer, key)
            buffer.seek(0)
            return buffer
        except Exception as e:
            st.error(f"Error saving key: {e}")
            return None

    def reset(self):
        state = get_state()
        state['original_image'] = None
        state['encrypted_image'] = None
        state['key'] = None
        state['image_uploaded'] = False
        state['key_uploaded'] = False

def pixel_manipulation_interface():
    st.header("🖼️ Image Encryption/Decryption")
    st.write("This tool encrypts and decrypts images using pixel manipulation techniques.")
    pm = StreamlitPixelManipulation()
    state = get_state()

    st.subheader("Upload Section")
    upload_mode = st.radio("What do you want to do?", ["Encrypt a new image", "Decrypt an encrypted image"], horizontal=True)

    if upload_mode == "Encrypt a new image":
        uploaded_file = st.file_uploader(
            "Choose an image file to encrypt", 
            type=['png', 'jpg', 'jpeg'],
            key="encrypt_image_upload",
            help="Upload an image to encrypt"
        )
        if uploaded_file is not None:
            if not state['image_uploaded']:
                if pm.load_image(uploaded_file):
                    st.success("Image loaded successfully!")

        if state['original_image'] is None:
            st.info("Please upload an image to begin.")
            return

        if state['original_image'] is not None:
            st.subheader("Original Image")
            original_display = pm.get_image_display(state['original_image'])
            if original_display:
                st.image(original_display, caption="Original Image", width=300)

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔒 Encrypt Image", type="primary"):
                    if pm.encrypt_image():
                        st.success("Image encrypted successfully!")
            with col2:
                if st.button("🔄 Reset", type="secondary"):
                    pm.reset()
                    st.success("Reset complete!")
                    st.experimental_rerun()

            if state['encrypted_image'] is not None:
                st.subheader("Encrypted Image")
                encrypted_display = pm.get_image_display((state['encrypted_image'] * 255).astype(np.uint8))
                if encrypted_display:
                    st.image(encrypted_display, caption="Encrypted Image", width=300)

                st.subheader("Download Options")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📥 Download Encrypted"):
                        encrypted_buffer = pm.save_image((state['encrypted_image'] * 255).astype(np.uint8))
                        if encrypted_buffer:
                            st.download_button(
                                label="Click to download encrypted image",
                                data=encrypted_buffer.getvalue(),
                                file_name="encrypted_image.png",
                                mime="image/png"
                            )
                with col2:
                    if st.button("📥 Download Key"):
                        key_buffer = pm.save_key(state['key'])
                        if key_buffer:
                            st.download_button(
                                label="Click to download key (.npy)",
                                data=key_buffer.getvalue(),
                                file_name="encryption_key.npy",
                                mime="application/octet-stream"
                            )
    else:
        encrypted_file = st.file_uploader(
            "Upload the encrypted image file", 
            type=['png', 'jpg', 'jpeg'],
            key="decrypt_image_upload",
            help="Upload the encrypted image you want to decrypt"
        )
        key_file = st.file_uploader(
            "Upload the key file (.npy)",
            type=['npy'],
            key="decrypt_key_upload",
            help="Upload the key file that was used for encryption"
        )
        if encrypted_file is not None:
            if pm.load_encrypted_image(encrypted_file):
                st.success("Encrypted image loaded successfully!")
        if key_file is not None:
            if pm.load_key(key_file):
                st.success("Key loaded successfully!")
        if state['encrypted_image'] is None:
            st.info("Please upload the encrypted image file to begin decryption.")
            return
        if state['key'] is None:
            st.info("Please upload the key file to enable decryption.")
            return
        if state['encrypted_image'] is not None:
            st.subheader("Encrypted Image Preview")
            encrypted_display = pm.get_image_display((state['encrypted_image'] * 255).astype(np.uint8))
            if encrypted_display:
                st.image(encrypted_display, caption="Encrypted Image", width=300)
            if st.button("🔓 Decrypt Image", type="primary"):
                decrypted_image = pm.decrypt_image()
                if decrypted_image is not None:
                    st.success("Image decrypted successfully!")
                    st.write('Decrypted min:', decrypted_image.min(), 'max:', decrypted_image.max())
                    st.subheader("Decrypted Image")
                    decrypted_display = pm.get_image_display(decrypted_image)
                    if decrypted_display:
                        st.image(decrypted_display, caption="Decrypted Image", width=300)
                    if st.button("📥 Download Decrypted"):
                        decrypted_buffer = pm.save_image(decrypted_image)
                        if decrypted_buffer:
                            st.download_button(
                                label="Click to download decrypted image",
                                data=decrypted_buffer.getvalue(),
                                file_name="decrypted_image.png",
                                mime="image/png"
                            )

    with st.expander("ℹ️ How to use"):
        st.write("""
        1. **Encrypt a new image**: Upload an image, click 'Encrypt Image', then download both the encrypted image and the key file.
        2. **Decrypt an encrypted image**: Upload the encrypted image and the key file you saved during encryption, then click 'Decrypt Image'.
        3. **Download**: Use the download buttons to save encrypted, decrypted images, and the key file.
        4. **Reset**: Click 'Reset' to clear the session and start over.
        
        **Technical Details:**
        - The encryption uses a random key generated from a normal distribution
        - Each pixel is divided by the corresponding key value
        - Decryption multiplies the encrypted pixels by the same key
        - The process works best with grayscale images
        
        **Note:** This tool is for educational and security testing purposes only.
        """) 