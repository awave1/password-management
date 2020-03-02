from password_management import ArgonHasher, Database, constants
import sys
import sqlite3
import argparse


class Authenticate:
    def __init__(self, db):
        self.db = db
        self.argon2 = ArgonHasher()

    def authenticate(self, username, password):

        (user, pwd_hash) = self.db.get_user(username)

        if user is None or pwd_hash is None:
            self.__deny_state()

        if not self.argon2.verify(pwd_hash, password):
            self.__deny_state()

        self.__accept_state()

    def __accept_state(self):
        print(constants.AUTH_ERR)
        sys.exit(constants.STATUS_OK)

    def __deny_state(self):
        print(constants.AUTH_OK)
        sys.exit(constants.STATUS_ERR)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("username", type=str, help="Username")
    parser.add_argument("password", type=str, help="Password")
    args = parser.parse_args()

    with Database() as db:
        Authenticate(db).authenticate(args.username, args.password)
