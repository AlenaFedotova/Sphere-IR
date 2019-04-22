 # coding: utf-8


import sys
import os
import re
import random
import time
import urllib
from sklearn.cluster import AffinityPropagation, MeanShift, KMeans, Birch
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import numpy as np
from collections import Counter


class Sekitei:
    def __init__(self):
        self.proba = {}
        self.quota = {}
        self.is_taken = {}
        self.keys = []
        self.cluster_expressions = {}
        self.delta = {}
        self.model = None
        self.check_functions = []
        self.parameters = []
        
    def _segments(self, segments, param):
        if len(segments) == param['n']:
            return True
        else:
            return False
            
    def _param(self, segments, param):
        if re.search('[\?&]' + param['p'] + '([\&\/].*)?$', url) is not None:
            return True
        else:
            return False
    
    def _param_name(self, segments, param):
        if re.search('[\?&]' + param['p'] + '=', url) is not None:
            return True
        else:
            return False
    
    def _segment_name(self, segments, param):
        if len(segments) <= param['i']:
            return False
        pos = segments[param['i']].find('?')
        if pos != -1:
            segments[param['i']] = segments[param['i']][:pos]
        if segments[param['i']] == param['s']:
            return True
        else:
            return False
    
    def _segment_09(self, segments, param):
        if len(segments) <= param['i']:
            return False
        pos = segments[param['i']].find('?')
        if pos != -1:
            segments[param['i']] = segments[param['i']][:pos]
        if segments[param['i']].isdigit():
            return True
        else:
            return False
    
    def _segment_substr_09(self, segments, param):
        if len(segments) <= param['i']:
            return False
        pos = segments[param['i']].find('?')
        if pos != -1:
            segments[param['i']] = segments[param['i']][:pos]
        if re.search('[^\d]+\d+[^\d]+$', segments[param['i']]) is not None:
            return True
        else:
            return False
    
    def _segment_ext(self, segments, param):
        if len(segments) <= param['i']:
            return False
        pos = segments[param['i']].find('?')
        if pos != -1:
            segments[param['i']] = segments[param['i']][:pos]
        if re.search('\.' + param['ext'] + '$', segments[param['i']]) is not None:
            return True
        else:
            return False
    
    def _segment_ext_substr_09(self, segments, param):
        if len(segments) <= param['i']:
            return False
        pos = segments[param['i']].find('?')
        if pos != -1:
            segments[param['i']] = segments[param['i']][:pos]
        if re.search('\.' + param['ext'] + '$', segments[param['i']]) is not None and re.search('[^\d]+\d+[^\d]+$', segments[param['i']]) is not None:
            return True
        else:
            return False
    
    def _segment_len(self, segments, param):
        if len(segments) <= param['i']:
            return False
        pos = segments[param['i']].find('?')
        if pos != -1:
            segments[param['i']] = segments[param['i']][:pos]
        if len(segments[param['i']]) == param['L']:
            return True
        else:
            return False
    
    def init_one(self, feature):
        m = re.match('segments:([0-9]+)$', feature)
        if m is not None:
            return self._segments, {'n': int(m.groups()[0])}
        m = re.match('param:(.*)$', feature)
        if m is not None:
            return self._param, {'p': m.groups()[0]}
        m = re.match('param_name:(.*)$', feature)
        if m is not None:
            return self._param_name, {'p': m.groups()[0]}
        m = re.match('segment_name_([0-9]+):(.*)$', feature)
        if m is not None:
            return self._segment_name, {'i': int(m.groups()[0]), 's': m.groups()[1]}
        m = re.match('segment_\[0\-9\]_([0-9]+):1$', feature)
        if m is not None:
            return self._segment_09, {'i': int(m.groups()[0])}
        m = re.match('segment_substr[0-9]_([0-9]+):1$', feature)
        if m is not None:
            return self._segment_substr_09, {'i': int(m.groups()[0])}
        m = re.match('segment_ext_([0-9]+):(.*)$', feature)
        if m is not None:
            return self._segment_ext, {'i': int(m.groups()[0]), 'ext': m.groups()[1]}
        m = re.match('segment_ext_substr\[0\-9\]_([0-9]+):(.*)$', feature)
        if m is not None:
            return self._segment_ext_substr_09, {'i': int(m.groups()[0]), 'ext': m.groups()[1]}
        m = re.match('segment_len_([0-9]+):([0-9]+)$', feature)
        if m is not None:
            return self._segment_len, {'i': int(m.groups()[0]), 'L': int(m.groups()[1])}
        print('ooops', feature, url)
        return False, False
        
    def init_functions(self, keys):
        for key in keys:
            f, p = self.init_one(key)
            self.check_functions.append(f)
            self.parameters.append(p)
            
    def check_url(self, url):
        N = len(self.keys)
        X = np.zeros((1, N))
        segments = url.split('/')[3:]
        if segments[-1] == '\n':
            del segments[-1]
        else:
            segments[-1] = segments[-1][:-1]
        for i in range(len(segments)):
            try:
                segments[i] = urllib.unquote(segments[i]).decode('cp1251')
            except UnicodeDecodeError:
                try:
                    segments[i] = urllib.unquote(segments[i]).decode('utf8')
                except UnicodeDecodeError:
                    pass
        for i in range(N):
            X[0, i] = self.check_functions[i](segments, self.parameters[i])
        return X
                    
