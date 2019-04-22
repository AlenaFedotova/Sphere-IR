#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import tree
import hash_serialize
import index_write
import sys
import pickle

def search(query):
    print query[:-1]
    Tree = tree.make_tree(query[:-1])

    t_goto = 0
    t_ev = 0
    res = []
    last_id = -1
    Tree.goto(last_id)
    last_id = Tree.evaluate()
    while last_id != -1:
        res.append(last_id)
        last_id += 1
        Tree.goto(last_id)
        last_id = Tree.evaluate()
    print len(res)

    with open('urls.txt', 'r') as f:
        lines = f.readlines()
        for r in res:
            print lines[r][:-1]
        
        
        
for line in sys.stdin:
    search(line)
