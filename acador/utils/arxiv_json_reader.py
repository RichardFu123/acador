#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 10/02/2023 14:55
# @Author  : Xiao
# @File    : arxiv_json_reader.py
# @Software: PyCharm
import os
import sys
import json
import sqlite3
from tqdm import tqdm


def load_arxiv_to_db(path):
    # load arxiv json
    with open(path, 'r') as _jf:
        doc_lines = _jf.readlines()
    header = list(json.loads(doc_lines[0]).keys())
    header_clean = [i.replace('-', '_') for i in header]

    # database preparing
    db_path = os.path.join(sys.path[1], 'db', 'arxiv.db')
    print(db_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # create table in not exists
    create_text = '''CREATE TABLE IF NOT EXISTS Documents ('''
    header_pair_text = [i.strip()+' TEXT' for i in header_clean]
    create_text += ', '.join(header_pair_text)
    create_text += ',CONSTRAINT documents_pk PRIMARY KEY (id));'
    cur.execute(create_text)
    conn.commit()

    # insert all lines
    for line in tqdm(doc_lines):
        one_j = json.loads(line)
        row = []
        for k in header:
            row.append(one_j[k])
        _dummy = []
        for i in row:
            _dummy.append("\""+str(i).replace('"', '')+"\"")
        _dummy = ','.join(_dummy)
        _dummy = f'INSERT OR REPLACE INTO Documents VALUES ({_dummy})'
        conn.execute(_dummy)
    conn.commit()


def get_arxiv_db():
    db_path = os.path.join(sys.path[1], 'db', 'arxiv.db')
    conn = sqlite3.connect(db_path)
    return conn

if __name__ == '__main__':
    load_arxiv_to_db('../../docs/arxiv-metadata-oai-snapshot.json')
