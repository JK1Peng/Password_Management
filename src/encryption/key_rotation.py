#by jiakai
import time
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from encryption_aes import AESmode
import xml.etree.ElementTree as ET
import psycopg2


# need change to the real database
fake_database = {
    "testing1": None,
    "testing2": None,
}


class KeyRotationManager:
    def __init__(self):
        self.current_key = None
        self.current_salt = None
        self.key_generation_time = None

    def rotate_key(self, user_id, master_password):
        # Generate a new salt and key
        new_salt = get_random_bytes(16)
        new_key = PBKDF2(master_password, new_salt, 32)
        
        # Update the current key, salt, and key generation time
        self.current_key = new_key
        self.current_salt = new_salt
        self.key_generation_time = int(time.time())
        
        # Update the XML file
        self.update_xml(user_id, new_key)

    def get_current_key(self):
        if self.current_key is None:
            raise ValueError("No current key set. Generate a new key before getting one.")
        return self.current_key
    
    def update_xml(self, user_id, key):
        # Create or update the XML file
        try:
            tree = ET.parse('keys.xml')
            root = tree.getroot()
        except FileNotFoundError:
            root = ET.Element('keys')
            tree = ET.ElementTree(root)
        
        # Find or create the user element
        user_element = None
        for elem in root.findall('user'):
            if elem.get('id') == user_id:
                user_element = elem
                break
        
        # If the user element does not exist, create it
        if user_element is None:
            user_element = ET.SubElement(root, 'user', {'id': user_id})
        
        # Add or update the key element
        key_element = user_element.find('key')
        if key_element is None:
            key_element = ET.SubElement(user_element, 'key')
        
        key_element.text = key.hex()
        
        # Write the updated XML file
        tree.write('keys.xml')

def reencrypt_database_data(old_key, new_key):
    # Loop through each record in the database
    for test_id, encrypted_data in fake_database.items():
        # Decrypt with the old key
        aes_decryptor = AESmode(old_key)
        decrypted_data = aes_decryptor.decrypt(encrypted_data)
        if decrypted_data is None:
            raise Exception(f"Decryption failed for record {test_id} with old key.")

        # Encrypt with the new key
        aes_encryptor = AESmode(new_key)
        new_encrypted_data = aes_encryptor.encrypt(decrypted_data)
        if new_encrypted_data is None:
            raise Exception(f"Encryption failed for record {test_id} with new key.")

        # Update the database record to the new encrypted data
        fake_database[test_id] = new_encrypted_data


# Example usage:
# Initialize the key manager
manager = KeyRotationManager()
user_id = "123"
master_password = "your_password"

# Generate a new key and store it in the XML file
manager.rotate_key(user_id, master_password)

# Get the current key
current_key = manager.get_current_key()
print("Current Key:", current_key)
