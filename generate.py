import hashlib

import numpy as np

from itertools import product

import pickle,gzip

from Crypto.Hash import MD2

chars = list('abcdefghijklmnpqrstvwxyz!? ')

def hashing(chars):
  A = 54059
  B = 76963
  C = 86969
  hash = 37
  for char in chars:
    hash = hash*A ^ ord(char)*B
  return hash%C

pairs = []
for p in product(chars, repeat=5):
  strings = ''.join(p)
  hash  = hashing(strings)
  hash  = (f'{hash:09d}')
  #print(hash)
  pairs.append( (strings, hash) )

pairs = gzip.compress(pickle.dumps(pairs))
open('pairs.pkl.gz', 'wb').write( pairs )
