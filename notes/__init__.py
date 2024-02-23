import sqlite3
from . import constants
import logging
from .note_structure import Note
from .sql_result import SqlResult
import datetime


# For testing only!
def print_all() -> None:
    rows: list = __get_connection().execute(f"SELECT * FROM {constants.NOTES_TABLE_NAME};")

    for row in rows:
        print(row)


def __get_connection() -> sqlite3.Connection:
    """
    Initialises a connection to a SQLite database, where the notes database table is located.
    (The notes database table is automatically created, if it is not present in the SQLite database).
    :return: sqlite3.Connection
    """

    try:
        # Establish a connection to the SQL database.
        connection: sqlite3.Connection = sqlite3.Connection(constants.DATABASE_NAME)

        # Ensure the notes database table is initialised.
        connection.execute(f'CREATE TABLE IF NOT EXISTS {constants.NOTES_TABLE_NAME} (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, title TEXT, description TEXT, date TEXT);')

        # Return the SQLite database connection.
        return connection

    except sqlite3.Error as error:

        # Log the error for future record.
        logging.error(f"Error establishing a SQL database connection: {error}")

        # Raise the SQLite error.
        raise error


def __get_date_now() -> str:
    return datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")


def add_note(note: Note) -> bool:
    try:
        # Initialise an SQLite database connection.
        connection: sqlite3.Connection = __get_connection()

        # Separate the query and values to prevent SQL injection.
        query: str = f"INSERT INTO {constants.NOTES_TABLE_NAME} (username, title, description, date) VALUES(?,?,?,?);"
        connection.execute(query, (note.username, note.title, note.description, __get_date_now(),))

        # Save and close the database.
        connection.commit()
        connection.close()

        return True

    except sqlite3.Error as error:

        # Log the error for future record.
        logging.error(f"Error establishing a SQL database connection: {error}")

        # Raise the SQLite error.
        raise error


def remove_note(identification: int) -> bool:
    try:
        # Initialise an SQLite database connection.
        connection: sqlite3.Connection = __get_connection()

        # Separate the query and values to prevent SQL injection.
        query: str = f"DELETE FROM {constants.NOTES_TABLE_NAME} WHERE id = ?;"
        connection.execute(query, (identification,))

        # Save and close the database.
        connection.commit()
        connection.close()

        return True

    except sqlite3.Error as error:

        # Log the error for future record.
        logging.error(f"Error establishing a SQL database connection: {error}")

        # Raise the SQLite error.
        raise error


def update_note(identification: int, title: str, description: str) -> None:
    try:
        # Initialise an SQLite database connection.
        connection: sqlite3.Connection = __get_connection()

        # Separate the query and values to prevent SQL injection.
        query: str = f"UPDATE {constants.NOTES_TABLE_NAME} SET title = ?, description = ?, date = ? WHERE id = ?;"
        connection.execute(query, (title, description, __get_date_now(), identification,))

        # Save and close the database.
        connection.commit()
        connection.close()

        return True

    except sqlite3.Error as error:

        # Log the error for future record.
        logging.error(f"Error establishing a SQL database connection: {error}")

        # Raise the SQLite error.
        raise error