sekitei = Sekitei()

def check(feature, url):
    segments = url.split('/')[3:]
    if segments[-1] == '\n':
        del segments[-1]
    else:
        segments[-1] = segments[-1][:-1]
    for i in range(len(segments)):
        try:
            segments[i] = urllib.unquote(segments[i]).decode('cp1251')
        except UnicodeDecodeError:
            try:
                segments[i] = urllib.unquote(segments[i]).decode('utf8')
            except UnicodeDecodeError:
                pass
    m = re.match('segments:([0-9]+)$', feature)
    if m is not None:
        n = int(m.groups()[0])
        if len(segments) == n:
            return True
        else:
            return False
    m = re.match('param:(.*)$', feature)
    if m is not None:
        if re.search('[\?&]' + m.groups()[0] + '([\&\/].*)?$', url) is not None:
            return True
        else:
            return False
    m = re.match('param_name:(.*)$', feature)
    if m is not None:
        if re.search('[\?&]' + m.groups()[0] + '=', url) is not None:
            return True
        else:
            return False
    m = re.match('segment_name_([0-9]+):(.*)$', feature)
    if m is not None:
        i = int(m.groups()[0])
        s = m.groups()[1]
        if len(segments) <= i:
            return False
        pos = segments[i].find('?')
        if pos != -1:
            segments[i] = segments[i][:pos]
        if segments[i] == s:
            return True
        else:
            return False
    m = re.match('segment_\[0\-9\]_([0-9]+):1$', feature)
    if m is not None:
        i = int(m.groups()[0])
        if len(segments) <= i:
            return False
        pos = segments[i].find('?')
        if pos != -1:
            segments[i] = segments[i][:pos]
        if segments[i].isdigit():
            return True
        else:
            return False
    m = re.match('segment_substr[0-9]_([0-9]+):1$', feature)
    if m is not None:
        i = int(m.groups()[0])
        if len(segments) <= i:
            return False
        pos = segments[i].find('?')
        if pos != -1:
            segments[i] = segments[i][:pos]
        if re.search('[^\d]+\d+[^\d]+$', segments[i]) is not None:
            return True
        else:
            return False
    m = re.match('segment_ext_([0-9]+):(.*)$', feature)
    if m is not None:
        i = int(m.groups()[0])
        ext = m.groups()[1]
        if len(segments) <= i:
            return False
        pos = segments[i].find('?')
        if pos != -1:
            segments[i] = segments[i][:pos]
        if re.search('\.' + ext + '$', segments[i]) is not None:
            return True
        else:
            return False
    m = re.match('segment_ext_substr\[0\-9\]_([0-9]+):(.*)$', feature)
    if m is not None:
        i = int(m.groups()[0])
        ext = m.groups()[1]
        if len(segments) <= i:
            return False
        pos = segments[i].find('?')
        if pos != -1:
            segments[i] = segments[i][:pos]
        if re.search('\.' + ext + '$', segments[i]) is not None and re.search('[^\d]+\d+[^\d]+$', segments[i]) is not None:
            return True
        else:
            return False
    m = re.match('segment_len_([0-9]+):([0-9]+)$', feature)
    if m is not None:
        i = int(m.groups()[0])
        L = int(m.groups()[1])
        if len(segments) <= i:
            return False
        pos = segments[i].find('?')
        if pos != -1:
            segments[i] = segments[i][:pos]
        if len(segments[i]) == L:
            return True
        else:
            return False
    #print('ooops', feature, url)
    return False


