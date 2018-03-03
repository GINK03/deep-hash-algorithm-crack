import numpy as np

import pickle

import gzip

import random

import math

import statistics

pairs = pickle.loads(gzip.decompress(open('pairs.pkl.gz', 'rb').read()))
pairs = random.sample(pairs, len(pairs))

char_index = { char:index for index, char in enumerate(list('abcdefghijklmnpqrstvwxyz!? ')) } 
hex_index = { hex:index for index, hex in enumerate(list('0123456789')) }

max_ = max( [float(digest) for origin, digest in pairs] )
count, Xs, Ys, Xst, Yst = 0, [], [], [], []
for pair in pairs:
  origin, digest = pair
  x = np.zeros((len(origin), len(char_index)), dtype=float)
  for index, char in enumerate(origin):
    x[index, char_index[char] ] = 1.0
 
  y = float(digest)/max_
  #print(y)

  if random.random() <= 0.8:
    Xs.append(x)
    Ys.append(y)
  else:
    Xst.append(x)
    Yst.append(y)


  if len(Xs) >= 500000 or len(Ys) >= 500000:
    data = gzip.compress(pickle.dumps((np.array(Xs), np.array(Ys), np.array(Xst), np.array(Yst))))
    print(count)
    open(f'data/data_{count:09d}.pkl.gz', 'wb').write( data )
    Xs, Ys = [], []
    count += 1
data = gzip.compress(pickle.dumps((np.array(Xs), np.array(Ys), np.array(Xst), np.array(Yst))))
print(count)
open(f'data/data_{count:09d}.pkl.gz', 'wb').write( data )
count += 1

