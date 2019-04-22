#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import doc2words
import msgpack
import bor
import itertools
import re
import os
from time import time

t = time()

os.environ["LANG"] = 'ru_RU.UTF-8'

lan = 'lan_bi'
with open(lan, 'r') as f:
    l_model = msgpack.unpack(f)

class Query(object):
    def __init__(self, query):
        self.query = query
        self.words = doc2words.extract_words(query)
        
    def find_word_positions(self, word):
        pos1 = self.query.find(word)
        return pos1, pos1 + len(word)
        
    def apply_transforms(self, word, transforms):
        di = 0
        for t in transforms:
            t = list(t)
            pos = t[1] + di
            if t[0] == 'change':
                if t[2] == u'_':
                    word = word[:pos] + word[pos + 1:]
                    di -= 1
                else:
                    if pos < len(word):
                        if word[pos].isupper():
                            t[2] = t[2].upper()
                    else:
                        if word[-1].isupper():
                            t[2] = t[2].upper()
                    word = word[:pos] + t[2] + word[pos + 1:]
            elif t[0] == 'add line':
                if len(word) > 0:
                    if pos < len(word):
                        if word[pos].isupper():
                            t[2] = t[2].upper()
                    else:
                        if word[pos - 1].isupper():
                            t[2] = t[2].upper()
                word = word[:pos] + t[2] + word[pos:]
                di += 1
        return word
                
        
    def return_to_query(self, new_query, type):
        res = self.query
        if type == 'dic':
            words = re.findall(doc2words.SPLIT_RGX, self.query)
            for i, word in enumerate(words):
                pos1, pos2 = self.find_word_positions(word)
                self.query = self.query[:pos1] + self.apply_transforms(word, new_query[i][2]) + self.query[pos2:]
        return self.query
        
def find_weight(query):
    if len(query) == 0:
        return 0
    w = 0
    if query[0][0].encode('utf8') not in l_model['']:
        w -= 10000
    else:
        w += l_model[''][query[0][0].encode('utf8')]
    w += query[0][1]
    for i in range(1, len(query)):
        w += query[i][1]
        if query[i - 1][0].encode('utf8') not in l_model:
            w -= 10000
        elif query[i][0].encode('utf8') not in l_model[query[i - 1][0].encode('utf8')]:
            w -= 10000
        else:
            w += l_model[query[i - 1][0].encode('utf8')][query[i][0].encode('utf8')]
    return w

def estimate_query(query):
    words = doc2words.extract_words(query)
    if len(words) == 0:
        return 0
    w = 0
    if words[0].encode('utf8') not in l_model['']:
        w -= 10000
    else:
        w += l_model[''][words[0].encode('utf8')]
    for i in range(1, len(words)):
        if words[i - 1].encode('utf8') not in l_model:
            w -= 10000
        elif words[i].encode('utf8') not in l_model[words[i - 1].encode('utf8')]:
            w -= 10000
        else:
            w += l_model[words[i - 1].encode('utf8')][words[i].encode('utf8')]
    return w
        
def find_best(cand):
    w0 = float('-inf')
    c0 = None
    for it in itertools.product(*cand):
        w = find_weight(it)
        if c0 is None or w > w0:
            w0 = w
            c0 = it
    return c0, w0

def fix_dic(query):
    q = Query(query)
    n = 5
    cand = [None] * len(q.words)
    for i, word in enumerate(q.words):
        b = bor.Bor(word, n, -15)
        cand[i] = b.candidates()
        '''
        print('Word ' + str(i))
        for c in cand[i]:
            print(c[0])
            print(c[1])
            print(c[2])
            print(c[3])
        '''
    best, w = find_best(cand)
    res = q.return_to_query(best, 'dic')
    return res, estimate_query(res)
    
_eng_chars = u"`~!@#$%^&qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?"
_rus_chars = u"ёЁ!\"№;%:?йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"
_trans_table_enru = dict(zip(_eng_chars, _rus_chars))
_trans_table_ruen = dict(zip(_rus_chars, _eng_chars))
 
def change_layout_2ru(s):
    return u''.join([_trans_table_enru.get(c, c) for c in s])
    
def change_layout_2en(s):
    return u''.join([_trans_table_ruen.get(c, c) for c in s])

def fix_layout(query):
    q1 = ''
    try:
        q1 = change_layout_2ru(query)
    except KeyError:
        q1 = change_layout_2en(query)
    return q1, estimate_query(q1)
    
def str_find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)
    
def fix_join(query):
    q0 = query
    w0 = estimate_query(query)
    its = list(str_find_all(query, u' '))
    for it in its:
        q = query[:it] + query[it + 1:]
        w = estimate_query(q)
        if w > w0:
            w0 = w
            q0 = q
    return q0, w0
    
def fix_split(query):
    q0 = query
    w0 = estimate_query(query)
    for i in range(1, len(query) - 1):
        q = query[:i] + u' ' + query[i:]
        w = estimate_query(q)
        if w > w0:
            w0 = w
            q0 = q
    return q0, w0

def fix_all(query):
    q0, w0 = fix_dic(query)
    q, w = fix_layout(query)
    if w > w0:
        q0, w0 = q, w
    q, w = fix_join(query)
    if w > w0:
        q0, w0 = q, w
    q, w = fix_split(query)
    if w > w0:
        q0, w0 = q, w
    if w0 < -3000:
        return query
    return q0
    
def fix_iter(query):
    q0 = ''
    q = query
    while q != q0:
        q0 = q
        q = fix_all(q0)
        #print(q)
    return q
    
#print('ready ' + str(time() - t))
for line in sys.stdin:
    sys.stdout.write(fix_iter(line.decode('utf8')).encode('utf8'))
