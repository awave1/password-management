from password_management import ArgonHasher, Database
import sys
import sqlite3
import argparse


class Authenticate:
    def __init__(self):
        self.db = Database()
        self.argon2 = ArgonHasher()

    def authenticate(self, username, password):

        (user, pwd_hash) = self.db.get_user(username)

        if user is None or pwd_hash is None:
            self.__deny_state()

        if not argon2.verify(pwd_hash, password):
            self.__deny_state()

        self.__accept_state()

    def __accept_state(self):
        print("access granted.")
        sys.exit(0)

    def __deny_state(self):
        print("access denied.")
        sys.exit(-1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("username", type=str, help="Username")
    parser.add_argument("password", type=str, help="Password")
    args = parser.parse_args()

    Authenticate().authenticate(args.username, args.password)
