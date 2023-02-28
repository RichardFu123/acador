#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/02/2023 15:51
# @Author  : Xiao
# @File    : pdf_to_keywords.py
# @Software: PyCharm

import fitz
import re


def pdf_to_keywords(path_to_pdf):

    doc = fitz.open(path_to_pdf)

    blocks = doc.load_page(0).get_text('blocks')
    try:
        blocks += doc.load_page(1).get_text('blocks')
    except:
        pass

    # for b in blocks:
    #     print(b)

    texts = [b[-3] for b in blocks]
    res = []
    for i in range(len(texts)-1):
        if ('keyword' in texts[i].lower() or 'key word' in texts[i].lower()) and len(texts[i]) < 15:
            texts[i] = ''
            texts[i+1] = 'kws: ' + texts[i+1]
    for t in texts:
        if res:
            res = keywords_string_to_list(cut_by_kws(t))
        else:
            res += keywords_string_to_list(cut_by_kws(t))
        if res:
            return res


    return []


# def get_keywords(string):
def cut_by_kws(t):
    kws = [
        'keywords',
        'kws'
    ]
    for kw in kws:
        if cut_with_word(t, kw):
            return cut_with_word(t, kw)
    return ''


def cut_with_word(string: str, word: str):
    if not word.lower() in string.lower():
        # print(string.lower())
        return ''
    if string.lower()[::-1].find('.') and (len(string.lower()) - string.lower()[::-1].find('.') > string.lower().find(word.lower())+len(word)):
        cut = string[string.lower().find(word.lower()) + len(word):len(string.lower()) - string.lower()[::-1].find('.')].strip()
    else:
        cut = string[string.lower().find(word.lower())+len(word):].strip()
    cut = cut.replace('- \n', '-\n')
    if cut.find('\n') and cut[cut.find('\n')] != '-':
        return cut.strip('\n')
    else:
        return cut


def keywords_string_to_list(kw_string):
    kw_string = kw_string.replace('-\n', '')
    kw_string = kw_string.replace('\n', '')
    kw_string = kw_string.replace(':', '').strip()
    kws = kw_string.split(',')
    if not is_keywords_list(kws):
        kws = kw_string.split('.')
    kws = [i for i in kws if i]

    for j in range(len(kws)):

        if kws[j].strip().startswith('——') or kws[j].strip().startswith('--'):
            kws[j] = kws[j].strip()[2:].strip()
        elif kws[j].strip().startswith('—') or kws[j].strip().startswith('-'):
            kws[j] = kws[j].strip()[1:].strip()
        elif kws[j].strip().startswith('and Phrases') or kws[j].strip().startswith('and phrases'):
            kws[j] = kws[j].strip()[11:].strip()
        elif kws[j].strip().startswith('& Phrases') or kws[j].strip().startswith('& phrases'):
            kws[j] = kws[j].strip()[9:].strip()
        elif kws[j].strip().startswith('and ') or kws[j].strip().startswith('And '):
            kws[j] = kws[j].strip()[4:].strip()
        else:
            kws[j] = kws[j].strip()
        kws[j] = kws[j].replace("\r", ' c')
        if kws[j].find('- ') and kws[j].startswith('- '):
            kws[j] = kws[j].replace('- ', '').strip()
        else:
            kws[j] = kws[j].replace('- ', '-')
        kws[j] = kws[j].strip('-')
        kws[j] = kws[j].strip('–')
        kws[j] = kws[j].strip('.')
        kws[j] = kws[j].strip()




    if kws and len(kws[-1]) > 30 and kws[-1].find(' and '):
        kws = kws[:-1]+kws[-1].split(' and ')

    if is_keywords_list(kws):
        for i in range(len(kws)):
            kws[i] = kws[i].strip()
            if kws[i][-1] == '.':
                kws[i] = kws[i][:-1]
        return kws
    else:
        return []


def is_keywords_list(kws):
    bad_words = [
        'e.g.'
    ]
    if len(''.join(kws)) > 150:
        return False
    if len(kws) < 3 or len(kws) > 8:
        return False
    if not isinstance(kws, type([])):
        return False
    for i in kws:
        if len(i) > 60 or len(i) < 2 or i.lower() in bad_words or re.findall(r'\d{2,}', i):
            return False
        if '∈' in i or '�' in i:
            return False
    return True


if __name__ == '__main__':
    _test = [
        '0801.3111',
        '0711.3128',
        '0710.3642',
        '0706.2732',
        '0708.2230',
        '0708.2309',
        '0708.3341',
        '0708.3879',
        '0709.0428',
        '0803.2174',
        '0804.0556',
        '1005.1771',
        '0707.2630',
        '2010.14228',
        '1003.6030',
        '1901.09161',
        '1806.09447',
        '2105.00560',
        '2209.01339'
    ]

    for _t in _test:
        print(pdf_to_keywords(f'../../docs/{_t}.pdf'))
