#!/usr/bin/env python
import docreader
import doc2words
import argparse
import array
import hash_serialize
import index_write
import pickle

def parse_command_line():
    parser = argparse.ArgumentParser(description='compressed documents reader')
    parser.add_argument('encoding', nargs=1, help='Varbyte or simple9') # choose encoding
    parser.add_argument('files', nargs='+', help='Input files (.gz or plain) to process')
    return parser.parse_args()

encoding = parse_command_line().encoding[0] # choose encoding
reader = docreader.DocumentStreamReader(parse_command_line().files)
index = {}
last_doc = {}

max_docs = 200001
index_num = 1
ind_small = 0

with open('urls.txt', 'w') as f:
    for ind, doc in enumerate(reader):
        ind_small += 1
        words = doc2words.extract_words(doc.text)
        f.write(doc.url + '\n')
        for word in words:
            word = hash(word)
            if word not in last_doc:
                index[word] = [ind]
                last_doc[word] = ind
            else:
                if last_doc[word] != ind:
                    if word not in index:
                        index[word] = []
                    index[word].append(ind - last_doc[word])
                    last_doc[word] = ind
        if ind_small == max_docs:
            positions_sizes = index_write.index_write('index' + str(index_num), index, encoding)
            with open('dictionary' + str(index_num), 'wb') as fd:
                pickle.dump(positions_sizes, fd)
            index_num += 1
            ind_small = 0
            index = {}
            
positions_sizes = index_write.index_write('index' + str(index_num), index, encoding)
with open('dictionary' + str(index_num), 'wb') as fd:
    pickle.dump(positions_sizes, fd)

with open('conf.txt', 'w') as f:
    f.write(encoding + '\n')
    f.write(str(index_num) + '\n')
