#!/usr/bin/env python3

import unittest
import os
import sys
from unittest.mock import patch
from io import StringIO
import password_management
import password_management.constants as constants
from password_management.enroll import Enroll
from password_management.db import Database


class EnrollTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_name = "users.test.db"

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.db_name)
        return super().tearDownClass()

    def test_should_create_a_new_user(self):
        """Should successfully enroll a new user with secure password
        """

        with patch("sys.stdout", new=StringIO()) as out:
            username = "john doe"
            password = "s3cur3"

            with Database(self.db_name) as db:
                enroller = Enroll(db)
                with self.assertRaises(SystemExit) as sys_exit:
                    enroller.enroll(username, password)

                self.assertEqual(sys_exit.exception.code, constants.STATUS_OK)
                self.assertEqual(out.getvalue().strip(), constants.ENROLL_OK)
                db.remove(username)

    def test_should_create_user_with_same_password_but_different_hash(self):
        """Should successfully enroll a new user with the same password and their hashes should not equal
        """

        with patch("sys.stdout", new=StringIO()) as out:
            username1 = "john doe1"
            username2 = "john doe2"
            password = "s3cur3"

            with Database(self.db_name) as db:
                enroller = Enroll(db)
                with self.assertRaises(SystemExit) as sys_exit:
                    enroller.enroll(username1, password)
                    self.assertEqual(sys_exit.exception.code, constants.STATUS_OK)
                    self.assertEqual(out.getvalue().strip(), constants.ENROLL_OK)

                with self.assertRaises(SystemExit) as sys_exit:
                    enroller.enroll(username2, password)
                    self.assertEqual(sys_exit.exception.code, constants.STATUS_OK)
                    self.assertEqual(out.getvalue().strip(), constants.ENROLL_OK)

                user1 = db.get_user(username1)
                user2 = db.get_user(username2)

                self.assertNotEqual(user1[0], user2[0])
                self.assertNotEqual(user1[1], user2[1])

                db.remove(username1)
                db.remove(username2)

    def test_should_create_new_user_and_throw_when_enrolling_again(self):
        """Should enroll a new user and then should fail to enroll it again
        """

        with patch("sys.stdout", new=StringIO()) as out:
            username = "john doe"
            password = "s3cur3"

            with Database(self.db_name) as db:
                enroller = Enroll(db)
                with self.assertRaises(SystemExit) as sys_exit_succ:
                    enroller.enroll(username, password)
                    self.assertEqual(sys_exit_succ.exception.code, constants.STATUS_OK)
                    self.assertEqual(out.getvalue().strip(), constants.ENROLL_OK)

                with self.assertRaises(SystemExit) as sys_exit_fail:
                    enroller.enroll(username, password)
                    self.assertEqual(sys_exit_fail.exception.code, constants.STATUS_ERR)
                    self.assertEqual(out.getvalue().strip(), constants.ENROLL_ERR)

                db.remove(username)

    def test_should_reject_number_password(self):
        """Should fail to enroll a user with a weak (numbers only) password
        """

        with patch("sys.stdout", new=StringIO()) as out:
            username = "john doe"
            password = "123456"

            with Database(self.db_name) as db:
                enroller = Enroll(db)
                with self.assertRaises(SystemExit) as sys_exit:
                    enroller.enroll(username, password)
                    self.assertEqual(sys_exit.exception.code, constants.STATUS_ERR)
                    self.assertEqual(out.getvalue().strip(), constants.ENROLL_ERR)

    def test_should_reject_dictionary_password(self):
        """Should fail to enroll a user with a weak password - dictionary word
        """

        with patch("sys.stdout", new=StringIO()) as out:
            username = "batka"
            password = "byelorussia"

            with Database(self.db_name) as db:
                enroller = Enroll(db)
                with self.assertRaises(SystemExit) as sys_exit:
                    enroller.enroll(username, password)
                    self.assertEqual(sys_exit.exception.code, constants.STATUS_ERR)
                    self.assertEqual(out.getvalue().strip(), constants.ENROLL_ERR)

    def test_should_reject_dictionary_password_followed_by_num(self):
        """Should fail to enroll a user with a weak password - dictionary word followed by a number
        """

        with patch("sys.stdout", new=StringIO()) as out:
            username = "batka"
            password = "byelorussia1"

            with Database(self.db_name) as db:
                enroller = Enroll(db)
                with self.assertRaises(SystemExit) as sys_exit:
                    enroller.enroll(username, password)
                    self.assertEqual(sys_exit.exception.code, constants.STATUS_ERR)
                    self.assertEqual(out.getvalue().strip(), constants.ENROLL_ERR)

    def test_should_reject_dictionary_password_preceded_by_num(self):
        """Should fail to enroll a user with a weak password - dictionary word preceded by a number
        """

        with patch("sys.stdout", new=StringIO()) as out:
            username = "batka"
            password = "1byelorussia"

            with Database(self.db_name) as db:
                enroller = Enroll(db)
                with self.assertRaises(SystemExit) as sys_exit:
                    enroller.enroll(username, password)
                    self.assertEqual(sys_exit.exception.code, constants.STATUS_ERR)
                    self.assertEqual(out.getvalue().strip(), constants.ENROLL_ERR)

    def test_should_reject_dictionary_password_surrounded_by_nums(self):
        """Should fail to enroll a user with a weak password - dictionary word surrounded by numbers
        """

        with patch("sys.stdout", new=StringIO()) as out:
            username = "batka"
            password = "1byelorussia234"

            with Database(self.db_name) as db:
                enroller = Enroll(db)
                with self.assertRaises(SystemExit) as sys_exit:
                    enroller.enroll(username, password)
                    self.assertEqual(sys_exit.exception.code, constants.STATUS_ERR)
                    self.assertEqual(out.getvalue().strip(), constants.ENROLL_ERR)


if __name__ == "__main__":
    unittest.main()
