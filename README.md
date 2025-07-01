# Cyber Security Tools

A collection of cybersecurity tools with both GUI and web (Streamlit) interfaces for educational and testing purposes.

## Features

- **Caesar Cipher**: Encrypt and decrypt text using the classic Caesar cipher.
- **Password Strength Checker**: Analyze password strength and generate secure passwords.
- **Keylogger**: Demonstration of keylogging for educational use.
- **Image Pixel Manipulation**: Encrypt and decrypt images using pixel manipulation techniques.

## Project Structure

```
.
├── CaesarCipher.py                  # GUI for Caesar cipher
├── KeyLogger.py                     # GUI for keylogger
├── PasswordStrength.py              # GUI for password strength checker
├── PixelManipulation.py             # GUI for image encryption/decryption
├── streamlit_app.py                 # Main Streamlit app (all-in-one)
├── streamlit_keylogger.py           # Streamlit keylogger interface
├── streamlit_pixel_manipulation.py  # Streamlit image manipulation interface
```

## Requirements

- Python 3.7+
- [Streamlit](https://streamlit.io/)
- [Pillow](https://python-pillow.org/) (PIL)
- [opencv-python](https://pypi.org/project/opencv-python/)
- [pyperclip](https://pypi.org/project/pyperclip/) (for clipboard in password checker)

Install dependencies with:

```bash
pip install streamlit pillow opencv-python pyperclip
```

## How to Run

### GUI Applications

Each tool can be run as a standalone GUI app:

```bash
python CaesarCipher.py
python PasswordStrength.py
python KeyLogger.py
python PixelManipulation.py
```

### Streamlit Web App

To launch the all-in-one web app:

```bash
python -m streamlit run streamlit_app.py
```

Or run individual Streamlit interfaces:

```bash
streamlit run streamlit_keylogger.py
streamlit run streamlit_pixel_manipulation.py
```

## Usage Notes

- **Keylogger**: For educational and ethical use only. Do not use without consent.
- **Image Encryption**: Only supports common image formats (PNG, JPG, JPEG).
- **Password Strength**: Provides feedback and can generate random passwords.

## Disclaimer

This project is for educational and testing purposes only. Use responsibly and ethically. 
