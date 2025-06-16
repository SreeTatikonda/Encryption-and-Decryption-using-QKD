import streamlit as st
from qkd_simulation import generate_qkd_key
from secure_buffer import encrypt_message, decrypt_message
import pyqrcode
from PIL import Image
import io

import time

# ------------------------------
# Initial Setup
# ------------------------------
st.set_page_config(page_title="Quantum Secure Chat", layout="centered")
st.title("🔐 Quantum-Enhanced Secure Communication")

# ------------------------------
# Initialize Session State
# ------------------------------
def init_session():
    st.session_state.setdefault("qkd_key", [])
    st.session_state.setdefault("last_cipher", "")

init_session()

# ------------------------------
# Sidebar: Key Generation
# ------------------------------
st.sidebar.header("🔑 Key Management")

key_length = st.sidebar.slider("QKD Key Length (bits)", 64, 512, 128)
simulate_eve = st.sidebar.checkbox("Simulate Eve", value=False)

if st.sidebar.button("Generate QKD Key"):
    result = generate_qkd_key(n=key_length, simulate_eve=simulate_eve)
    st.session_state.qkd_key = result['key']
    
    st.sidebar.success(f"✅ Key generated: {result['length']} bits")
    if result['eve_detected']:
        st.sidebar.error("⚠️ Eve detected! Discard this key.")
    elif result['length'] < 64:
        st.sidebar.warning("⚠️ Warning: QKD key too short.")
    else:
        st.sidebar.info("Secure key established.")

# ------------------------------
# QR Code Generator
# ------------------------------
def generate_qr(data: str) -> io.BytesIO:
    """Generate QR code image from string data."""
    qr = pyqrcode.create(data)
    buffer = io.BytesIO()
    qr.png(buffer, scale=5)
    buffer.seek(0)
    return buffer

st.subheader("📡 Share Key via QR Code")

if st.session_state.qkd_key:
    key_str = ''.join(map(str, st.session_state.qkd_key))
    qr_buffer = generate_qr(key_str)
    st.image(qr_buffer, caption="Scan this QR to retrieve QKD key")
    st.download_button("⬇️ Download QR", qr_buffer, file_name="qkd_key.png")
else:
    st.info("ℹ️ No QKD key available for QR generation.")

# ------------------------------
# Secure Messaging Section
# ------------------------------
st.subheader("✉️ Send a Secure Message")

message = st.text_input("Enter your message:")
method = st.radio("Encryption Method", ["AES", "OTP"])

# ------------------------------
# Encrypt
# ------------------------------
if st.button("🔒 Encrypt"):
    if not st.session_state.qkd_key:
        st.error("❌ No QKD key available.")
    elif not message.strip():
        st.error("❌ Message cannot be empty.")
    else:
        try:
            key = (
                ''.join(map(str, st.session_state.qkd_key)) 
                if method == "AES" else st.session_state.qkd_key
            )

            if method == "OTP" and len(st.session_state.qkd_key) < len(message):
                st.warning("⚠️ OTP key is shorter than message length — result may be truncated.")

            start_time = time.time()
            cipher = encrypt_message(message, key, method)
            elapsed = round(time.time() - start_time, 4)
            st.session_state.last_cipher = cipher

            st.success(f"✅ Encrypted in {elapsed}s")
            st.code(cipher)

        except Exception as e:
            st.error(f"Encryption Error: {e}")

# ------------------------------
# Decrypt
# ------------------------------
if st.button("🔓 Decrypt"):
    if not st.session_state.last_cipher:
        st.warning("⚠️ No message to decrypt.")
    elif not st.session_state.qkd_key:
        st.error("❌ No QKD key found.")
    else:
        try:
            key = (
                ''.join(map(str, st.session_state.qkd_key)) 
                if method == "AES" else st.session_state.qkd_key
            )

            start_time = time.time()
            plaintext = decrypt_message(st.session_state.last_cipher, key, method)
            elapsed = round(time.time() - start_time, 4)

            st.success(f"✅ Decrypted in {elapsed}s")
            st.code(plaintext)

        except Exception as e:
            st.error(f"Decryption Error: {e}")
