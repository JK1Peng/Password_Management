from src.database.postgres import connect, execute_query, execute_update
import datetime

""" 
@param: username: the user's username
@param: password: the user's master password
@return: user_id upon successful login. prints message and returns -1 upoin failed login.

Allows a user to authenticate themself with the database and establish a connection.
"""
def login(username, password):
    db = connect()
    if db is not None:
        master_password = execute_query(db, "SELECT master_password FROM users WHERE username = '" + username + "';")
        if (len(master_password)) >= 1:
            if master_password[0][0] == password:
                user_id = execute_query(db, "SELECT user_id FROM users WHERE username = '" + username + "';")[0][0]
                db.close()
                return user_id
    else:
        print("Could not access to the database while processing login request.")
    return -1


def sign_up(username, password, email):
    db = connect()
    if db is not None:
        test_users1 = execute_query(db, f"SELECT * FROM users WHERE username = '{username}';")
        test_user2 = execute_query(db, f"SELECT * FROM users WHERE email = '{email}';")

        if len(test_users1) > 0:
            print("Another account exists with this username")
            db.close()
            return 0

        if len(test_user2) > 0:
            print("Another account exists with this email")
            db.close()
            return 0

        ct = datetime.datetime.now()
        print(username, password, email, ct)
        print(
            f"INSERT INTO users (username, master_password, email, created_datetime, "
            f"last_accessed_datetime) "
            f"VALUES ('{username}', '{password}', '{email}', '{ct}', '{ct}');"
        )
        execute_update(db, f"INSERT INTO users (username, master_password, email, created_datetime, "
                           f"last_accessed_datetime) "
                           f"VALUES ('{username}', '{password}', '{email}', '{ct}', '{ct}');")
        db.close()
        return login(username, password)
    else:
        print("Could not access the database while processing sign up request.")
    return -1


def get_user_passwords(user_id, query=""):
    db = connect()
    if db is not None:
        if query == "":
            passwords = execute_query(db, f"SELECT domain, account_name, url, password FROM passwords "
                                          f"WHERE user_id = {user_id};")
        else:
            passwords = execute_query(db, f"SELECT domain, account_name, url, password FROM passwords "
                                          f"WHERE user_id = {user_id} AND (domain LIKE '%{query}%' OR "
                                          f"account_name LIKE '%{query}%' OR url LIKE '%{query}%');")
        db.close()
        return passwords
    else:
        print("Could not access the database while processing get-password request")
    return -1


def add_password(user_id, domain, password, account_name="", url=""):
    db = connect()
    if db is not None:
        print(
            f"SELECT * FROM passwords WHERE domain = '{domain}' AND "
            f"account_name = '{account_name}';"
        )
        passwords = execute_query(db, f"SELECT * FROM passwords WHERE domain = '{domain}' AND "
                                      f"account_name = '{account_name}';")
        if len(passwords) >= 1:
            db.close()
            return 0
        ct = datetime.datetime.now()
        print(
            f"INSERT INTO passwords (user_id, domain, account_name, url, created_datetime, "
            f"last_modified_datetime) VALUES ({user_id}, '{domain}', '{account_name}', '{url}',"
            f"'{password}', '{ct}', '{ct}');"
        )
        execute_update(db, f"INSERT INTO passwords (user_id, domain, account_name, url, password, created_datetime, "
                           f"last_modified_datetime) VALUES ({user_id}, '{domain}', '{account_name}', '{url}',"
                           f"'{password}', '{ct}', '{ct}');")
        db.close()
        return 1
    else:
        print("Could not access the database while adding a password")
    return -1


def remove_password(user_id, domain, account_name):
    db = connect()
    if db is not None:
        execute_update(db, f"DELETE FROM passwords WHERE user_id = {user_id} AND domain = '{domain}' AND "
                           f"account_name = '{account_name}';")
        db.close()
        return 1
    else:
        print("Could not access the database while removing a password")
    return -1
