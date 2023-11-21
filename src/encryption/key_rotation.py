"""
File: src/encryption/encryption.py

Author: Jiakai Peng
"""

import time
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes


class KeyRotationManager:
    def __init__(self):
        self.current_key = None
        self.current_salt = None
        self.key_generation_time = None

    def rotate_key(self):
        # Generate a new salt and key
        new_salt = get_random_bytes(16)
        self.current_salt = new_salt
        self.key_generation_time = int(time.time())

        return new_salt

    def get_current_key(self):
        if self.current_key is None:
            raise ValueError("No current key set. Generate a new key before getting one.")
        return self.current_key

    def get_key(self,password,salt):
        key = PBKDF2(password, salt, 32)
        self.current_key = key
        return key
