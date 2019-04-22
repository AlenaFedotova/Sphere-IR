import varbyte
import simple9
from bitarray import bitarray

def index_write(file_name, index, encoding):
    coder = None
    dumped_index = bitarray()
    if encoding == 'varbyte':
        coder = varbyte.varbyte_code_list
        decoder = varbyte.varbyte_decode_list
    elif encoding == 'simple9':
        coder = simple9.simple9_code_list
        decoder = simple9.simple9_decode_list
    else:
        print 'encoding error'
        return
        
    positions_sizes = {}
    pos = 0

    for word in index.keys():
        arr = coder(index[word])
        dumped_index.extend(arr)
        s = len(arr) / 8
        positions_sizes[word] = (pos, s)
        pos += s
        
        
    with open(file_name, 'wb') as f:
        dumped_index.tofile(f)
    return positions_sizes
    
def index_read(file_name, tup, encoding):
    position, size = tup
    arr = bitarray()
    decoder = None
    if encoding == 'varbyte':
        decoder = varbyte.varbyte_decode_list
    elif encoding == 'simple9':
        decoder = simple9.simple9_decode_list
    with open(file_name, 'rb') as f:
        f.seek(position)
        arr.fromfile(f, size)
    return decoder(arr)
