# -*- coding: utf-8 -*-
import Levenshtein
from collections import Counter
import doc2words
import numpy as np

N = 0

def create_model(f, type='bigram'):
    res = {}
    for line in f:
        words = None
        parts = line.split('\t')
        if len(parts) == 1:
            continue
        elif len(parts) != 2:
            raise ValueError
        if type == 'unigram':
            add_uni_query(res, '='.join(doc2words.extract_words(parts[1].decode('utf8'))), '='.join(doc2words.extract_words(parts[0].decode('utf8'))))
        elif type == 'bigram':
            add_bi_query(res, '='.join(doc2words.extract_words(parts[1].decode('utf8'))), '='.join(doc2words.extract_words(parts[0].decode('utf8'))))
        else:
            raise ValueError
    if type == 'unigram':
        for k in res.keys():
            res[k] = np.log(res[k])
    elif type == 'bigram':
        for k in res.keys():
            for k1 in res[k].keys():
                for k2 in res[k][k1].keys():
                    res[k][k1][k2] = np.log(float(res[k][k1][k2]) / N)
    return res
    
    
def string_insert(string, index, sym):
    return string[:index] + sym + string[index:]
    
def add_uni_query(count, ss, sd):
    global N
    ss = '^' + ss
    sd = '^' + sd
    i_s = 0
    i_d = 0
    eds = Levenshtein.editops(ss, sd)
    for ed in eds:
        if ed[0] == 'insert':
            ss = string_insert(ss, ed[1] + i_s, '_')
            i_s += 1
        if ed[1] == 'delete':
            sd = string_insert(sd, ed[2] + i_d, '_')
            i_d += 1
    assert(len(ss) == len(sd))
    for i in range(len(ss) - 1):
        if sd[i + 1] not in count:
            count[sd[i + 1]] = Count()
        count[sd[i + 1]][ss[i + 1]] += 1
        N += 1
    
def add_bi_query(count, ss, sd):
    global N
    ss = '^' + ss
    sd = '^' + sd
    i_s = 0
    i_d = 0
    eds = Levenshtein.editops(ss, sd)
    for ed in eds:
        if ed[0] == 'insert':
            ss = string_insert(ss, ed[1] + i_s, '_')
            i_s += 1
        if ed[0] == 'delete':
            sd = string_insert(sd, ed[2] + i_d, '_')
            i_d += 1
    assert(len(ss) == len(sd))
    sym = '='.decode('utf8')
    for i in range(len(ss) - 2):
        if sd[i + 1] == ss[i + 1] or sym == sd[i] or sym == sd[i + 1] or sym == ss[i] or sym == ss[i + 1]:
            continue
        if sd[i:i + 2] not in count:
            count[sd[i:i + 2]] = {}
        if ss[i] not in count[sd[i:i + 2]]:
            count[sd[i:i + 2]][ss[i]] = Counter()
        count[sd[i:i + 2]][ss[i]][ss[i + 1]] += 1
        N += 1
