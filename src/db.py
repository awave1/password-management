import sqlite3
import os.path


class Database:
    def __init__(self):
        self.db_path = "users.db"
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.__create_tables()

    def add_user(self, username, password):
        """
        Add a new user to the database
        
        Arguments:
            username {str} -- username
            password {str} -- hashed password
        """

        try:
            self.cursor.execute(
                "INSERT INTO users (username, password) VALUES (:username, :password)",
                {"username": username, "password": password},
            )
            self.connection.commit()

            return True
        except sqlite3.IntegrityError:
            return False

    def get_user(self, username):
        """
        Get a user with specified username from the database
        
        Arguments:
            username {str} -- username
        
        Returns:
            (str, str) -- user information, username and password hash
        """

        self.cursor.execute(
            "select username, password from users where username=?", (username,)
        )
        self.connection.commit()

        result = self.cursor.fetchone()
        return result

    def __create_tables(self):
        self.cursor.execute(
            """
            create table if not exists users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
            """
        )
        self.connection.commit()
