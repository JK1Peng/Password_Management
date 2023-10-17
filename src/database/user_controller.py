from src.database.postgres import connect, execute_query, execute_update


""" 
@param: username: the user's username
@param: password: the user's master password
@return: user_id upon successful login. prints message and returns -1 upoin failed login.

Allows a user to authenticate themself with the database and establish a connection.
"""
def login(username, password):
    db = connect()
    if db is not None:
        master_password = execute_query(db, "SELECT master_password FROM users WHERE username = '" + username +"';")[0][0]
        if master_password == password:
            user_id = execute_query(db, "SELECT user_id FROM users WHERE username = '" + username + "';")[0][0]
            return user_id
    else:
        print("Could not login to the database while processing login request.")
    return -1