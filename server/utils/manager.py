# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import uuid
import hashlib


class Manager:
    def __init__(self):
        pass

    @staticmethod
    def get_random_char():
        num = str(random.randint(0, 9))
        # low_alpha = chr(random.randint(97, 122))
        up_alpha = chr(random.randint(65, 90))
        return str(random.choice([num, up_alpha]))

    @staticmethod
    def get_random_code(length=5):
        code = ''
        for i in range(length):
            code += Manager.get_random_char()
        return code

    @staticmethod
    def get_md5_str():
        uuid_val = uuid.uuid4()
        uuid_str = str(uuid_val).encode("utf-8")
        md5 = hashlib.md5()
        md5.update(uuid_str)
        return md5.hexdigest()
