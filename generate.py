import hashlib

import numpy as np

from itertools import product

import pickle,gzip

from Crypto.Hash import MD2

chars = list('abcdefghijklmnpqrstvwxyz!? ')

def hashing(chars):
  A = 179424691 # 大きな素数1
  B = 15485867 # 大きな素数2
  C = 32416187567 # 大きな素数3
  hash = 105733 # 初期値の素数
  for char in chars:
    hash = hash*A ^ ord(char)*B # XOEを計算する
  return hash%C

pairs = []
for p in product(chars, repeat=4):
  strings = ''.join(p)
  hash  = hashing(strings)
  hash  = (f'{hash:09d}')
  #print(hash)
  pairs.append( (strings, hash) )

pairs = gzip.compress(pickle.dumps(pairs))
open('pairs.pkl.gz', 'wb').write( pairs )
