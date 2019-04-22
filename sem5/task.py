#!/usr/bin/env python
# -*- coding: utf-8 -*-

import doc2words
import operator

image = {}
web = {}

with open('image_queries.txt', 'r') as f:
    for line in f:
        words = doc2words.extract_words(line)
        for word in words:
            if word in image:
                image[word] += 1
            else:
                image[word] = 1

with open('web_queries.txt', 'r') as f:
    for line in f:
        words = doc2words.extract_words(line)
        for word in words:
            if word in web:
                web[word] += 1
            else:
                web[word] = 1
                
proba = {}

for word in image:
    if word in web:
        proba[word] = image[word] / (web[word])
    else:
        proba[word] = 1e6
        
for word in web:
    if word not in image:
        proba[word] = 1e-6
        
image_queries = {}
web_queries = {}

with open('image_queries.txt', 'r') as f:
    for line in f:
        words = doc2words.extract_words(line)
        if len(words) == 0:
            continue
        image_queries[line] = 1
        for word in words:
            image_queries[line] *= proba[word]

with open('web_queries.txt', 'r') as f:
    for line in f:
        words = doc2words.extract_words(line)
        if len(words) == 0:
            continue
        web_queries[line] = 1
        for word in words:
            web_queries[line] *= proba[word]
            
print(sorted(web_queries.items(), key=operator.itemgetter(1))[-10:][::-1])

print(sorted(image_queries.items(), key=operator.itemgetter(1))[:10])
