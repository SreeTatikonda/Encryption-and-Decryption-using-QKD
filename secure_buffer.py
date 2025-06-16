from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from metrics import log_latency

# AES Helper Functions
def pad(s):
    return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

def unpad(s):
    return s[:-ord(s[len(s) - 1:])]

def encrypt_aes(message, key):
    key = key[:32].ljust(32, '0').encode()  # AES-256
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(message).encode())
    return base64.b64encode(iv + ciphertext).decode()

def decrypt_aes(ciphertext, key):
    key = key[:32].ljust(32, '0').encode()
    raw = base64.b64decode(ciphertext)
    iv = raw[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(raw[16:])).decode()
    return decrypted

# OTP Encryption
def encrypt_otp(message, key_bits):
    key_stream = ''.join(map(str, key_bits))[:len(message)*8]
    if len(key_stream) < len(message)*8:
        raise ValueError("QKD key too short for OTP")
    message_bits = ''.join(f'{ord(c):08b}' for c in message)
    encrypted_bits = ''.join(str(int(a)^int(b)) for a, b in zip(message_bits, key_stream))
    return encrypted_bits

def decrypt_otp(encrypted_bits, key_bits):
    key_stream = ''.join(map(str, key_bits))[:len(encrypted_bits)]
    decrypted_bits = ''.join(str(int(a)^int(b)) for a, b in zip(encrypted_bits, key_stream))
    message = ''.join(chr(int(decrypted_bits[i:i+8], 2)) for i in range(0, len(decrypted_bits), 8))
    return message

# Controller Functions
def encrypt_message(message, key, method="AES"):
    if method == "AES":
        return encrypt_aes(message, key)
    elif method == "OTP":
        return encrypt_otp(message, key)
    else:
        raise ValueError("Unknown encryption method")

def decrypt_message(ciphertext, key, method="AES"):
    if method == "AES":
        return decrypt_aes(ciphertext, key)
    elif method == "OTP":
        return decrypt_otp(ciphertext, key)
    else:
        raise ValueError("Unknown decryption method")
