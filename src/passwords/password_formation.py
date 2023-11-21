from src.passwords.password_strength import password_check
from Crypto.Random import random

def generate_password():
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    numbers = "1234567890"
    symbols = "!@#$%^&*.,;"
    alphabet = uppercase + lowercase + numbers + symbols
    password = "a"
    while password_check(password) is not True:
        password = ""
        for i in range(15):
            password += alphabet[random.randint(0, len(alphabet) - 1)]
    return password
