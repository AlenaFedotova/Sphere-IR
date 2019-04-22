import pickle
import hash_serialize

N = 0

with open('conf.txt', 'r') as f:
    lines = f.readlines()
    N = int(lines[1])

for i in xrange(N):
    with open('dictionary' + str(i + 1), 'rb') as f:
        positions_sizes = pickle.load(f)
    hash_serialize.serialize('dictionary' + str(i + 1), positions_sizes)

