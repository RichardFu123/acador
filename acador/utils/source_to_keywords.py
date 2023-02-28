#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 27/02/2023 16:58
# @Author  : Xiao
# @File    : source_to_keywords.py
# @Software: PyCharm

import os
import sys
import re
import tarfile
from tqdm import tqdm
from pdf_to_keywords import is_keywords_list



def tidy_kw(kw:str):
    t = kw.strip()
    t = t.strip('.')
    return t.strip()

def tex_to_kws(path):
    with open(path, 'r') as tex:
        lines = tex.readlines()
        tex.close()
    string = ''.join(lines)
    s_kws = re.search(r'\\keywords\{(.*?)\}', string).group(1)
    if len(s_kws.split(',')) > 1:
        kwl = s_kws.split(',')
    else:
        kwl = s_kws.split(';')
    return [tidy_kw(k) for k in kwl]


def uncompress_tar_gzs(folder='source/'):
    docs_path = os.path.join(sys.path[1], folder)
    only_files = [f for f in os.listdir(docs_path) if
                  (os.path.isfile(os.path.join(docs_path, f)) and f.endswith('.tar.gz'))]
    for tar in only_files:
        try:
            file = tarfile.open(os.path.join(docs_path, tar))
            file.extractall(f'{docs_path}{tar[:-7]}')
            file.close()
        except:
            continue

def source_to_kws(folder='source/'):
    uncompress_tar_gzs(folder)
    docs_path = os.path.join(sys.path[1], folder)
    only_folder = [f for f in os.listdir(docs_path) if os.path.isdir(os.path.join(docs_path, f))]
    kws_dict = {}
    for sub_folder in tqdm(only_folder):
        _id = sub_folder
        only_tex = [l for l in os.listdir(os.path.join(docs_path, sub_folder)) if
                      (os.path.isfile(os.path.join(os.path.join(docs_path, sub_folder), l)) and l.endswith('.tex'))]
        for tex in only_tex:
            try:
                kws = tex_to_kws(os.path.join(docs_path, sub_folder, tex))
            except:
                kws = []
            if is_keywords_list(kws):
                kws_dict[_id] = kws
    return kws_dict


if __name__ == '__main__':
    print(source_to_kws())