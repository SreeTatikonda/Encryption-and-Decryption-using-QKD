import random
import time
from metrics import log_latency  # imported, now used below

def generate_random_bits(n):
    """Generate a list of n random bits (0 or 1)."""
    return [random.randint(0, 1) for _ in range(n)]

def generate_random_bases(n):
    """Generate a list of n random bases ('+' or 'x')."""
    return [random.choice(['+', 'x']) for _ in range(n)]

def measure(bit, basis):
    """Simulate quantum measurement with potential noise on 'x' basis."""
    if basis == '+':
        return bit
    return bit if random.random() > 0.5 else 1 - bit

def sift_keys(sender_bases, receiver_bases, sender_bits, receiver_bits):
    """Sift keys by comparing matching bases and bit agreement."""
    return [
        s_bit for s_bit, r_bit, s_base, r_base in
        zip(sender_bits, receiver_bits, sender_bases, receiver_bases)
        if s_base == r_base and s_bit == r_bit
    ]

def generate_qkd_key(n=128, simulate_eve=False):
    """
    Simulate QKD key exchange using the BB84 protocol.
    Returns a dictionary with key info and Eve detection flag.
    """
    start_time = time.time()

    sender_bits = generate_random_bits(n)
    sender_bases = generate_random_bases(n)

    if simulate_eve:
        eve_bases = generate_random_bases(n)
        intercepted_bits = [measure(b, e_basis) for b, e_basis in zip(sender_bits, eve_bases)]
        receiver_bases = generate_random_bases(n)
        receiver_bits = [measure(b, r_basis) for b, r_basis in zip(intercepted_bits, receiver_bases)]
    else:
        receiver_bases = generate_random_bases(n)
        receiver_bits = [measure(b, r_basis) for b, r_basis in zip(sender_bits, receiver_bases)]

    shared_key = sift_keys(sender_bases, receiver_bases, sender_bits, receiver_bits)
    time_taken = round(time.time() - start_time, 4)

    print(f"[Manual Timing] QKD took {time_taken:.4f} seconds")
    # Log latency for metrics

    eve_detected = simulate_eve and len(shared_key) < n * 0.4  # Heuristic detection

    return {
        'key': shared_key,
        'length': len(shared_key),
        'time': time_taken,
        'eve_detected': eve_detected
    }

if __name__ == "__main__":
    def test_qkd():
        result = generate_qkd_key(128, simulate_eve=True)
        print("QKD Key:", result['key'])
        print("Length:", result['length'])
        print("Time Taken (s):", result['time'])
        print("Eavesdropper Detected:", result['eve_detected'])

    test_qkd()
