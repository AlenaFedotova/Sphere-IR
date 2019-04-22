#!/usr/bin/env python
# -*- coding: utf-8 -*-
import document_pb2
import struct
import sys
import doc2words
import hashlib
import numpy as np
import argparse
import gzip
import mmh3
import re
import string


class DocumentStreamReader:
    def __init__(self, paths):
        self.paths = paths

    def open_single(self, path):
        return gzip.open(path, 'rb') if path.endswith('.gz') else open(path, 'rb')

    def __iter__(self):
        for path in self.paths:
            with self.open_single(path) as stream:
                while True:
                    sb = stream.read(4)
                    if sb == '':
                        break

                    size = struct.unpack('i', sb)[0]
                    msg = stream.read(size)
                    doc = document_pb2.document()
                    doc.ParseFromString(msg)
                    yield doc


def parse_command_line():
    parser = argparse.ArgumentParser(description='compressed documents reader')
    parser.add_argument('files', nargs='+', help='Input files (.gz or plain) to process')
    return parser.parse_args()
    
class TextNormalizer:
    @staticmethod
    def join_numbers(text):
        regex = re.compile('([\d])[\s]+([\d])')
        return regex.sub('\\1\\2', text)

    @staticmethod
    def clean_out_punct(text):
        regex = re.compile('[%s]' % re.escape(string.punctuation + "«" + "»"))
        return regex.sub(' ', text)

    @staticmethod
    def lower_case(text):
        return text.lower()

    @staticmethod
    def remove_entities(text):
        regex = re.compile('&[0-9a-z_A-Z]+;')
        return regex.sub(' ', text)
    
basis = [1663, 1999, 2203, 2381, 2411,
         2657, 2789, 2843, 2861, 2909,
         2953, 3169, 3217, 3259, 3491,
         3467, 3469, 3499, 3511, 27644437]

def Hash(n, i):
    return divmod(n, basis[i])[1]
    
def normalize(text):
    text = TextNormalizer.join_numbers(text)
    text = TextNormalizer.remove_entities(text)
    text = TextNormalizer.clean_out_punct(text)
    text = TextNormalizer.lower_case(text)
    return text

    
def TakeShingles(text):
    words = doc2words.extract_words(text)
    shingles = []
    for i in xrange(len(words) - 5):
        shingle = ' '.join(words[i:i + 5])
        shingles.append(mmh3.hash(shingle.encode('utf-8')))
    return shingles
    
def TakeMinShingles(text):
    text = normalize(text)
    shingles = TakeShingles(text)
    if len(shingles) == 0:
        return None
    res = [None] * 20
    for i in xrange(20):
        sh = shingles[0]
        h = Hash(sh, i)
        for sh_new in shingles:
            h_new = Hash(sh_new, i)
            if h_new < h:
                sh = sh_new
                h = h_new
        res[i] = sh
    return shingles, res


if __name__ == '__main__':
    reader = DocumentStreamReader(parse_command_line().files)
    minshingles = []
    urls = []
    for doc in reader:
        tmp = TakeMinShingles(doc.text)
        if tmp is None:
            continue
        minshingles.append(tmp[1])
        urls.append(doc.url)
    
    Groups = {}
    for i in xrange(len(urls)):
        for j in xrange(20):
            k = '_'.join([str(j), str(minshingles[i][j])])
            if k not in Groups.keys():
                Groups[k] = [i]
            else:
                Groups[k].append(i)
                
    X = np.zeros((len(urls), len(urls)))
    for v in Groups.values():
        for p1 in xrange(len(v)):
            for p2 in xrange(p1 + 1,len(v)):
                X[v[p2], v[p1]] += 1
            
    for i in xrange(len(urls)):
        for j in xrange(i):
            if X[i, j] > 15:
                print urls[i], urls[j], X[i, j] / 20
