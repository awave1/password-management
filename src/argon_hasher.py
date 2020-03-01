from argon2.low_level import verify_secret, hash_secret, Type
import os

DEFAULT_SALT_LEN = 16
DEFAULT_HASH_LEN = 16
DEFAULT_TIME_COST = 2
DEFAULT_MEM_COST = 1000000
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
        encoded_str = string.encode(self.string_encoding)

        # random salt, 16 bytes long
        salt = os.urandom(self.salt_len)

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
        return verify_secret(
            hash.encode(self.hash_encoding),
            actual_string.encode(self.string_encoding),
            Type.ID,
        )
