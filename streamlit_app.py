# streamlit_app.py
import streamlit as st
from CaesarCipher import caesar_cipher_encrypt_decrypt
from PasswordStrength import check_password_strength
from streamlit_keylogger import keylogger_interface
from streamlit_pixel_manipulation import pixel_manipulation_interface

st.set_page_config(
    page_title="Cybersecurity Tools Demo",
    page_icon="🔒",
    layout="wide"
)

st.title("🔒 Cybersecurity Tools Demo")
st.write("A comprehensive collection of cybersecurity tools for educational and testing purposes.")

# Create tabs for different tools
tab1, tab2, tab3, tab4 = st.tabs(["🔐 Caesar Cipher", "🔑 Password Strength", "🔑 Key Logger", "🖼️ Image Encryption"])

with tab1:
    st.header("Caesar Cipher")
    st.write("Encrypt and decrypt text using the Caesar cipher algorithm.")
    
    text = st.text_input("Enter text:")
    shift = st.slider("Shift value:", 1, 25, 3)
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Encrypt", type="primary"):
            if text:
                result = caesar_cipher_encrypt_decrypt(text, shift, 'encrypt')
                st.success(f"Encrypted: {result}")
            else:
                st.warning("Please enter some text to encrypt.")

    with col2:
        if st.button("Decrypt", type="secondary"):
            if text:
                result = caesar_cipher_encrypt_decrypt(text, shift, 'decrypt')
                st.success(f"Decrypted: {result}")
            else:
                st.warning("Please enter some text to decrypt.")

with tab2:
    st.header("Password Strength Checker")
    st.write("Check the strength of your passwords and get detailed feedback.")
    
    password = st.text_input("Enter password:", type="password")
    if password:
        strength_result, strength_score = check_password_strength(password)
        st.info(f"Password Strength: {strength_score}/5")
        st.text_area("Detailed Analysis:", value=strength_result, height=200, disabled=True)
    else:
        st.info("Enter a password to check its strength.")

with tab3:
    keylogger_interface()

with tab4:
    pixel_manipulation_interface()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🔒 <strong>Cybersecurity Tools Demo</strong> - For educational and testing purposes only</p>
    <p>Built with Streamlit | Use responsibly and ethically</p>
</div>
""", unsafe_allow_html=True)