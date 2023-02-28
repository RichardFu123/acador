#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19/02/2023 15:30
# @Author  : Xiao
# @File    : docs_kws_extractor.py
# @Software: PyCharm

import os
import sys
import pickle
from tqdm import tqdm
from pdf_to_keywords import pdf_to_keywords
from source_to_keywords import source_to_kws


def kws_extractor():
    path_to_docs = os.path.join(sys.path[1], 'docs/')
    path_to_source = os.path.join(sys.path[1], 'source/')
    path_to_temp = os.path.join(sys.path[1], 'temp/')

    pdf_to_kws = {}

    only_files = [f for f in os.listdir(path_to_docs) if
                  (os.path.isfile(os.path.join(path_to_docs, f)) and f.endswith('.pdf'))]
    if 'pdf_to_kws.pkl' in os.listdir(path_to_temp):
        with open(os.path.join(path_to_temp, 'pdf_to_kws.pkl'), 'rb') as pk:
            pdf_to_kws = pickle.load(pk)
        pk.close()

    for pdf in tqdm(only_files):
        if pdf in pdf_to_kws:
            continue
        else:
            try:
                kws = pdf_to_keywords(os.path.join(path_to_docs, pdf))
                if kws:
                    pdf_to_kws['.'.join(pdf.split('.')[:-1])] = kws
            except:
                continue

    with open(os.path.join(path_to_temp, 'pdf_to_kws.pkl'), 'wb') as pkw:
        pickle.dump(pdf_to_kws, pkw)
    pkw.close()

    kws_from_source = source_to_kws()

    with open(os.path.join(path_to_temp, 'pdf_to_kws_source.pkl'), 'wb') as pks:
        pickle.dump(kws_from_source, pks)
    pks.close()

    return only_files


if __name__ == '__main__':
    print(len(kws_extractor()))
