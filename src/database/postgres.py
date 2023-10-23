"""
File: src/database/postgres.py

Author: Aaron Kersten, amk9398@rit.edu

Description: Includes useful utility functions for using our project's
    postgreSQL database hosted through AWS.
"""

import psycopg2
from src.database.config import config


"""
@return: a connection to a postgres database. returns None on error and prints error message

Establishes a connection to the password database.
"""
def connect():
    try:
        params = config()                                       # get configuration parameters
        conn = psycopg2.connect(**params)                       # establish database connection
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
def execute_query(conn, query, args=None):
    cursor = conn.cursor()                                      # create database cursor
    if args is None:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    results = cursor.fetchall()                                 # gather the results
    cursor.close()
    return results


"""
@param: conn: database connection
@param: query: plaintext SQL update
@return: None

Executes update on the given database connection and commits the result.
"""
def execute_update(conn, update, args=None):
    cursor = conn.cursor()                                      # create database cursor
    if args is None:
        cursor.execute(update)
    else:
        cursor.execute(update, args)
    conn.commit()                                               # commit the results to the database
    cursor.close()
