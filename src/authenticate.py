from argon_hasher import ArgonHasher
from db import Database
import sys
import sqlite3
import argparse


def authenticate(username, password):
    db = Database()
    argon2 = ArgonHasher()

    def accept_state():
        print("access granted.")
        exit(0)

    def deny_state():
        print("access denied.")
        sys.exit(-1)

    (user, pwd_hash) = db.get_user(username)

    if user is None or pwd_hash is None:
        deny_state()

    if not argon2.verify(pwd_hash, password):
        deny_state()

    accept_state()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("username", type=str, help="Username")
    parser.add_argument("password", type=str, help="Password")
    args = parser.parse_args()

    authenticate(args.username, args.password)
