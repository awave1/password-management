import unittest
import os
from context import password_management
from password_management import Enroll, Database, constants


class EnrollTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_name = "users.test.db"

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.db_name)
        return super().tearDownClass()

    def test_should_create_a_new_user(self):
        """TODO
        """

        username = "john doe"
        password = "s3cur3"

        with Database(self.db_name) as db:
            enroller = Enroll(db)
            with self.assertRaises(SystemExit) as sys_exit:
                enroller.enroll(username, password)

            self.assertEqual(sys_exit.exception.code, 0)
            db.remove(username)

    def test_should_create_new_user_and_throw_when_enrolling_again(self):
        """TODO
        """

        username = "john doe"
        password = "s3cur3"

        with Database(self.db_name) as db:
            enroller = Enroll(db)
            with self.assertRaises(SystemExit) as sys_exit_succ:
                enroller.enroll(username, password)
                self.assertEqual(sys_exit_succ.exception.code, constants.STATUS_OK)

            with self.assertRaises(SystemExit) as sys_exit_fail:
                enroller.enroll(username, password)
                self.assertEqual(sys_exit_fail.exception.code, constants.STATUS_ERR)

            db.remove(username)

    def test_should_reject_number_password(self):
        username = "john doe"
        password = "123456"

        with Database(self.db_name) as db:
            enroller = Enroll(db)
            with self.assertRaises(SystemExit) as sys_exit:
                enroller.enroll(username, password)
                self.assertEquals(sys_exit.exception.code, constants.STATUS_ERR)

    def test_should_reject_dictionary_password(self):
        username = "batka"
        password = "byelorussia"

        with Database(self.db_name) as db:
            enroller = Enroll(db)
            with self.assertRaises(SystemExit) as sys_exit:
                enroller.enroll(username, password)
                self.assertEquals(sys_exit.exception.code, constants.STATUS_ERR)

    def test_should_reject_dictionary_password_followed_by_num(self):
        username = "batka"
        password = "byelorussia1"

        with Database(self.db_name) as db:
            enroller = Enroll(db)
            with self.assertRaises(SystemExit) as sys_exit:
                enroller.enroll(username, password)
                self.assertEquals(sys_exit.exception.code, constants.STATUS_ERR)

    def test_should_reject_dictionary_password_preceded_by_num(self):
        username = "batka"
        password = "1byelorussia"

        with Database(self.db_name) as db:
            enroller = Enroll(db)
            with self.assertRaises(SystemExit) as sys_exit:
                enroller.enroll(username, password)
                self.assertEquals(sys_exit.exception.code, constants.STATUS_ERR)

    def test_should_reject_dictionary_password_surrounded_by_nums(self):
        username = "batka"
        password = "1byelorussia234"

        with Database(self.db_name) as db:
            enroller = Enroll(db)
            with self.assertRaises(SystemExit) as sys_exit:
                enroller.enroll(username, password)
                self.assertEquals(sys_exit.exception.code, constants.STATUS_ERR)


if __name__ == "__main__":
    unittest.main()
