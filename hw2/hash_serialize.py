import struct
import mmap

def serialize(file_name, positions_sizes):
    fmt = 'qQI'
    N = max(1, (len(positions_sizes) * struct.calcsize(fmt)) // 2 ** 15)
    baskets = [[]] * N
    for h, tup in positions_sizes.items():
        baskets[h % N].append((h, tup[0], tup[1]))
        
    with open(file_name, 'wb') as f:
        f.write(struct.pack('I', N))
        pos = 0
        for basket in baskets:
            f.write(struct.pack('II', pos, len(basket)))
            pos += len(basket)
        dt = 0
        for basket in baskets:
            basket.sort()
            buf = bytes()
            for term in basket:
                buf += struct.pack(fmt, *term)
            f.write(buf)
       
       
s_size = struct.calcsize('I')
basket_info_size = struct.calcsize('II')
item_size = struct.calcsize('qQI')
                
def find_term(file_name, word):
    with open(file_name, 'rb') as f:
        N = struct.unpack('I', f.read(s_size))[0]
        basket_i = word % N
        f.seek(basket_i * basket_info_size, 1)
        pos, num = struct.unpack('II', f.read(basket_info_size))
        basket_data = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
        return bin_search(word, basket_data, num, s_size + N * basket_info_size + pos * item_size)
        
def bin_search(word, basket_data, num, offset):
    left = 0
    right = num
    while left < right:
        mid = (left + right) // 2
        cur = struct.unpack_from('qQI', basket_data, mid * item_size + offset)
        if word < cur[0]:
            right = mid
        elif word > cur[0]:
            left = mid + 1
        else:
            return (cur[1], cur[2])
    
    return None
