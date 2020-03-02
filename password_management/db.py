import sqlite3
import os.path


class Database:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.__create_tables()

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()

    def __del__(self):
        try:
            self.cursor.close()
            self.connection.close()
        except sqlite3.ProgrammingError:
            pass

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

    def remove(self, username):
        self.cursor.execute("delete from users where username=?", (username,))
        self.connection.commit()
        rows = self.cursor.rowcount

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
