from cryptography.fernet import Fernet

# This key should be securely stored and not hardcoded
ENCRYPTION_KEY = Fernet.generate_key()  # Change this key in production
cipher = Fernet(ENCRYPTION_KEY)

def encrypt_file(data: bytes) -> bytes:
    """Encrypts file content"""
    return cipher.encrypt(data)

def decrypt_file(encrypted_data: bytes) -> bytes:
    """Decrypts file content"""
    return cipher.decrypt(encrypted_data)
