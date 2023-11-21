"""
File: src/database/user_controller.py

Author: Aaron Kersten, amk9398@rit.edu

Description: Contains all functions and logic the GUI needs to interact with
    the database, including login & signup functionality as well as updating
    the user's password information.
"""

from src.database.postgres import connect, execute_query, execute_update
import datetime
import pyotp
import src.encryption.key_rotation as key_rotate
import src.encryption.encryption as AESmode
from Crypto.Protocol.KDF import PBKDF2


""" 
@param: username: the user's username
@param: password: the user's master password
@return: user_id for successful login
         0 for incorrect username or password
         -1 for a database connection error
         -2 for unverified user

Allows a user to authenticate themself with the database and establish a connection.
"""
def login(username, password):
    # get database connection
    db = connect()
    if db is not None:
        # get master password for the current user
        query_response = execute_query(db,
                                       "SELECT master_password, verified,key FROM users WHERE username = %(username)s;",
                                       {"username": username})

        # check that a password was returned
        if (len(query_response)) == 1:
            master_password, verified, key = query_response[0]
            key = key.replace(r'\x', '')
            key = bytes.fromhex(key)
            aes_r = AESmode.AESmode(key)
            master_password = aes_r.decrypt(master_password)

            # return error code -2 for unverified user
            if not verified:
                return -2

            # get number of failed logins for this username
            num_failed_logins = execute_query(db, f"SELECT login_counter FROM users WHERE username = %(username)s;",
                                              {"username": username})[0][0]

            # if number of failed logins exceeds 5, return error code -2
            if num_failed_logins >= 5:
                # reset login counter
                execute_update(db, f"UPDATE users SET login_counter = 0 WHERE username = %(username)s;",
                               {"username": username})
                # set verified to false
                execute_update(db, f"UPDATE users SET verified = false WHERE username = %(username)s",
                               {"username": username})
                return -2

            # if the passwords match, return the user id and close the connection
            if master_password == password:
                user_id = execute_query(db, f"SELECT user_id FROM users WHERE username = %(username)s;",
                                        {"username": username})[0][0]

                # # twoFactorA secret
                # totp_secret = execute_query(db, f"SELECT totp_secret FROM users WHERE username = %(username)s;",
                #                             {"username": username})[0][0]
                # # twoFactorA code
                # user_input_totp = input("Enter the TOTP from your app: ")
                # totp = pyotp.TOTP(totp_secret)
                # if totp.verify(user_input_totp):
                #     return user_id
                # else:
                #     # if fail
                #     return -3

                # update user's last accessed date
                ct = datetime.datetime.now()
                execute_update(db, f"UPDATE users SET last_accessed_datetime = '{ct}' WHERE user_id = {user_id};")

                # set user's failed login number to 0
                execute_update(db, f"UPDATE users SET login_counter = 0 WHERE user_id = {user_id};")

                # set verified to true
                execute_update(db, f"UPDATE users SET verified = true WHERE user_id = {user_id};")

                db.close()
                return user_id

            else:
                # increment num failed logins by one
                execute_update(db, f"UPDATE users SET login_counter = {num_failed_logins + 1} WHERE username = "
                                   f"%(username)s;", {"username": username})

                # return error code 0 for failed login
                db.close()
                return 0

        # if more or less than one password was found, return error code 0
        else:
            db.close()
            return 0
    else:
        print("Could not access to the database while processing login request.")

    # if a connection could not be established, return -1
    return -1


