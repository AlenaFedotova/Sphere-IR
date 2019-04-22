import numpy as np

def fibo(n):
    if n == 1 or n == 2:
        return 1
    return fibo(n - 1) + fibo(n - 2)
    
def find_min(n):
    k = 1
    while fibo(k + 1) <= n:
        k += 1
    return k

def fibo_code(n):
    k = find_min(n)
    s = ''
    while k > 1:
        if n >= fibo(k):
            n -= fibo(k)
            s += '1'
        else:
            s += '0'
        k -= 1
    return s[::-1] + '1'
    

lines = open("./task_1/data").readlines()


res = ''
for s in lines:
    i = int(s)
    code = fibo_code(i)
    #print i
    #print code
    res += code
    
    
print len(res)

truth = open("./task_1/baseline").readlines()[0]
print len(truth)
    
    
diff = []
for i in range(len(res)):
    if res[i] != truth[i]:
        diff.append(i)
        
print diff
print len(diff)
print diff[0], diff[-1]
print sum(diff)
print truth[-1]
    
