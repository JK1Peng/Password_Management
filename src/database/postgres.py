import psycopg2
from src.database.config import config


def connect():
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None


def execute_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results


def execute_update(conn, update):
    cursor = conn.cursor()
    cursor.execute(update)
    conn.commit()
    cursor.close()


if __name__ == '__main__':
    db = connect()
    if db is not None:
        print("Connected.")
        results = execute_query(db, "SELECT * FROM test_table;")
        print(results)
        db.close()
    else:
        print("Could not connect to the database.")