"""
@param: username: username of new user
@param: password: master password of new user
@parma: email: email of new user:
@return: user_id for successful signup and login
         0 for duplicate username or email error
         -1 for database connection error

Allows a user to make a new account and get their user id.
"""
def sign_up(username, password, email, hint=None):
    # get database connection
    db = connect()
    if db is not None:
        # get number of users with the same username
        username_check = execute_query(db, f"SELECT COUNT(*) FROM users WHERE username = %(username)s;",
                                       {"username": username})[0][0]

        # get number of users with the same email
        email_check = execute_query(db, f"SELECT COUNT(*) FROM users WHERE email = %(email)s;",
                                    {"email": email})[0][0]

        # check that there are no users with the same username or email, if not return 0
        if username_check > 0:
            db.close()
            return 0

        if email_check > 0:
            db.close()
            return 0

        # get current timestamp
        ct = datetime.datetime.now()
        # set hint to first four characters of the password
        if hint is None:
            hint = password[:min(4, len(password))] + "..."

        manager = key_rotate.KeyRotationManager()
        new_salt = manager.rotate_key()
        new_key = PBKDF2(password, new_salt, 32)
        aes_encryption = AESmode.AESmode(new_key)
        # set 2fa secret
        secret = pyotp.random_base32()
        password = aes_encryption.encrypt(password)
        # print(new_salt)
        # add new user to the users table in the database(your version)
        # execute_update(db, f"INSERT INTO users (username, master_password, email, created_datetime, "
        #                    f"last_accessed_datetime, hint) "
        #                    f"VALUES (%(username)s, %(master_password)s, %(email)s, '{ct}', '{ct}', %(hint)s);",
        #                {"username": username, "master_password": password, "email": email,
        #                 "hint": hint,
        #                 "created_datetime": ct, "last_accessed_datetime": ct})
        execute_update(db, f"INSERT INTO users (username, master_password, email, created_datetime, "
                           f"last_accessed_datetime, hint, secret, salt, key) "
                           f"VALUES (%(username)s, %(master_password)s, %(email)s, %(created_datetime)s, "
                           f"%(last_accessed_datetime)s, %(hint)s, %(secret)s, %(salt)s, %(key)s);",
                       {"username": username, "master_password": password, "email": email,
                        "hint": hint, "secret": secret, "salt": new_salt, "key": new_key,
                        "created_datetime": ct, "last_accessed_datetime": ct})

        print(2)
        # close connection and login to retrieve and return user_id
        db.close()
        return 1
    else:
        print("Could not access the database while processing sign up request.")

    # if a connection could not be established, return -1
    return -1


"""
@param: user_id: user's id
@param: query: optional search filter
@result: a list of tuples for each password with the form:
    (domain, account_name, url, password),
    0 if query is invalid

Gets all passwords for a specific user. Can also be filtered using a search term.
"""
def get_user_passwords(user_id, query=""):
    # get database connection
    db = connect()
    decrypted_passwords = []
    if db is not None:

        # if no query is given, grab the entire password repo
        if query == "":
            passwords = execute_query(db, "SELECT domain, account_name, url, password, category_name, color, entry_id "
                                          "FROM passwords "
                                          "INNER JOIN categories on passwords.category_id = categories.category_id "
                                          f"WHERE passwords.user_id = {user_id} ORDER BY domain")

            query_response = execute_query(db, "SELECT key FROM users WHERE user_id = %(user_id)s;",
                                           {"user_id": user_id})

            key = query_response[0][0]
            key = key.replace(r'\x', '')
            key = bytes.fromhex(key)
            aes_r = AESmode.AESmode(key)

            for password in passwords:
                decrypted_password = aes_r.decrypt(password[3])
                decrypted_passwords.append((password[0], password[1], password[2], decrypted_password, password[4],
                                            password[5], password[6]))

        # otherwise, only grab entries with a domain, account name, or url like '...<query>...'
        else:

            # make sure that query does not contain quotations
            if "\'" in query or "\"" in query:
                return 0

            passwords = execute_query(db, f"SELECT domain, account_name, url, password, category_name, color, entry_id "
                                          f"FROM passwords p INNER JOIN categories c on p.category_id = c.category_id "
                                          f"WHERE p.user_id = {user_id} AND (LOWER(domain) LIKE '%{query}%' OR "
                                          f"LOWER(account_name) LIKE '%{query}%' OR LOWER(url) LIKE '%{query}%')"
                                          f"ORDER BY domain;")

            query_response = execute_query(db, "SELECT key FROM users WHERE user_id = %(user_id)s;",
                                           {"user_id": user_id})
            key = query_response[0][0]
            key = key.replace(r'\x', '')
            key = bytes.fromhex(key)
            aes_r = AESmode.AESmode(key)

            for password in passwords:
                decrypted_password = aes_r.decrypt(password[3])
                decrypted_passwords.append((password[0], password[1], password[2], decrypted_password, password[4],
                                            password[5], password[6]))

        # close connection and return passwords
        db.close()
        return decrypted_passwords
    else:
        print("Could not access the database while processing get-password request")

    # if a connection could not be established, return -1
    return -1


