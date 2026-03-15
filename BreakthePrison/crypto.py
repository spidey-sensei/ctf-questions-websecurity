import hashlib


def xor(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])


def encrypt_flag(flag, secret):
    key = hashlib.md5(secret.encode()).digest()
    return xor(flag.encode(), key).hex()


def decrypt_flag(cipher_hex, secret):
    key = hashlib.md5(secret.encode()).digest()
    cipher = bytes.fromhex(cipher_hex)
    return xor(cipher, key).decode()