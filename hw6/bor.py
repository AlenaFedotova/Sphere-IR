# -*- coding: utf-8 -*-
import msgpack
import numpy as np

mis = 'mis'
lan = 'lan_uni'

with open(mis, 'r') as f:
    unp = msgpack.Unpacker(f, max_map_len=524288)
    m_model = unp.unpack()
with open(lan, 'r') as f:
    l_model = msgpack.unpack(f)

alpha = 1

class Bor(object):
    def __init__(self, word, n, eps):
        self.word = u'^' + word + u'_'
        self.n = n
        self.eps = eps
        self.cand = []

    def check_candidate(self, cur, w, fix):
        res = cur[1:].replace(u'_', u'')
        self.cand.append((res, w, fix, True))
        self.cand.sort(key=lambda tup: -tup[1])
        if len(self.cand) > self.n:
            self.cand = self.cand[:-1]

    def rec_search(self, pos, cur, w, fix, empty):
        if w < self.eps:
            return
        if pos + 1 < len(self.word):
            if not empty:
                self.rec_search(pos + 1, cur + self.word[pos + 1], w, fix, False)
                if self.word[pos:pos + 2].encode('utf8') in m_model:
                    if cur[-1].encode('utf8') in m_model[self.word[pos:pos + 2].encode('utf8')]:
                        possible_fix = m_model[self.word[pos:pos + 2].encode('utf8')][cur[-1].encode('utf8')]
                        for pf in possible_fix.keys():
                            self.rec_search(pos + 1, cur + pf.decode('utf8'), w + possible_fix[pf], fix + [('change', pos, pf.decode('utf8'), self.word[pos + 1])], False) 
                if (self.word[pos] + u'_').encode('utf8') in m_model:
                    if cur[-1].encode('utf8') in m_model[(self.word[pos] + u'_').encode('utf8')]:
                        possible_fix = m_model[(self.word[pos] + u'_').encode('utf8')][cur[-1].encode('utf8')]
                        for pf in possible_fix.keys():
                            self.rec_search(pos + 1, cur + pf.decode('utf8'), w + possible_fix[pf], fix + [('add line', pos, pf.decode('utf8'), self.word[pos + 1])], True)
            else:
                self.rec_search(pos, cur + self.word[pos], w, fix, False)
                if (u'_' + self.word[pos]).encode('utf8') in m_model:
                    if cur[-1].encode('utf8') in m_model[(u'_' + self.word[pos]).encode('utf8')]:
                        possible_fix = m_model[(u'_' + self.word[pos]).encode('utf8')][cur[-1].encode('utf8')]
                        for pf in possible_fix.keys():
                            self.rec_search(pos, cur + pf.decode('utf8'), w + possible_fix[pf], fix + [('change', pos, pf.decode('utf8'), self.word[pos + 1])], False)
                if (self.word[pos] + u'_').encode('utf8') in m_model:
                    if cur[-1].encode('utf8') in m_model[(self.word[pos] + u'_').encode('utf8')]:
                        possible_fix = m_model[(self.word[pos] + u'_').encode('utf8')][cur[-1].encode('utf8')]
                        for pf in possible_fix.keys():
                            self.rec_search(pos, cur + pf.decode('utf8'), w + possible_fix[pf], fix + [('add line', pos, pf.decode('utf8'), self.word[pos + 1])], True)
        elif pos < len(self.word) and empty:
            if (u'_' + self.word[pos]).encode('utf8') in m_model:
                if cur[-1].encode('utf8') in m_model[(u'_' + self.word[pos]).encode('utf8')]:
                    possible_fix = m_model[(u'_' + self.word[pos]).encode('utf8')][cur[-1].encode('utf8')]
                    for pf in possible_fix.keys():
                        self.rec_search(pos, cur + pf.decode('utf8'), w + possible_fix[pf], fix + [('change', pos, pf.decode('utf8'), self.word[pos])], False)
        else:
            res = cur[1:].replace(u'_', u'')
            if res.encode('utf8') in l_model:
                self.check_candidate(cur, w + l_model[res.encode('utf8')], fix)

    def candidates(self):
        self.rec_search(0, u'^', 0, [], False)
        if len(self.cand) == 0:
            self.check_candidate(self.word, 0, [])
        return self.cand
