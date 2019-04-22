# -*- coding: utf-8 -*-
import hash_serialize
import index_write
import pickle
import re

SPLIT_RGX = re.compile(r'\w+', re.U)

encoding = ''
N = 0
with open('conf.txt', 'r') as f:
    lines = f.readlines()
    encoding = lines[0][:-1]
    N = int(lines[1])
    
    
def read_from_index(h_w):
    res = []
    t_find = 0
    t_read = 0
    for i in xrange(N):
        tup = hash_serialize.find_term('dictionary' + str(i + 1), h_w)
        if tup is not None:
            res += index_write.index_read('index' + str(i + 1), tup, encoding)
    print t_find, t_read
    return res
    

def make_tree(query):
    query = query.decode('utf8').lower()
    query = query.replace('&', ' AND ').replace('|', ' OR ').replace('!', ' NOT ').replace('(', ' BRL ').replace(')', ' BRR ')
    parts = re.findall(SPLIT_RGX, query)
    return build_tree(parts)
    
def build_tree(parts):
    if len(parts) == 1:
        return TreeTerm(parts[0])
    pos = len(parts) - 1
    pos_opr = len(parts) - 2
    end = len(parts)
    if parts[-1] == 'BRR':
        pos = find_br(parts)
        pos_opr = pos - 1
        end -= 1
        pos += 1
    if_not = False
    while parts[pos_opr] == 'NOT' and pos_opr >= 0:
        pos_opr -= 1
        if_not = not if_not
    if pos_opr < 0:
        if if_not:
            return TreeNot(build_tree(parts[pos:end]))
        return build_tree(parts[pos:end])
    if parts[pos_opr] == 'AND':
        if if_not:
            return TreeAnd(build_tree(parts[:pos_opr]), TreeNot(build_tree(parts[pos:end])))
        return TreeAnd(build_tree(parts[:pos_opr]), build_tree(parts[pos:end]))
    if parts[pos_opr] == 'OR':
        if if_not:
            return TreeOr(build_tree(parts[:pos_opr]), TreeNot(build_tree(parts[pos:end])))
        return TreeOr(build_tree(parts[:pos_opr]), build_tree(parts[pos:end]))
    return None
    
def find_br(parts):
    i = len(parts) - 2
    counter = 0
    while counter != 0 or parts[i] != 'BRL':
        if parts[i] == 'BRR':
            counter += 1
        if parts[i] == 'BRL':
            counter -= 1
        i -= 1
    return i
    
class TreeTerm:
    def __init__(self, word):
        self.word = word
        self.doc = []
        self.doc = read_from_index(hash(word))
        self.cur = 0
        if self.cur >= len(self.doc):
            self.cur = -1
        else:
            self.cur_doc = self.doc[self.cur]
            
    def goto(self, id):
        if self.cur == -1:
            return
        while self.cur_doc < id:
            self.cur += 1
            if self.cur >= len(self.doc):
                self.cur = -1
                return
            self.cur_doc += self.doc[self.cur]
    
    def evaluate(self):
        if self.cur == -1:
            return -1
        else:
            return self.cur_doc
            
    def __str__(self):
        return str(self.word.encode('utf8'))
    

class TreeNot:
    def __init__(self, node):
        self.node = node
        self.id = 0
            
    def goto(self, id):
        self.node.goto(id)
        self.id = id
        if id == -1:
            self.id = 0
    
    def evaluate(self):
        while self.id == self.node.evaluate():
            self.id += 1
            self.node.goto(self.id)
        return self.id
        
    def __str__(self):
        return 'Not(' + str(self.node) + ')'


class TreeAnd:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
            
    def goto(self, id):
        self.node1.goto(id)
        self.node2.goto(id)
    
    def evaluate(self):
        ev1 = self.node1.evaluate()
        ev2 = self.node2.evaluate()
        while ev1 != ev2:
            if ev1 == -1 or ev2 == -1:
                return -1
            if ev1 > ev2:
                self.node2.goto(ev1)
                ev2 = self.node2.evaluate()
            else:
                self.node1.goto(ev2)
                ev1 = self.node1.evaluate()
        return ev1
        
    def __str__(self):
        return 'And(' + str(self.node1) + ', ' + str(self.node2) + ')'


class TreeOr:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
            
    def goto(self, id):
        self.node1.goto(id)
        self.node2.goto(id)
    
    def evaluate(self):
        ev1 = self.node1.evaluate()
        ev2 = self.node2.evaluate()
        if ev1 == -1:
            return ev2
        if ev2 == -1:
            return ev1
        res = min(self.node1.evaluate(), self.node2.evaluate())
        return res

    def __str__(self):
        return 'Or(' + str(self.node1) + ', ' + str(self.node2) + ')'

