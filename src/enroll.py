from argon_hasher import ArgonHasher
from db import Database
import sys
import argparse
import re


def is_valid_password(password):
    """
    Check if given password is valid. A valid password cannot contain the following:

    - can't contain only numbers
    - can't contain words form the given dictionary, pre- or post- fixed by a number
    
    Arguments:
        password {str} -- password string
    
    Returns:
        [bool] -- true, if password is valid, false otherwise
    """

    password = password.lower()

    # check if password contains only numbers
    if password.isdigit():
        return False

    with open("data/words") as words:
        # remove all numbers from the password
        password = "".join(list(filter(lambda c: c.isalpha(), password)))

        # read the dictionary words from the file and keep any matches with specified password
        dictionary_words = list(
            filter(
                lambda w: w == password,
                map(lambda w: w.lower(), words.read().split("\n")),
            )
        )

        # if dictionary_words contain any elements, return False
        if len(dictionary_words) != 0:
            return False

    return True


def enroll(username, password):
    db = Database()
    argon2 = ArgonHasher()

    def accept_state():
        print("accepted")
        sys.exit(0)

    def reject_state():
        print("rejected")
        sys.exit(-1)

    if not is_valid_password(password):
        reject_state()

    password_hash = argon2.hash(password)
    if db.add_user(username, password_hash):
        accept_state()
    else:
        reject_state()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("username", type=str, help="Username")
    parser.add_argument("password", type=str, help="Password")
    args = parser.parse_args()

    enroll(args.username, args.password)
