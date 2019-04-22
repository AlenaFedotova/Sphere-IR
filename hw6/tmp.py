#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Levenshtein
import doc2words
import msgpack

print(u'\u043c\u0438\u0434\u0432\u0435\u0434\u044c')

lan = 'lan_uni'
with open(lan, 'r') as f:
    l_model = msgpack.unpack(f)
mis = 'mis'
with open(mis, 'r') as f:
    m_model = msgpack.unpack(f)
    
print(u'^м' in m_model)
print(u'медведь'.encode('utf8') in l_model)
    
def string_insert(string, index, sym):
    return string[:index] + sym + string[index:]

ss = 'президенты'.decode('utf8')
sd = 'пtрезуиkет'.decode('utf8')
print('ъъъъ'.decode('utf8') in l_model)


ss = '^' + ss
sd = '^' + sd
i_s = 0
i_d = 0
eds = Levenshtein.editops(ss, sd)
print(eds)
for ed in eds:
    if ed[0] == 'insert':
        ss = string_insert(ss, ed[1] + i_s, '_')
        i_s += 1
    if ed[0] == 'delete':
        sd = string_insert(sd, ed[2] + i_d, '_')
        i_d += 1

print ss, sd
