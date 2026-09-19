import sqlite3


DATABASE = "ecommerce.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def get_schema():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
    """)

    tables = cursor.fetchall()

    schema = {}

    for (table_name,) in tables:

        cursor.execute(f"PRAGMA table_info('{table_name}')")

        columns = cursor.fetchall()

        schema[table_name] = [column[1] for column in columns]

    connection.close()

    return schema


def execute_query(sql):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(sql)

    rows = cursor.fetchall()

    columns = [column[0] for column in cursor.description]

    connection.close()

    return [dict(zip(columns, row)) for row in rows]