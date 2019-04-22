# coding: utf-8

import sys
import re
import random
import urllib
from collections import Counter
# you may add imports if needed (and if they are installed)

def extract_features(INPUT_FILE_1, INPUT_FILE_2, OUTPUT_FILE):
    result = Counter()
    random_lines = random.sample(open(INPUT_FILE_2).readlines(), 2000) + random.sample(open(INPUT_FILE_1).readlines(), 2000)
    for line in random_lines:
        segments = line.split('/')[3:]
        if segments[-1] == '\n':
            del segments[-1]
        else:
            segments[-1] = segments[-1][:-1]
        result['segments:' + str(len(segments))] += 1
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
                    result['param_name:' + p.split('=')[0]] += 1
                segment = mb_par[0]
            result['segment_name_' + str(i) + ':' + segment] += 1
            if segment.isdigit():
                result['segment_[0-9]_' + str(i) + ':1'] += 1
            if re.search('[^\d]+\d+[^\d]+$', segment) is not None:
                result['segment_substr[0-9]_' + str(i) + ':1'] += 1
            ext = segment.split('.')
            if len(ext) > 1:
                result['segment_ext_' + str(i) + ':' + ext[-1]] += 1
            if len(ext) > 1 and re.search('[^\d]+\d+[^\d]+$', segment) is not None:
                result['segment_ext_substr[0-9]_' + str(i) + ':' + ext[-1]] += 1
            result['segment_len_' + str(i) + ':' + str(len(segment))] += 1
    with open(OUTPUT_FILE, 'w') as f:
        for key, value in sorted(result.iteritems(), key=lambda (k,v): (-v,k)):
            if value < 205:
                break
            f.write(key + '\t' + str(value) + '\n')
