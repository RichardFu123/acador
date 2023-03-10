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
import time
from tqdm import tqdm
from itertools import repeat
import multiprocessing as mp
from arxiv_json_reader import get_arxiv_db


def download(_url, _target, _id, _folder):
    docs_path = os.path.join(sys.path[1], _folder)
    try:
        r = requests.get(_url, allow_redirects=True)
        file_path = os.path.join(docs_path, _id.split('/')[-1])
        if _target == 'pdf':
            open(f'{file_path}.pdf', 'wb').write(r.content)
        else:
            open(f'{file_path}.tar.gz', 'wb').write(r.content)
        r.close()
        time.sleep(2)
    except ConnectionResetError:
        print(_id,': reset by peer')
        time.sleep(60)


def download_acm_paper(target='pdf', folder='docs/'):
    docs_path = os.path.join(sys.path[1], folder)

    only_files = ['.'.join(f.split('.')[:int(-1*len(target.split('.')))]) for f in os.listdir(docs_path) if os.path.isfile(os.path.join(docs_path, f))]

    conn = get_arxiv_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    num_cpu = mp.cpu_count() - 3

    acms = cur.execute('''SELECT * FROM cs WHERE doi IS NOT "None"''').fetchall()
    # acms = cur.execute('''SELECT * FROM cs WHERE journal_ref LIKE "%ACM%"''').fetchall()
    list_accumulator = []
    for item in acms:
        list_accumulator.append({k: item[k] for k in item.keys()})
    download_urls = []
    download_target = []
    download_id = []
    for i in tqdm(list_accumulator):
        try:
            _id = ''
            if i['id'].split('/')[-1] not in only_files:
                _id = i['id']
            else:
                continue
            if target == 'pdf':
                url = f'https://export.arxiv.org/pdf/{_id}'
            else:
                url = f'https://export.arxiv.org/e-print/{_id}'
            download_urls.append(url)
            download_target.append(target)
            download_id.append(_id)
        except:
            continue

    with mp.Pool(num_cpu) as p:
        list(tqdm(p.starmap(download, zip(download_urls,
                                       download_target,
                                       download_id,
                                       repeat(folder))), total=len(download_target)))




if __name__ == '__main__':
    download_acm_paper(target='pdf', folder='docs/')
