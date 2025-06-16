from PIL import Image
import numpy as np

def encrypt_image(input_path, output_path, key):
    # Load image and convert to RGB numpy array
    img = Image.open(input_path).convert("RGB")
    img_np = np.array(img)

    # Flatten the image and key to match length
    flat_img = img_np.flatten()
    key_np = np.frombuffer(key, dtype=np.uint8)
    key_expanded = np.resize(key_np, flat_img.shape)

    # XOR encryption
    encrypted_flat = np.bitwise_xor(flat_img, key_expanded)
    encrypted_img = encrypted_flat.reshape(img_np.shape)

    # Save encrypted image
    Image.fromarray(encrypted_img.astype(np.uint8)).save(output_path)

def decrypt_image(input_path, output_path, key):
    # Load encrypted image
    img = Image.open(input_path).convert("RGB")
    img_np = np.array(img)

    # Flatten and prepare key
    flat_img = img_np.flatten()
    key_np = np.frombuffer(key, dtype=np.uint8)
    key_expanded = np.resize(key_np, flat_img.shape)

    # XOR decryption
    decrypted_flat = np.bitwise_xor(flat_img, key_expanded)
    decrypted_img = decrypted_flat.reshape(img_np.shape)

    # Save decrypted image
    Image.fromarray(decrypted_img.astype(np.uint8)).save(output_path)
