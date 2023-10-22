from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64
import bcrypt

class AES:
    def __init__(self, key):
        self.key = key

    def encrypt(self, data):
        try:
            # pad to 128
            data = pad(data.encode('utf-8'), AES.block_size)
            # Randomly generate an initialization vector.
            iv = get_random_bytes(AES.block_size)
            # create using CBC chain mode
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            # Encrypt the data.
            encrypted_data = cipher.encrypt(data)
            # Combine the initialization vector and the encrypted data for future decryption. 
            return base64.b64encode(iv + encrypted_data).decode('utf-8')
        except Exception as e:
                print(f"An error occurred during encryption: {str(e)}")
                return None    

    def decrypt(self, encrypted_data):
        try:
            encrypted_data = base64.b64decode(encrypted_data) 
            iv = encrypted_data[:AES.block_size]       
            encrypted_data = encrypted_data[AES.block_size:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted_data = cipher.decrypt(encrypted_data)
         
            return unpad(decrypted_data, AES.block_size).decode('utf-8')
        except ValueError as e:
            print(f"Decryption failed: {str(e)}")
            return None
        except Exception as e:
            print(f"An error occurred during decryption: {str(e)}")
            return None 


# Simulate user registration adding bcrypot
# username = "example_user"
# master_password = "123456" 
# user_registration(username, master_password)
# def hash_password(password):
#     # Generate password hash with bcrypt.
#     return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# def check_password(password, hashed):
#     return bcrypt.checkpw(password.encode('utf-8'), hashed)

master_password = "123456"
# Generate a random salt each user
salt = get_random_bytes(16)
# use AES-256
key = PBKDF2(master_password, salt, 32)  

# test purpose
aes_cipher = AES(key)
data = "12345465" 
encrypted = aes_cipher.encrypt(data)
decrypted = aes_cipher.decrypt(encrypted)
print(f"Encrypted data: {encrypted}")
print(f"Decrypted data: {decrypted}")
