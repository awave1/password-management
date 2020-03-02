from password_management import ArgonHasher, Database
import sys
import argparse


class Enroll:
    def __init__(self, db):
        self.db = db
        self.argon2 = ArgonHasher()

    def enroll(self, username, password):
        if not self.is_valid_password(password):
            return self.__reject_state()

        password_hash = self.argon2.hash(password)
        if self.db.add_user(username, password_hash):
            return self.__accept_state()
        else:
            return self.__reject_state()

    def __accept_state(self):
        print("accepted.")
        sys.exit(0)

    def __reject_state(self):
        print("rejected.")
        sys.exit(-1)

    @staticmethod
    def is_valid_password(password):
        """Check if given password is valid. A valid password cannot contain the following:

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("username", type=str, help="Username")
    parser.add_argument("password", type=str, help="Password")
    args = parser.parse_args()

    with Database() as db:
        enroller = Enroll(db)
        enroller.enroll(args.username, args.password)
