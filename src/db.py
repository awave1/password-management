import sqlite3
import os.path


class Database:
    def __init__(self):
        self.db_path = "users.db"
        self.connection = sqlite3.connect(self.db_path)
        self.__create_tables()

    def add_user(self, username, password):
        """Add a new user to the database
        
        Arguments:
            username {str} -- username
            password {str} -- hashed password
        """
        try:
            with self.connection:
                self.connection.cursor().execute(
                    "INSERT INTO users (username, password) VALUES (:username, :password)",
                    {"username": username, "password": password},
                )
                return True
        except sqlite3.IntegrityError:
            return False

    def __create_tables(self):
        """Create 'users' table, if it doesn't exist already
        """
        self.connection.cursor().execute(
            """
            create table if not exists users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
            """
        )
