#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mis_model
import lan_model
import msgpack

data = 'queries_all.txt'
mis = 'mis'
lan_uni = 'lan_uni'
lan_bi = 'lan_bi'

with open(data, 'r') as f:
    m_model = mis_model.create_model(f, type='bigram')
    with open(mis, 'w') as m:
        msgpack.pack(m_model, m)

with open(data, 'r') as f:
    l_model = lan_model.create_model(f, type='unigram')
    with open(lan_uni, 'w') as l:
        msgpack.pack(l_model, l)

with open(data, 'r') as f:
    l_model = lan_model.create_model(f, type='bigram')
    with open(lan_bi, 'w') as l:
        msgpack.pack(l_model, l)
