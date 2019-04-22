from bitarray import bitarray

mask = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000']
a = [1, 2, 3, 4, 5, 7, 9, 14, 28]
b = [28, 14, 9, 7, 5, 4, 3, 2, 1]
base = [2 ** 28, 2 ** 14, 2 ** 9, 2 ** 7, 2 ** 5, 16, 8, 4, 2]

def try_put(nums, i):
    res = 0
    if len(nums) < a[i]:
        return 0
    while res < len(nums) and nums[res] < base[i] and res < a[i]:
        res += 1
    if res != a[i]:
        return 0
    return res
    
def binary_code(n, base_):
    res = str(bin(n))[2:]
    Fill = base_ - len(res)
    return '0' * Fill + res
    
def really_put(nums, i, n):
    res = ''
    for j in range(n):
        res += binary_code(nums[j], b[i])
    if len(res) != 28:
        res += '0' * (28 - len(res))
    return mask[i] + res

def simple9_code(nums):
    i = 8
    n = try_put(nums, i)
    while n == 0 and i > 0:
        i -= 1
        n = try_put(nums, i) 
    return n, really_put(nums, i, n)
    
def simple9_code_list(nums):
    res = bitarray()
    i = 0
    while i < len(nums):
        n, code = simple9_code(nums[i:])
        i += n
        res.extend(code)
    return res
    
def simple9_decode(s):
    i = 0
    m = s[:4]
    s = s[4:]
    while m != mask[i]:
        i += 1
    res = [None] * a[i]
    for j in range(a[i]):
        part = s[b[i] * j:b[i] * (j + 1)]
        res[j] = int(part, base=2)
    return res
    
def list_to_string(s):
    res = ''
    for b in s:
        if b:
            res += '1'
        else:
            res += '0'
    return res

def simple9_decode_list(arr):
    res = []
    m = 32
    for i in xrange(len(arr) // m):
        s = arr[m * i:m * i + m].tolist()
        s = list_to_string(s)
        res += simple9_decode(s)
    return res
