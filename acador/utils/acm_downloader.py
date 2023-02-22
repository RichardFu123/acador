#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/02/2023 15:04
# @Author  : Xiao
# @File    : acm_downloader.py
# @Software: PyCharm

import os
import sys
import sqlite3
import requests
from tqdm import tqdm
from arxiv_json_reader import get_arxiv_db

def download_acm_paper():
    docs_path = os.path.join(sys.path[1], 'docs/')
    only_files = ['.'.join(f.split('.')[:-1]) for f in os.listdir(docs_path) if os.path.isfile(os.path.join(docs_path, f))]


    conn = get_arxiv_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    acms = cur.execute('''SELECT * FROM cs WHERE doi IS NOT "None"''').fetchall()
    list_accumulator = []
    for item in acms:
        list_accumulator.append({k: item[k] for k in item.keys()})
    for i in tqdm(list_accumulator):
        try:
            _id = ''
            if i['id'].split('/')[-1] not in only_files:
                _id = i['id']
            else:
                continue
            url = f'https://arxiv.org/pdf/{_id}'
            r = requests.get(url, allow_redirects=True)
            file_path = os.path.join(docs_path, i['id'].split('/')[-1])
            open(f'{file_path}.pdf', 'wb').write(r.content)
            r.close()
        except:
            continue



if __name__ == '__main__':
    download_acm_paper()