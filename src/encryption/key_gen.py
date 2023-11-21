"""
File: src/encryption/key_gen.py

Author: Jiakai Peng
"""

import secrets
import string


class PasswordGenerator:
    def __init__(self, length=12, include_uppercase=True, include_digits=True, include_special=True):
        self.length = max(length, 4)
        self.include_uppercase = include_uppercase
        self.include_digits = include_digits
        self.include_special = include_special

    def generate(self):
        if self.length < 4:
            raise ValueError("at least be 4")

        characters = string.ascii_lowercase

        if self.include_uppercase:
            characters += string.ascii_uppercase
        if self.include_digits:
            characters += string.digits
        if self.include_special:
            special_chars = "!@#$%^&*()-_+=[]{}|;:<>/?"
            characters += special_chars

        password = ''.join(secrets.choice(characters) for _ in range(self.length))

        return password