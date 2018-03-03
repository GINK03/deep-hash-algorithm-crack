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
from keras.callbacks       import Callback
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
index_char = { index:char for index, char in enumerate(list('abcdefghijklmnpqrstvwxyz!? ')) } 

inputs      = Input(shape=(4, len(char_index)) ) 
encoded     = Bi(GRU(512, activation='relu', return_sequences=True))(inputs)
encoded     = Flatten()(encoded)
encoded     = Dense(5000, activation='relu')(encoded)
encoded     = Dense(5000, activation='relu')(encoded)
encoded     = Dense(1, activation='linear')(encoded)


spectre = Model(inputs, encoded)
spectre.compile(optimizer=Adam(), loss='mae')

buff = None
def callback(epoch, logs):
  global buff
  buff = copy.copy(logs)
batch_callback = LambdaCallback(on_epoch_end=lambda batch,logs: callback(batch,logs) )

if '--train' in sys.argv:
  for name in Path('./data').glob('*'):
    Xs,Ys, Xst, Yst = pickle.loads(gzip.decompress(name.open('rb').read()))
    print('start to fit') 

    init_rate = 0.0005
    decay     = 0.01
    for i in range(100):
      lr = init_rate*(1.0 - decay*i)
      print(f'lr={lr:0.09f}')
      spectre.optimizer = Adam(lr=0.0005) 
      spectre.fit(Xs, Ys, shuffle=True, batch_size=1000, epochs=1, validation_data=(Xst, Yst), callbacks=[batch_callback])
      loss, val_loss = buff['loss'], buff['val_loss']
      spectre.save_weights(f'models/{val_loss:0.09f}_{loss:0.09f}_{i:09d}.h5')

if '--predict' in sys.argv:
  model = sorted(Path('./models').glob('*')).pop(0)
  model = f'{model}'
  print(model)
  spectre.load_weights(model)
  Xs,Ys, Xst, Yst = pickle.loads(gzip.decompress(open('./data/data_000000000.pkl.gz', 'rb').read()))

  yps = spectre.predict(Xst)
  for xt, yr, yp in zip(Xst.tolist(), Yst.tolist(), [y.pop() for y in yps.tolist()]):
    xt = ' '.join( [ index_char[np.argmax(x)] for x in xt ] )
    print(f'input={xt}, real={yr}, predict={yp}')

