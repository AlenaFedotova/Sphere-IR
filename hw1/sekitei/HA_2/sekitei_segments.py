 # coding: utf-8


import sys
import os
import re
import random
import time
import urllib
from sklearn.cluster import AffinityPropagation, MeanShift, KMeans, Birch, AgglomerativeClustering, DBSCAN
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC, NuSVC
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import jaccard_similarity_score
import numpy as np
from collections import Counter
import time


class Sekitei:
    def __init__(self):
        self.proba = {}
        self.quota = {}
        self.is_taken = {}
        self.keys = []
        self.cluster_expressions = {}
        self.delta = {}
        self.part = {}
        self.bad_part = {}
        self.i = 0
        self.j = 0
        self.cluster_expressions_help = {}
        self.model = Pipeline([('scaler', StandardScaler()),
                              # ('clustering', Birch(n_clusters=20, threshold=0.1))])
                              # ('clustering', AgglomerativeClustering(n_clusters=20))])
                              # ('clustering', DBSCAN(eps=3, min_samples=5))])
                               ('clustering', KMeans(n_clusters=20))])
        self.classifier = Pipeline([('scaler', StandardScaler()),
                                   # ('classification', LogisticRegression(C=10000))]) # eps = -0.05; k = 10
                                   # ('classification', LinearSVC())])
                                   # ('classification', KNeighborsClassifier())])
                                   # ('classification', BernoulliNB(alpha=0.5))]) # eps = 0.5; k = 5
                                    ('classification', DecisionTreeClassifier(criterion='entropy'))])
        self.check_functions = []
        self.parameters = []
        self.T = time.time()
        
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
        ext = segments[param['i']].split('.')
        if len(ext) > 1:
            if ext[-1].lower() == param['ext']:
       # if re.search('\.' + param['ext'] + '$', segments[param['i']]) is not None:
                return True
        return False
    
    def _segment_ext_substr_09(self, segments, param):
        if len(segments) <= param['i']:
            return False
        pos = segments[param['i']].find('?')
        if pos != -1:
            segments[param['i']] = segments[param['i']][:pos]
        ext = segments[param['i']].split('.')
        if len(ext) > 1:
            if ext[-1].lower() == param['ext'] and re.search('[^\d]+\d+[^\d]+$', segments[param['i']]) is not None:
       # if re.search('\.' + param['ext'] + '$', segments[param['i']]) is not None and re.search('[^\d]+\d+[^\d]+$', segments[param['i']]) is not None:
                return True
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
            
    def _segment_2points(self, segments, param):
        if len(segments) <= param['i']:
            return False
        pos = segments[param['i']].find('?')
        if pos != -1:
            segments[param['i']] = segments[param['i']][:pos]
        wik = segments[param['i']].split(':')
        if len(wik) != 1:# and wik[0] == param['wik']:
            return True
        else:
            return False
            
    def _segment_strix(self, segments, param):
        if len(segments) <= param['i']:
            return False
        pos = segments[param['i']].find('?')
        if pos != -1:
            segments[param['i']] = segments[param['i']][:pos]
        strix = segments[param['i']].split('_')
        if param['strix'] == len(strix):
            return True
        else:
            return False
            
    def _segment_strix_quote(self, segments, param):
        if len(segments) <= param['i']:
            return False
        pos = segments[param['i']].find('?')
        if pos != -1:
            segments[param['i']] = segments[param['i']][:pos]
        strix = segments[param['i']].split('_')
        if len(strix) == 0:
            return False
        if ',' in strix[0]:
            return True
        else:
            return False
            
    def _segment_smile(self, segments, param):
        if len(segments) <= param['i']:
            return False
        pos = segments[param['i']].find('?')
        if pos != -1:
            segments[param['i']] = segments[param['i']][:pos]
        if '(' in segments[param['i']]:
            return True
        else:
            return False
            
    def _segment_ru(self, segments, param):
        if len(segments) <= param['i']:
            return False
        pos = segments[param['i']].find('?')
        if pos != -1:
            segments[param['i']] = segments[param['i']][:pos]
        if re.search('[А-Яа-я]', segments[param['i']]) is not None:
            return True
        else:
            return False
            
    def _segment_in_br(self, segments, param):
        if len(segments) <= param['i']:
            return False
        pos = segments[param['i']].find('?')
        if pos != -1:
            segments[param['i']] = segments[param['i']][:pos]
        m = re.search('\((.*)\)', segments[param['i']])
        if m is not None:
            data = m.groups()[0].split('_')
            if len(data) == param['data']:
                return True
        return False
            
    def _segment_defis(self, segments, param):
        if len(segments) <= param['i']:
            return False
        pos = segments[param['i']].find('?')
        if pos != -1:
            segments[param['i']] = segments[param['i']][:pos]
        if '-' in segments[param['i']]:
            return True
        else:
            return False
            
    def _segment_start_dig(self, segments, param):
        if len(segments) <= param['i']:
            return False
        pos = segments[param['i']].find('?')
        if pos != -1:
            segments[param['i']] = segments[param['i']][:pos]
        if re.match('[0-9]+', segments[param['i']]):
            return True
        else:
            return False
            
    def _segment_more(self, segments, param):
        if len(segments) <= param['i']:
            return False
        pos = segments[param['i']].find('?')
        if pos != -1:
            segments[param['i']] = segments[param['i']][:pos]
        if len(segments[param['i']]) > 15:
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
        m = re.match('segment_substr\[0\-9\]_([0-9]+):1$', feature)
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
        m = re.match('segment_2points_([0-9]+):1$', feature)
        if m is not None:
            return self._segment_2points, {'i': int(m.groups()[0])}
        m = re.match('segment_strix_([0-9]+):([0-9]+)$', feature)
        if m is not None:
            return self._segment_strix, {'i': int(m.groups()[0]), 'strix': int(m.groups()[1])}
        m = re.match('segment_strix_quote_([0-9]+):1$', feature)
        if m is not None:
            return self._segment_strix_quote, {'i': int(m.groups()[0])}
        m = re.match('segment_smile_([0-9]+):1$', feature)
        if m is not None:
            return self._segment_smile, {'i': int(m.groups()[0])}
        m = re.match('segment_ru_([0-9]+):1$', feature)
        if m is not None:
            return self._segment_ru, {'i': int(m.groups()[0])}
        m = re.match('segment_in_br_([0-9]+):(.*)$', feature)
        if m is not None:
            return self._segment_in_br, {'i': int(m.groups()[0]), 'data': int(m.groups()[1])}
        m = re.match('segment_defis_([0-9]+):1$', feature)
        if m is not None:
            return self._segment_defis, {'i': int(m.groups()[0])}
        m = re.match('segment_start_dig_([0-9]+):1$', feature)
        if m is not None:
            return self._segment_start_dig, {'i': int(m.groups()[0])}
        m = re.match('segment_more_([0-9]+):1$', feature)
        if m is not None:
            return self._segment_more, {'i': int(m.groups()[0])}
        #print('ooops', feature)
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
        if segments[-1] == '\n' or segments[-1] == '':
            del segments[-1]
        elif segments[-1][-1] == '\n':
            segments[-1] = segments[-1][:-1]
        for i in range(len(segments)):
            try:
                segments[i] = urllib.unquote(segments[i]).decode('utf8')
            except UnicodeDecodeError:
                try:
                    segments[i] = urllib.unquote(segments[i]).decode('cp1251')
                except UnicodeDecodeError:
                    pass
        for i in range(N):
            X[0, i] = self.check_functions[i](segments, self.parameters[i])
        return X
        
    def extract_features(self, URLS):
        result = Counter()
        X_ = {}
        for line in URLS:
            X_[line] = []
            segments = line.split('/')[3:]
            if segments[-1] == '\n' or segments[-1] == '':
                del segments[-1]
            elif segments[-1][-1] == '\n':
                segments[-1] = segments[-1][:-1]
            result['segments:' + str(len(segments))] += 1
            X_[line].append('segments:' + str(len(segments)))
            if (len(segments) == 0):
                continue
            for i in range(len(segments)):
                segment = segments[i]
                try:
                    segment = urllib.unquote(segment).decode('utf8')
                except UnicodeDecodeError:
                    try:
                        segment = urllib.unquote(segment).decode('cp1251')
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
                    result['segment_ext_' + str(i) + ':' + ext[-1].lower()] += 1
                    X_[line].append('segment_ext_' + str(i) + ':' + ext[-1].lower())
                if len(ext) > 1 and re.search('[^\d]+\d+[^\d]+$', segment) is not None:
                    result['segment_ext_substr[0-9]_' + str(i) + ':' + ext[-1].lower()] += 1
                    X_[line].append('segment_ext_substr[0-9]_' + str(i) + ':' + ext[-1].lower())
                wik = segment.split(':')
                if len(wik) != 1:
                    #result['segment_2points_' + str(i) + ':' + wik[0]] += 1
                    #X_[line].append('segment_2points_' + str(i) + ':' + wik[0])
                    result['segment_2points_' + str(i) + ':1'] += 1
                    X_[line].append('segment_2points_' + str(i) + ':1')
                strix = segment.split('_')
                if len(strix) > 1:
                    result['segment_strix_' + str(i) + ':' + str(len(strix))] += 1
                    X_[line].append('segment_strix_' + str(i) + ':' + str(len(strix)))
                if len(strix) > 0:
                    if ',' in strix[0]:
                        result['segment_strix_quote_' + str(i) + ':1'] += 1
                        X_[line].append('segment_strix_quote_' + str(i) + ':1')
                result['segment_len_' + str(i) + ':' + str(len(segment))] += 1
                X_[line].append('segment_len_' + str(i) + ':' + str(len(segment)))
                if '(' in segment:
                    result['segment_smile_' + str(i) + ':1'] += 1
                    X_[line].append('segment_smile_' + str(i) + ':1')
                m = re.search('\((.*)\)', segment)
                if m is not None:
                    data = m.groups()[0].split('_')
                    result['segment_in_br_' + str(i) + ':' + str(len(data))] += 1
                    X_[line].append('segment_in_br_' + str(i) + ':' + str(len(data)))
                if re.search('[А-Яа-я]', segment) is not None:
                    result['segment_ru_' + str(i) + ':1'] += 1
                    X_[line].append('segment_ru_' + str(i) + ':1')
          #      if '-' in segment:
          #          result['segment_defis_' + str(i) + ':1'] += 1
          #          X_[line].append('segment_defis_' + str(i) + ':1')
          #      if re.match('[0-9]+', segment):
          #          result['segment_start_dig_' + str(i) + ':1'] += 1
          #          X_[line].append('segment_start_dig_' + str(i) + ':1')
                if len(segment) > 15:
                    result['segment_more_' + str(i) + ':1'] += 1
                    X_[line].append('segment_more_' + str(i) + ':1')
    
        for key in result.keys():
            if result[key] > 100:
                self.keys.append(key)
        self.init_functions(self.keys)
       # print self.keys
        X = np.zeros((len(URLS), len(self.keys)))
        for j, url in enumerate(URLS):
            X[j, :] = self.check_url(url)
            '''
            for i, key in enumerate(self.keys):
                if (key in X_[url]) != X[j, i]:
                    print('fuck', key, url, X[j, i], key in X_[url])
            '''
        return X
        
    def fit_model(self, QLINK_URLS, UNKNOWN_URLS, QUOTA):
        self.__init__()
        URLS = QLINK_URLS + UNKNOWN_URLS
        X = self.extract_features(URLS)
        y = np.zeros((len(QLINK_URLS) + len(UNKNOWN_URLS)))
        y[:len(QLINK_URLS)] = 1
        clusters = self.model.fit_predict(X)
        self.classifier.fit(X, y)
        self.un_clusters, counts = np.unique(clusters, return_counts=True)
        #print counts, self.keys
        eps = -0.09
        Delta = 20
        dupl = 1
        a = 0
        b = 0
        k = 10
        zero = 0
        if self.classifier.score(X, y) < 0.7:
            k = 1.7
            eps = 0.27
        for cluster, count in np.dstack((self.un_clusters, counts))[0]:
            self.proba[cluster] = np.min((np.max((np.sum(y[clusters == cluster]) / count - eps, 0)), 1))
            self.is_taken[cluster] = 0
            #self.quota[cluster] = np.ceil(QUOTA * np.sum(y[clusters == cluster]) / len(QLINK_URLS))
            min_quota = QUOTA / len(QLINK_URLS) * k
            #self.quota[cluster] = np.ceil(k * np.sum(y[clusters == cluster]) + (QUOTA - k * np.sum(y)) * np.sum(1 - y[clusters == cluster]) / np.sum(1 - y))
            self.quota[cluster] = min_quota * np.sum(y[clusters == cluster]) + 100
            self.cluster_expressions_help[cluster] = np.mean(X[clusters == cluster], axis=0) > 0.5
            self.cluster_expressions[cluster] = np.zeros(len(self.cluster_expressions_help[cluster]))
            self.cluster_expressions[cluster][self.cluster_expressions_help[cluster]] = 1
            self.delta[cluster] = np.ceil(np.sum(np.abs(np.mean(X[clusters == cluster], axis=0) - self.cluster_expressions[cluster]))) + Delta
            self.part[cluster] = np.sum(y[clusters == cluster]) / np.sum(y)
            self.bad_part[cluster] = np.sum(1 - y[clusters == cluster]) / np.sum(1 - y)
            if self.proba[cluster] < 0.01:
                a += 1
            if np.sum(y[clusters == cluster]) == 0:
                zero += count
        #print a
        #print self.classifier.score(X, y)
        if zero > 300:
            #print "here"
            for cluster in self.un_clusters:
                self.quota[cluster] = self.quota[cluster] + 1400
                self.proba[cluster] = np.min((np.max((self.proba[cluster] + 0.35, 0)), 1))
        '''
        elif zero > 200:
            #print "here"
            for cluster in self.un_clusters:
                self.quota[cluster] = self.quota[cluster] + 1000
                self.proba[cluster] = np.min((np.max((self.proba[cluster] + 1, 0)), 1))
        elif a > 300:
            for cluster in self.un_clusters:
                self.quota[cluster] = self.quota[cluster] + 1000
                self.proba[cluster] = np.min((np.max((self.proba[cluster] + 1, 0)), 1))
        '''
        self.T = 0
        self.cluster_expressions_ = np.zeros((len(self.un_clusters), len(self.keys)))
        for i in range(len(self.un_clusters)):
            self.cluster_expressions_[i, :] = self.cluster_expressions[self.un_clusters[i]]
        #print self.proba
        
    def predict_cluster(self, X):
        Dist = len(self.cluster_expressions.keys())
        cl = -1
        nums = np.sum(X != self.cluster_expressions_, axis=1)
        ind = np.argmin(nums)
        cl = self.un_clusters[ind]
        Dist = nums[ind]
        if Dist <= self.delta[cl]:
            return cl
        return -1
        
    def predict_fetch(self, url):
        X = self.check_url(url) # ~1-3-4s
        fetch = self.classifier.predict(X) # ~3-7-7s
        y = self.predict_cluster(X) # ~1-2-2
        if fetch:
            if y != -1:
                self.is_taken[y] += 1
            return True
        if y == -1:
            return False
        fetch = np.random.choice((True, False), p=(self.proba[y], 1 - self.proba[y]))
        if fetch and self.is_taken[y] < self.quota[y]:
            self.is_taken[y] += 1
            return True
        return False
        
                    
sekitei = Sekitei()

def define_segments(QLINK_URLS, UNKNOWN_URLS, QUOTA):
    sekitei.fit_model(QLINK_URLS, UNKNOWN_URLS, QUOTA)


#
# returns True if need to fetch url
#
def fetch_url(url):
    #global sekitei
    #return sekitei.fetch_url(url);
    res = sekitei.predict_fetch(url)
    '''
    sekitei.j += 1
    if res:
        sekitei.i += 1
    if sekitei.i == 9999 or sekitei.j == 20999:
        print sekitei.T 
    '''
    return res
    
