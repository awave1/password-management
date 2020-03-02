import unittest
import os
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

    def test_should_successfully_authenticate_existing_user(self):
        username = "john doe"
        password = "s3cur3"

        with Database(self.db_name) as db:
            enroller = Enroll(db)
            authenticator = Authenticate(db)

            with self.assertRaises(SystemExit) as sys_exit:
                enroller.enroll(username, password)
                self.assertEquals(sys_exit.exception.code, constants.STATUS_OK)

            with self.assertRaises(SystemExit) as sys_exit:
                authenticator.authenticate(username, password)
                self.assertEquals(sys_exit.exception.code, constants.STATUS_OK)


if __name__ == "__main__":
    unittest.main()
