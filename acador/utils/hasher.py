#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 07/12/2022 16:03
# @Author  : Xiao
# @Email   : crbpfx@gmail.com
# @File    : hasher
# @Software: PyCharm

import hashlib


def hash_string(input_string: str) -> str:
    md5 = hashlib.md5(input_string.encode('utf-8'))
    return md5.hexdigest()


if __name__ == '__main__':
    print(hash_string('test'))
