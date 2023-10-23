from src.database.postgres import connect, execute_query, execute_update
import datetime


""" 
@param: username: the user's username
@param: password: the user's master password
@return: user_id for successful login
         0 for incorrect username or password
         -1 for a database connection error
         -2 for incorrect login limit exceeded

Allows a user to authenticate themself with the database and establish a connection.
"""
def login(username, password):
    # get database connection
    db = connect()
    if db is not None:
        # get master password for the current user
        master_password = execute_query(db, "SELECT master_password FROM users WHERE username = %(username)s;",
                                        {"username": username})

        # check that a password was returned
        if (len(master_password)) == 1:

            # get number of failed logins for this username
            num_failed_logins = execute_query(db, f"SELECT login_counter FROM users WHERE username = %(username)s;",
                                              {"username": username})[0][0]
            print(num_failed_logins)

            # if number of failed logins exceeds 5, return error code -2
            if num_failed_logins >= 5:
                db.close()
                return -2

            # if the passwords match, return the user id and close the connection
            if master_password[0][0] == password:
                user_id = execute_query(db, f"SELECT user_id FROM users WHERE username = %(username)s;",
                                        {"username": username})[0][0]

                # update user's last accessed date
                ct = datetime.datetime.now()
                execute_update(db, f"UPDATE users SET last_accessed_datetime = '{ct}' WHERE user_id = {user_id};")

                # set user's failed login number to 0
                execute_update(db, f"UPDATE users SET login_counter = 0 WHERE user_id = {user_id};")

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
def sign_up(username, password, email):
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

        # add new user to the users table in the database
        execute_update(db, f"INSERT INTO users (username, master_password, email, created_datetime, "
                           f"last_accessed_datetime) "
                           f"VALUES (%(username)s, %(master_password)s, %(email)s, '{ct}', '{ct}');",
                       {"username": username, "master_password": password, "email": email})

        # close connection and login to retrieve and return user_id
        db.close()
        return login(username, password)
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
    if db is not None:

        # if no query is given, grab the entire password repo
        if query == "":
            passwords = execute_query(db, f"SELECT domain, account_name, url, password FROM passwords "
                                          f"WHERE user_id = {user_id};")

        # otherwise, only grab entries with a domain, account name, or url like '...<query>...'
        else:

            # make sure that query does not contain quotations
            if "\'" in query or "\"" in query:
                return 0

            passwords = execute_query(db, f"SELECT domain, account_name, url, password FROM passwords p "
                                          f"WHERE user_id = {user_id} AND (LOWER(domain) LIKE '%{query}%' OR "
                                          f"LOWER(account_name) LIKE '%{query}%' OR LOWER(url) LIKE '%{query}%');")

        # close connection and return passwords
        db.close()
        return passwords
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
def add_password(user_id, domain, password, account_name="", url=""):
    # get database connection
    db = connect()
    if db is not None:
        # get count of user's with matching domain and account names
        matching_pswrd = execute_query(db, f"SELECT COUNT(*) FROM passwords WHERE domain = %(domain)s AND "
                                           f"account_name = %(account_name)s;",
                                           {"domain": domain, "account_name": account_name})[0][0]

        # if there is an existing password with matching domain and account name, return 0
        if matching_pswrd > 0:
            db.close()
            return 0

        # get current timestamp
        ct = datetime.datetime.now()

        # add new password to user's password repo
        execute_update(db, f"INSERT INTO passwords (user_id, domain, account_name, url, password, created_datetime, "
                           f"last_modified_datetime) VALUES ({user_id}, %(domain)s, %(account_name)s, %(url)s,"
                           f"%(password)s, '{ct}', '{ct}');",
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
