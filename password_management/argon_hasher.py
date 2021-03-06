#!/usr/bin/env python3

from argon2.low_level import verify_secret, hash_secret, Type
import argon2.exceptions
import os

# argon2 defaults
DEFAULT_SALT_LEN = 16
DEFAULT_HASH_LEN = 16
DEFAULT_TIME_COST = 2
DEFAULT_MEM_COST = 100000
DEFAULT_PARALLELISM = 8
DEFAULT_STRING_ENCODING = "utf-8"
DEFAULT_HASH_ENCODING = "ascii"


class ArgonHasher:
    def __init__(
        self,
        salt_len=DEFAULT_SALT_LEN,
        hash_len=DEFAULT_HASH_LEN,
        time_cost=DEFAULT_TIME_COST,
        memory_cost=DEFAULT_MEM_COST,
        parallelism=DEFAULT_PARALLELISM,
        string_encoding=DEFAULT_STRING_ENCODING,
        hash_encoding=DEFAULT_HASH_ENCODING,
    ):
        self.salt_len = salt_len

        # the length of output hash
        self.hash_len = hash_len

        # argon2 configuration
        self.time_cost = time_cost
        self.memory_cost = memory_cost
        self.parallelism = parallelism

        # encoding information
        self.string_encoding = string_encoding
        self.hash_encoding = hash_encoding

    def hash(self, string):
        """Hash a provided string using argon2id
        
        Arguments:
            string {str} -- string you want to hash
        
        Returns:
            str -- argon2 hash of the given string
        """

        encoded_str = string.encode(self.string_encoding)

        # random salt, 16 bytes long
        salt = os.urandom(self.salt_len)

        # hash the given string using argon2id algorithm
        result = hash_secret(
            secret=encoded_str,
            salt=salt,
            time_cost=self.time_cost,
            memory_cost=self.memory_cost,
            parallelism=self.parallelism,
            hash_len=self.hash_len,
            type=Type.ID,
        )

        return result.decode(self.hash_encoding)

    def verify(self, hash, actual_string):
        """Verify hash against the plaintext string
        
        Arguments:
            hash {str} -- hash string
            actual_string {str} -- string you want to check
        
        Returns:
            bool -- true, if given hash corresponds to the string
        """

        try:
            return verify_secret(
                hash.encode(self.hash_encoding),
                actual_string.encode(self.string_encoding),
                Type.ID,
            )
        except argon2.exceptions.VerifyMismatchError:
            # if mismatch error occured, return False
            return False
