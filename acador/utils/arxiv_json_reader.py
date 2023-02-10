#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 10/02/2023 14:55
# @Author  : Xiao
# @File    : arxiv_json_reader.py
# @Software: PyCharm

import json
















if __name__ == '__main__':
    with open('../../docs/arxiv-metadata-oai-snapshot.json', 'r') as j:
        aj = j.readlines()
    for i in range(10):
        one_line_json = json.loads(aj[i])
        print(one_line_json['id'])
