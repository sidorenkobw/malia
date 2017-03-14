"""
Read audio files, output model weights file.
"""
from __future__ import division
import numpy
from twisted.python.filepath import FilePath

import speechmodel
from loader import load
import keras.callbacks

import audiotransform 

def train(callback=None, out_weights='weights.h5'):
    reload(audiotransform)
    reload(speechmodel)


    words = 'angeles  be  going  los  malia  on  recording  start  to  will add  asdf  click  df  edit  sadf  sdf  text  to  your click  edit test'.split()
    repeat = 20
    goalSize = 10000
    embedSize = 30

    
    model = speechmodel.makeModel()

    model.compile(loss='mean_squared_error',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    top = FilePath('sounds/incoming/')
    paths = []
    for p in sorted(top.walk()):
        if p.isfile():
            try:
                raw = load(p)
                crop = audiotransform.autoCrop(raw, rate=8000)
                padDoesntFail = audiotransform.randomPad(crop, goalSize)
                print 'using %s cropped to %s samples' % (p, len(crop))
            except audiotransform.TooQuiet:
                print '%s too quiet' % p
                continue
            paths.append(p)

    x = numpy.zeros((len(paths) * repeat, goalSize), dtype=numpy.float)
    y = numpy.zeros((len(paths) * repeat, embedSize), dtype=numpy.float)

    def embed(p, embedSize):
        user, word, timestamp = p.path.split('/')[-3:]
        vec = [0] * embedSize
        vec[words.index(word)] = 1
        return vec

    for row, p in enumerate(paths * repeat):
        x[row,:] = audiotransform.randomPad(audiotransform.autoCrop(load(p)),
                                            goalSize, path=p)
        y[row,:] = embed(p, embedSize)
        if callback:
            callback.loaded_sound(row, len(paths) * repeat)

    callbacks = []
    #callbacks.append(keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=1, write_graph=True))
    if callback:
        callbacks.append(callback)

    model.fit(x, y, batch_size=500, nb_epoch=20, validation_split=.03,
              callbacks=callbacks)

    model.save_weights(out_weights)
    if callback:
        callback.on_save(out_weights)


if __name__ == '__main__':
    train()
