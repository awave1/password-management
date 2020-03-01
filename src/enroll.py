# /usr/bin/env python3

from argon2 import PasswordHasher
from db import Database
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("username", type=str, help="Username")
parser.add_argument("password", type=str, help="Password")
args = parser.parse_args()

db = Database()

ph = PasswordHasher()
username = args.username
password = ph.hash(args.password)

if db.add_user(username, password):
    print("accepted")
    sys.exit(0)
else:
    print("rejected")
    sys.exit(-1)
