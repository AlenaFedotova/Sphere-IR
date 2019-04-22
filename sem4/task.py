#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
#from Levenshtein import distance
    
dic = {}
dic[''] = 0

def ldistance(a, b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n+1) # Keep current and previous row, not entire matrix
    for i in range(1, m+1):
        previous_row, current_row = current_row, [i]+[0]*n
        for j in range(1,n+1):
            add, delete, change = previous_row[j]+1, current_row[j-1]+1, previous_row[j-1]
            if a[j-1] != b[i-1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]

def spell(word):
    res = ''
    dist = -1
    for k in dic.keys():
        cur = ldistance(k, word)
        if dist == -1 or cur < dist or (cur == dist and dic[res] < dic[k]):
            res = k
            dist = cur
    return res
    
with open('lenta_words.txt', 'r') as f:
    for line in f:
        line = line[:-1]
        if line in dic:
            dic[line] += 1
        else:
            dic[line] = 1

for line in sys.stdin:
    line = line[:-1]
    words = line.split()
    res = []
    for word in words:
        res.append(spell(word))
    print(' '.join(res))
