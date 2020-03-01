import sqlite3
import os.path


class Database:
    def __init__(self):
        self.db_path = "users.db"
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

        self.__create_tables()

    def add_user(self, username, password):
        """Add a new user to the database
        
        Arguments:
            username {str} -- username
            password {str} -- hashed password
        """
        self.__insert(username, password)

    def user_exists(self, username):
        """Check if a user with  given username exists
        
        Arguments:
            username {str} -- username
        
        Returns:
            bool -- true, if user exists, false otherwise
        """
        user_rows = self.__select(username)
        return len(user_rows.fetchall()) == 1

    def __create_tables(self):
        """Create 'users' table, if it doesn't exist already
        """
        self.cursor.execute(
            "SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'users'"
        )

        table_exists = self.cursor.fetchone()[0] == 1

        if not table_exists:
            self.cursor.execute(
                """
                CREATE TABLE users(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL UNIQUE,
                  password TEXT NOT NULL
                )
                """
            )

    def __insert(self, username, password):
        """Insert user credentials into 'users' table
        
        Arguments:
            username {str} -- username
            password {str} -- hashed password
        
        Returns:
            list -- row added
        """
        return self.cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
        )

    def __select(self, username):
        return self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
