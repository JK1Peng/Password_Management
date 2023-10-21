import psycopg2
from src.database.config import config


"""
@return: a connection to a postgres database. returns None on error and prints error message

Establishes a connection to the password database.
"""
def connect():
    conn = None

    try:
        #params = config()                                       # get configuration parameters
        conn = psycopg2.connect(host="password-manager.c9sdfgddghu2.us-east-2.rds.amazonaws.com",
                                port=5432,
                                database="postgres",
                                user="postgres",
                                password="HJuebx;8,ok")                       # establish database connection
        return conn
    except (Exception, psycopg2.DatabaseError) as error:        # catch potential errors
        print(error)
        return None


"""
@param: conn: database connection
@param: query: plaintext SQL query
@return: list of tuples containing the results of the query

Executes query on database connection and returns query results.
"""
def execute_query(conn, query):
    cursor = conn.cursor()                                      # create database cursor
    cursor.execute(query)                                       # user cursor to execute query
    results = cursor.fetchall()                                 # gather the results
    cursor.close()
    return results


"""
@param: conn: database connection
@param: query: plaintext SQL update
@return: None

Executes update on the given database connection and commits the result.
"""
def execute_update(conn, update):
    cursor = conn.cursor()                                      # create database cursor
    cursor.execute(update)                                      # user cursor to execute update
    conn.commit()                                               # commit the results to the database
    cursor.close()