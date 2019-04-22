from collections import Counter
import doc2words
import numpy as np

def create_model(f, type='unigram'):
    if type == 'query':
        return query_model(f)
    if type == 'unigram':
        return unigram_model(f)
    if type == 'bigram':
        return bigram_model(f)
    raise ValueError
        
def query_model(f):
    res = Counter()
    N = 0
    for line in f:
        line = line.decode('utf8')
        words = None
        parts = line.split('\t')
        if len(parts) == 1:
            words = doc2words.extract_words(parts[0])
        elif len(parts) == 2:
            words = doc2words.extract_words(parts[1])
        else:
            raise ValueError
        query = ' '.join(words)
        res[query] += 1
        N += 1
    for k in res.keys():
        res[k] = np.log(float(res[k]) / N)
    return res
        
def unigram_model(f):
    res = Counter()
    N = 0
    for line in f:
        line = line.decode('utf8')
        words = None
        parts = line.split('\t')
        if len(parts) == 1:
            words = doc2words.extract_words(parts[0])
        elif len(parts) == 2:
            words = doc2words.extract_words(parts[1])
        else:
            raise ValueError
        N += len(words)
        for word in words:
            res[word] += 1
    for k in res.keys():
        res[k] = np.log(float(res[k]) / N)
    return res
        
def bigram_model(f):
    res = {'': Counter()}
    N = 0
    for line in f:
        line = line.decode('utf8')
        words = None
        parts = line.split('\t')
        if len(parts) == 1:
            words = doc2words.extract_words(parts[0])
        elif len(parts) == 2:
            words = doc2words.extract_words(parts[1])
        else:
            raise ValueError
        N += len(words)
        for i in range(len(words) - 1):
            if words[i] not in res:
                res[words[i]] = Counter()
            res[words[i]][words[i + 1]] += 1
        if len(words) > 0:
            res[''][words[0]] += 1
    for k in res.keys():
        for k1 in res[k].keys():
            res[k][k1] = np.log(float(res[k][k1]) / N)
    return res
    