"""
@param: user_id: user's id
@param: domain: domain name of new password
@param: password: password string to be added
@param: account_name: account name of new password
@param: url: url of new password account
@return: 1 for successful add
         0 for existing password error
         -1 for database connection error

Adds a password the user's password repo.
"""
def add_password(user_id, domain, password, account_name="", url="", category="-"):
    # get database connection
    db = connect()
    if db is not None:
        # get count of user's with matching domain and account names
        matching_pswrd = execute_query(db, f"SELECT COUNT(*) FROM passwords WHERE domain = %(domain)s AND "
                                           f"account_name = %(account_name)s AND user_id = {user_id};",
                                       {"domain": domain, "account_name": account_name})[0][0]

        # if there is an existing password with matching domain and account name, return 0
        if matching_pswrd > 0:
            db.close()
            return 0

        if category == "-":
            category_id = 0
        else:
            category_id = execute_query(db, f"SELECT category_id FROM categories WHERE category_name = %(category)s "
                                            f"AND user_id = {user_id};",
                                        {"category": category})[0][0]

        # get current timestamp
        ct = datetime.datetime.now()

        query_response = execute_query(db, "SELECT key FROM users WHERE user_id = %(user_id)s;",
                                       {"user_id": user_id})

        # encrypt password
        key = query_response[0][0]
        key = key.replace(r'\x', '')
        key = bytes.fromhex(key)
        aes_r = AESmode.AESmode(key)
        password = aes_r.encrypt(password)

        # add new password to user's password repo
        execute_update(db, f"INSERT INTO passwords (user_id, domain, account_name, url, password, created_datetime, "
                           f"last_modified_datetime, category_id) VALUES ({user_id}, %(domain)s, %(account_name)s, "
                           f"%(url)s, %(password)s, '{ct}', '{ct}', {category_id});",
                       {"domain": domain, "account_name": account_name, "url": url, "password": password})

        # upon successful insert, close connection and return 1
        db.close()
        return 1
    else:
        print("Could not access the database while adding a password")

    # if a connection could not be established, return -1
    return -1


"""
@param: user_id: user's id
@param: domain: password domain name
@param: account_name: password account name
@return: 1 for successful removal
         -1 for database connection error

Remove password from user repo.
"""
def remove_password(user_id, domain, account_name):
    # get database connection
    db = connect()
    if db is not None:
        # remove password with given domain and account name from the repo
        execute_update(db, f"DELETE FROM passwords WHERE user_id = {user_id} AND domain = %(domain)s AND "
                           f"account_name = %(account_name)s;",
                       {"domain": domain, "account_name": account_name})

        # upon successful removal, close connection and return 1
        db.close()
        return 1
    else:
        print("Could not access the database while removing a password")

    # if a connection could not be established, return -1
    return -1


"""
@param: user_id: user's id
@param: username: user's username
@return: 1 for successful removal
         0 if both user_id and username are None
         -1 for database connection error

Remove account for given user id or username.
"""
def remove_account(user_id=None, username=None):
    db = connect()
    if db is not None:
        # check which parameter was left as None, as user the other to
        #   index the users table
        if username is None:
            execute_update(db, f"DELETE FROM users WHERE user_id={user_id}")

        elif user_id is None:
            execute_update(db, f"DELETE FROM users WHERE username='{username}'")

        # if both are left None, return error code 0
        else:
            return 0

        db.close()
        return 1
    else:
        print("Could not access the database while removing account")

    return -1


