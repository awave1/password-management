import unittest
import os
from unittest.mock import patch
from io import StringIO
from context import password_management
from password_management import Authenticate, Enroll, Database, constants


class AuthenticateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_name = "users.test.db"

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.db_name)
        return super().tearDownClass()

    def test_should_successfully_enroll_and_authenticate_new_user(self):
        """Should successfully enroll a user and authenticates it
        """

        with patch("sys.stdout", new=StringIO()) as out:
            username = "john doe"
            password = "s3cur3"

            with Database(self.db_name) as db:
                enroller = Enroll(db)
                authenticator = Authenticate(db)

                with self.assertRaises(SystemExit) as sys_exit:
                    enroller.enroll(username, password)
                    self.assertEquals(sys_exit.exception.code, constants.STATUS_OK)
                    self.assertEquals(out.getvalue().strip(), constants.ENROLL_OK)

                with self.assertRaises(SystemExit) as sys_exit:
                    authenticator.authenticate(username, password)
                    self.assertEquals(sys_exit.exception.code, constants.STATUS_OK)
                    self.assertEquals(out.getvalue().strip(), constants.AUTH_OK)

    def test_should_fail_to_authenticate_existing_user_with_wrong_password(self):
        """Should fail to authenticate existing user with wring password
        """

        with patch("sys.stdout", new=StringIO()) as out:
            username = "john doe"
            password = "wh@tisthis"

            with Database(self.db_name) as db:
                authenticator = Authenticate(db)

                with self.assertRaises(SystemExit) as sys_exit:
                    authenticator.authenticate(username, password)
                    self.assertEquals(sys_exit.exception.code, constants.STATUS_ERR)
                    self.assertEquals(out.getvalue().strip(), constants.AUTH_ERR)

    def test_should_successfully_authenticate_existsing_user(self):
        """Should successfully authenticate existsing user
        """

        with patch("sys.stdout", new=StringIO()) as out:
            username = "john doe"
            password = "s3cur3"

            with Database(self.db_name) as db:
                authenticator = Authenticate(db)

                with self.assertRaises(SystemExit) as sys_exit:
                    authenticator.authenticate(username, password)
                    self.assertEquals(sys_exit.exception.code, constants.STATUS_OK)
                    self.assertEquals(out.getvalue().strip(), constants.AUTH_OK)

    def test_should_fail_to_authenticate_unknown_user(self):
        """Should fail to authenticate unknown user
        """

        with patch("sys.stdout", new=StringIO()) as out:
            username = "john doe1"
            password = "s3cur3"

            with Database(self.db_name) as db:
                authenticator = Authenticate(db)

                with self.assertRaises(SystemExit) as sys_exit:
                    authenticator.authenticate(username, password)
                    self.assertEquals(sys_exit.exception.code, constants.STATUS_ERR)
                    self.assertEquals(out.getvalue().strip(), constants.AUTH_ERR)


if __name__ == "__main__":
    unittest.main()