def extract_features(URLS):
    result = Counter()
    X_ = {}
    for line in URLS:
        X_[line] = []
        segments = line.split('/')[3:]
        if segments[-1] == '\n':
            del segments[-1]
        else:
            segments[-1] = segments[-1][:-1]
        result['segments:' + str(len(segments))] += 1
        X_[line].append('segments:' + str(len(segments)))
        if (len(segments) == 0):
            continue
        for i in range(len(segments)):
            segment = segments[i]
            try:
                segment = urllib.unquote(segment).decode('cp1251')
            except UnicodeDecodeError:
                try:
                    segment = urllib.unquote(segment).decode('utf8')
                except UnicodeDecodeError:
                    pass
            if '?' in segment:
                mb_par = segment.split('?')
                params = mb_par[1].split('&')
                for p in params:
                    result['param:' + p] += 1
                    X_[line].append('param:' + p)
                    result['param_name:' + p.split('=')[0]] += 1
                    X_[line].append('param_name:' + p.split('=')[0])
                segment = mb_par[0]
            result['segment_name_' + str(i) + ':' + segment] += 1
            X_[line].append('segment_name_' + str(i) + ':' + segment)
            if segment.isdigit():
                result['segment_[0-9]_' + str(i) + ':1'] += 1
                X_[line].append('segment_[0-9]_' + str(i) + ':1')
            if re.search('[^\d]+\d+[^\d]+$', segment) is not None:
                result['segment_substr[0-9]_' + str(i) + ':1'] += 1
                X_[line].append('segment_substr[0-9]_' + str(i) + ':1')
            ext = segment.split('.')
            if len(ext) > 1:
                result['segment_ext_' + str(i) + ':' + ext[-1]] += 1
                X_[line].append('segment_ext_' + str(i) + ':' + ext[-1])
            if len(ext) > 1 and re.search('[^\d]+\d+[^\d]+$', segment) is not None:
                result['segment_ext_substr[0-9]_' + str(i) + ':' + ext[-1]] += 1
                X_[line].append('segment_ext_substr[0-9]_' + str(i) + ':' + ext[-1])
            result['segment_len_' + str(i) + ':' + str(len(segment))] += 1
            X_[line].append('segment_len_' + str(i) + ':' + str(len(segment)))
    
    for key in result.keys():
        if result[key] > 100:
            sekitei.keys.append(key)
    sekitei.init_functions(sekitei.keys)
    #print keys
    X = np.zeros((len(URLS), len(sekitei.keys)))
    for j, url in enumerate(URLS):
        x = sekitei.check_url(url)
        for i, key in enumerate(sekitei.keys):
            if check(key, url):
                X[j, i] = 1
        if (x != X[j, :]).any():
            print(x, X[j, :])
            '''
            if (key in X_[url]) != X[j, i]:
                print('fuck', key, url, X[j, i], key in X_[url])
            '''
    return X
    
def give_vector(url):
    X = np.zeros((1, len(sekitei.keys)))
    for i, key in enumerate(sekitei.keys):
        if check(key, url):
            X[0, i] = 1
    return X
    


def define_segments(QLINK_URLS, UNKNOWN_URLS, QUOTA):
    sekitei.proba = {}
    sekitei.quota = {}
    sekitei.is_taken = {}
    sekitei.keys = []
    sekitei.cluster_expressions = {}
    sekitei.delta = {}
    sekitei.model = Pipeline([('scaler', StandardScaler()),
                               ('clustering', Birch(n_clusters=20, threshold=0.1))])
    sekitei.check_functions = []
    sekitei.parameters = []
    
    URLS = QLINK_URLS + UNKNOWN_URLS
    X = extract_features(URLS)
    '''
    for i in range(len(URLS)):
        for j in range(len(sekitei.keys)):
            if X[i, j] != check(sekitei.keys[j], URLS[i]):
                print(sekitei.keys[j], URLS[i])
    '''
    y = np.zeros((len(QLINK_URLS) + len(UNKNOWN_URLS)))
    y[:len(QLINK_URLS)] = 1
    
    clusters = sekitei.model.fit_predict(X)
    un_clusters, counts = np.unique(clusters, return_counts=True)
    for cluster, count in np.dstack((un_clusters, counts))[0]:
        sekitei.proba[cluster] = np.sum(y[clusters == cluster]) / count
        sekitei.is_taken[cluster] = 0
        #sekitei.quota[cluster] = np.ceil(QUOTA * np.sum(y[clusters == cluster]) / len(QLINK_URLS))
        k = 1.5
        min_quota = QUOTA / len(QLINK_URLS) * k
        #sekitei.quota[cluster] = np.ceil(k * np.sum(y[clusters == cluster]) + (QUOTA - k * np.sum(y)) * np.sum(1 - y[clusters == cluster]) / np.sum(1 - y))
        sekitei.quota[cluster] = min_quota * np.sum(y[clusters == cluster])
        sekitei.cluster_expressions[cluster] = np.mean(X[clusters == cluster], axis=0) > 0.5
        sekitei.delta[cluster] = np.ceil(np.sum(np.abs(np.mean(X[clusters == cluster], axis=0) - sekitei.cluster_expressions[cluster])))
    #print(sekitei.delta)



def reg_predict(X):
    D = len(sekitei.cluster_expressions.keys())
    cl = -1
    for cluster, regs in sekitei.cluster_expressions.items():
        #print(np.sum(np.abs(X - regs)), cluster)
        if np.sum(np.abs(X - regs)) == 0:
            return cluster
        elif np.sum(np.abs(X - regs)) < D:
            D = np.sum(np.abs(X - regs))
            cl = cluster
    if cl != -1:
        if D <= sekitei.delta[cl]:
            return cl
    return -1


#
# returns True if need to fetch url
#
def fetch_url(url):
    #global sekitei
    #return sekitei.fetch_url(url);
    X = give_vector(url)
    #y = sekitei.predict(X)[0]
    y = reg_predict(X)
    if y == -1:
        return False
    
    if sekitei.is_taken[y] >= sekitei.quota[y]:
        return False
    sekitei.is_taken[y] += 1
    return True
    
