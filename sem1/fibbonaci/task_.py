import numpy as np

def fibo(n):
    if n == 1 or n == 2:
        return 1
    return fibo(n - 1) + fibo(n - 2)
    
def convert(s):
    res = 0
    #print s
    for i in range(len(s)):
        if s[i] == '1':
             res += fibo(i + 2)
    return res
    
def parse(s):
    res = []
    i = 0
    c = '0'
    for j in range(len(s) - 1):
        if c == '1' and s[j] == '1':
            res.append(convert(s[i:j]))
            c = '0'
            i = j + 1
            j += 1
        else:
            c = s[j]
    return res
    

line = open("./task_2/encoded").readlines()[0]
print line
res = parse(line)

print res
truth = open("./task_2/check_list").readlines()
print truth

i = 0
for n in truth:
    if not int(n) in res:
        print n
        i += 1
    
    
print i, len(res), len(truth)
