import numpy as np

import pickle

import gzip

import random

import math
pairs = pickle.loads(gzip.decompress(open('pairs.pkl.gz', 'rb').read()))
pairs = random.sample(pairs, len(pairs))

char_index = { char:index for index, char in enumerate(list('abcdefghijklmnpqrstvwxyz!? ')) } 
hex_index = { hex:index for index, hex in enumerate(list('0123456789')) }


count, Xs, Ys = 0, [], []
for pair in pairs:
  origin, digest = pair
  x = np.zeros((len(origin), len(char_index)), dtype=float)
  for index, char in enumerate(origin):
    x[index, char_index[char] ] = 1.0
  
  y = 1 / (1 + math.exp(-float(digest)) )

  Xs.append(x)
  Ys.append(y)

  if len(Xs) >= 500000 or len(Ys) >= 500000:
    data = gzip.compress(pickle.dumps((np.array(Xs), np.array(Ys))))
    print(count)
    open(f'data/data_{count:09d}.pkl.gz', 'wb').write( data )
    Xs, Ys = [], []
    count += 1
