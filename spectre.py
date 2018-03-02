from keras.layers          import Lambda, Input, Dense, GRU, LSTM, RepeatVector
from keras.models          import Model
from keras.layers.core     import Flatten
from keras.callbacks       import LambdaCallback 
from keras.optimizers      import SGD, RMSprop, Adam
from keras.layers.wrappers import Bidirectional as Bi
from keras.layers.wrappers import TimeDistributed as TD
from keras.layers          import merge, multiply
from keras.layers.merge    import Concatenate as Concat
from keras.regularizers    import l2
from keras.layers.core     import Reshape
from keras.layers.normalization import BatchNormalization as BN
import keras.backend as K
import numpy as np
import random
import sys
import pickle
import gzip
import copy
import os
import re
from pathlib import Path

char_index = { char:index for index, char in enumerate(list('abcdefghijklmnpqrstvwxyz!? ')) } 

inputs      = Input(shape=(5, len(char_index)) ) 
encoded     = Bi(GRU(512, activation='linear', return_sequences=True))(inputs)
encoded     = Dense(200, activation='linear')(encoded)
encoded     = Flatten()(encoded)
encoded     = Dense(200, activation='linear')(encoded)
encoded     = Dense(1, activation='sigmoid')(encoded)


spectre = Model(inputs, encoded)
spectre.compile(optimizer=Adam(), loss='binary_crossentropy')

if '--train' in sys.argv:
  for name in Path('./data').glob('*'):
    Xs,Ys = pickle.loads(gzip.decompress(name.open('rb').read()))
    print('start to fit') 
    spectre.fit(Xs, Ys, shuffle=True, batch_size=1000, epochs=1, validation_split=0.2)