"""
@param: user_id: user's id
@param: username: user's username
@return: user's email upon successulf retrieval
         0 if both user_id and username are None
         -1 for database connection error

Get email for given user id or username
"""
def get_user_email(user_id=None, username=None):
    db = connect()
    if db is not None:
        # check which parameter was left as None, as user the other to
        #   index the users table
        if username is None:
            email = execute_query(db, f"SELECT email FROM users WHERE user_id={user_id}")[0][0]
            db.close()
            return email

        elif user_id is None:
            email = execute_query(db, f"SELECT email FROM users WHERE username=%(username)s",
                                  {"username": username})[0][0]
            db.close()
            return email

        # if both parameters are left None, return 0
        db.close()
        return 0
    else:
        print("Could not access the database while getting user email")

    return -1


"""
@param: user_id: user's id
@param: username: user's username
@return: 1 for successful verification
         0 if both user_id and username are None
         -1 for database connection error

Set 'verified' to true for given user id or username
"""
def verify_user(user_id=None, username=None):
    db = connect()
    if db is not None:
        # check which parameter was left as None, as user the other to
        #   index the users table
        if username is None:
            execute_update(db, f"UPDATE users SET verified = true WHERE user_id={user_id}")

        elif user_id is None:
            execute_update(db, f"UPDATE users SET verified = true WHERE username='{username}'")

        # if both paramters are NOne, return 0
        else:
            db.close()
            return 0

        db.close()
        return 1
    else:
        print("Could not access the database while verifying user")

    return -1


"""
@param: username: user's username
@param: email: user's email
@return: 1 for successful match
         0 for unsuccessful match
         -1 for database connection error

Check that given username and email match.
"""
def check_user_email(username, email):
    db = connect()
    if db is not None:
        response = execute_query(db, f"SELECT * FROM users WHERE username = %(username)s AND email = %(email)s",
                                 {"username": username, "email": email})

        # check that there is at least one response
        if len(response) > 0:
            db.close()
            return 1

        # if not, return 0
        return 0
    else:
        print("Could not access the database while checking user email")

    return -1


"""
@param: username: user's username
@return: hint upon successful retrieval
         0 for unsuccessful retrieval
         -1 for database connection error

Get user's password hint.
"""
def get_user_hint(username):
    db = connect()
    if db is not None:
        response = execute_query(db, f"SELECT hint FROM users WHERE username = %(username)s;",
                                 {"username": username})

        # if at least one response is retrieved, return the hint
        if len(response) > 0:
            db.close()
            return response[0][0]

        # if not, return 0
        return 0
    else:
        print("Could not access the database while getting user hint")

    return -1


"""
@param: user_id: user's id
@param: category_name: password category name
@return: 1 for successful add
         0 for attempt to add duplicate category
         -1 for database error

Add password category for a user.
"""
def add_category(user_id, category_name):
    db = connect()
    if db is not None:
        response = execute_query(db, f"SELECT * FROM categories WHERE user_id = {user_id} "
                                     f"AND category_name = %(category)s;",
                                 {"category": category_name})

        # check that no category of the same name exists
        if len(response) != 0:
            db.close()
            return 0

        # if not, add new category to categories table
        execute_update(db, f"INSERT INTO categories (user_id, category_name) VALUES ({user_id}, %(category)s);",
                       {"category": category_name})
        db.close()
        return 1
    else:
        print("Could not access the database adding category")

    return -1


"""
@param: user_id: user's id
@return: list of user categories
         -1 for database error

Get list of user's password categories.
"""
def get_user_categories(user_id):
    db = connect()
    if db is not None:
        response = execute_query(db, f"SELECT category_id, category_name, color FROM categories "
                                     f"WHERE user_id = {user_id} AND category_id != 0;")
        db.close()
        return response
    else:
        print("Could not access the database while getting user categories")

    return -1


