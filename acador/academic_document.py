#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 09/12/2022 16:56
# @Author  : Xiao
# @File    : academic_document.py
# @Software: PyCharm

import bibtexparser
from utils.hasher import hash_string


class AcademicDocument:
    def __init__(self, year=1444, authors=None, title='test'):
        if authors is None:
            self.authors = ['dog']
        else:
            self.authors = authors

        self.year = year
        self.title = title
        self.type = ''
        self.keywords = []
        self.booktitle = ''
        self.hash = self.hash_doc()
        self.abstract = ''

    def hash_doc(self):
        self.hash = hash_string(str(self.year)+' '.join(self.authors)+self.title)
        return self.hash


if __name__ == '__main__':
    ads = []
    for i in range(5):
        ads.append(AcademicDocument(year=i))
        ads.append(AcademicDocument())
    for ad in ads:
        print(ad.hash)
