#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import numpy as np
import urllib

Dicts = []

def prepare_text(text):
    res = ''
    for c in text:
        if re.match(u'[a-zA-Zа-яА-Яё ]', c) is not None:
            if len(res) != 0:
                if res[-1] == ' ' and c == ' ':
                    continue
            c = c.lower()
            if c == u'ё':
                c = u'е'
            res += c
         #   elif res[-1] != ' ' or c != ' ':
          #      res += c.lower()
    #print(res)
    return res
    
def take_shingles_8sym(text, n):
    for i in range(len(text) - 8):
        part = text[i:i + 8]
        if part not in Dicts[n]:
            Dicts[n].append(part)
 

def take_shingles_3w(text, n):
    w = text.split(' ')
    for i in range(len(w) - 3):
        part = w[i] + ' ' + w[i + 1] + ' ' + w[i + 2]
        if part not in Dicts[n]:
            Dicts[n].append(part)

def check_metric(list1, list2, i, j):
    peresech = []
    for l in list1:
        if l in list2:
            peresech.append(l)
    unif = np.unique(list1 + list2)
    return float(len(peresech)) / len(unif)




names = ['./shingle_lab/p01.txt', './shingle_lab/p02.txt', './shingle_lab/p03.txt', './shingle_lab/p04.txt', './shingle_lab/p05.txt', './shingle_lab/p06.txt', './shingle_lab/p07.txt', './shingle_lab/p08.txt', './shingle_lab/p09.txt', './shingle_lab/p10.txt', './shingle_lab/p11.txt', './shingle_lab/p12.txt', ]

for i in range(len(names)):
    file = open(names[i])
    s = file.read()
    try:
        s = urllib.unquote(s).decode('utf8')
    except UnicodeDecodeError:
        try:
            s = urllib.unquote(s).decode('cp1251')
        except UnicodeDecodeError:
            print('problem')
    Dicts.append([])
    s = prepare_text(s)
    take_shingles_8sym(s, i)
    #take_shingles_3w(s, i)

#print(Dicts)

Metr = np.zeros((12, 12))

for i in range(12):
    for j in range(i):
        Metr[i, j] = check_metric(Dicts[i], Dicts[j], i, j)
        if Metr[i, j] > 0.05:
            print(i + 1, j + 1, Metr[i, j])


print Metr

print Metr[4, 3]