"""
@param: category_id: password category id
@return: list of passwords
         -1 for database error

Get list of passwords for a category.
"""
def get_category_passwords(category_id):
    db = connect()
    if db is not None:
        response = execute_query(db, f"SELECT domain, account_name, url, password from passwords "
                                     f"WHERE category_id = {category_id}")
        db.close()
        return response
    else:
        print("Could not access the database while getting category passwords")

    return -1


"""
@param: category_id: password category id
@param: color: hex color string
@return: 1 for successful update
         -1 for database error

Change a password category's color.
"""
def change_category_color(category_id, color):
    db = connect()
    if db is not None:
        execute_update(db, f"UPDATE categories SET color = '{color}' WHERE category_id = {category_id};")
        return 1
    else:
        print("Could not access the database while changing category color")

    return -1


"""
@param: category_id: password category's id
@return: category name,
         -1 for database error

Get name of password category.
"""
def get_category_name(category_id):
    db = connect()
    if db is not None:
        response = execute_query(db, f"SELECT category_name FROM categories WHERE category_id = {category_id};")
        return response[0][0]
    else:
        print("Could not access the database while getting category name")

    return -1


"""
@param: category_id: password category's id
@return: category color,
         -1 for database error

Get hex color for password category.
"""
def get_category_color(category_id):
    db = connect()
    if db is not None:
        response = execute_query(db, f"SELECT color FROM categories WHERE category_id = {category_id};")
        return response[0][0]
    else:
        print("Could not access the database while getting category color")

    return -1


def update_user_password(user_id, entry_id, domain, url, account_name, category, password):
    db = connect()
    if db is not None:
        query_response = execute_query(db, "SELECT key FROM users WHERE user_id = %(user_id)s;",
                                       {"user_id": user_id})
        key = query_response[0][0]
        key = key.replace(r'\x', '')
        key = bytes.fromhex(key)
        aes_r = AESmode.AESmode(key)
        password = aes_r.encrypt(password)
        execute_update(db, f"UPDATE passwords SET domain = %(domain)s, url = %(url)s, account_name = %(account_name)s, "
                           f"category_id = (SELECT category_id FROM categories WHERE user_id = {user_id} "
                           f"AND category_name = %(category)s), password = %(password)s WHERE entry_id = {entry_id};",
                       {"domain": domain, "url": url, "account_name": account_name, "category": category,
                        "password": password})

        db.close()
        return get_user_passwords(user_id)
    else:
        print("Could not access the database while updating user passwords")

    return -1


def get_account_info(user_id):
    db = connect()
    if db is not None:
        query_response = execute_query(db, f"SELECT username, email, created_datetime FROM users "
                                           f"WHERE user_id = {user_id}")[0]
        return query_response
    else:
        print("Could not access the database while getting account info")

    return -1


def update_users_and_reencrypt_passwords(old_key, new_key):
    db = connect()

    db.execute("SELECT user_id, salt, master_password FROM users")
    user_records = db.fetchall()

    for user_id, encrypted_salt, encrypted_master_password in user_records:
        aes_decryptor = AESmode(old_key)
        decrypted_salt = aes_decryptor.decrypt(encrypted_salt)
        decrypted_master_password = aes_decryptor.decrypt(encrypted_master_password)

        aes_encryptor = AESmode(new_key)
        new_encrypted_salt = aes_encryptor.encrypt(decrypted_salt)
        new_encrypted_master_password = aes_encryptor.encrypt(decrypted_master_password)

        db.execute("UPDATE users SET salt = %s, master_password = %s WHERE user_id = %s",
                   (new_encrypted_salt, new_encrypted_master_password, user_id))

    db.execute("SELECT id, encrypted_password FROM passwords")
    password_records = db.fetchall()

    for record_id, encrypted_password in password_records:
        decrypted_password = aes_decryptor.decrypt(encrypted_password)
        new_encrypted_password = aes_encryptor.encrypt(decrypted_password)

        db.execute("UPDATE passwords SET password = %s WHERE id = %s", (new_encrypted_password, record_id))

    db.commit()
    db.close()