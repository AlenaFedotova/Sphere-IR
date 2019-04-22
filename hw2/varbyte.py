from bitarray import bitarray

def varbyte_code(n):
    b = str(bin(n))[2:]
    parts = varbyte_split_by_len(b, 7)
    return ''.join(parts)
    
def varbyte_split_by_len(s, step):
    res = []
    Fill = step - (len(s) + 1) % step + 1
    s = '0' * Fill + s
    while(True):
        if len(s) > step:
            res.append('0' + s[:step])
            s = s[step:]
        else:
            res.append('1' + s) 
            break
    return res
    
def varbyte_code_list(nums):
    res = bitarray()
    for n in nums:
        res.extend(varbyte_code(n))
    return res


def varbyte_decode_list(arr):
    arr = str(arr)[10:-2]
    parts = ''
    res = []
    for i in xrange(0, len(arr), 8):
        s = arr[i:i + 8]
        parts += s[1:]
        if s[0] == '1':
            res.append(int(parts, base=2))
            parts = ''
    return res
