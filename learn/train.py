"""
Read audio files, output model weights file.


also see
https://github.com/coopie/speech_ml/blob/master/speech_ml/waveform_tools.py numpy code for random padding
"""
import random
import numpy
from twisted.python.filepath import FilePath

import speechmodel
from loader import load
import keras.callbacks


def randomPad(path, goalSize=20000):
    raw = load(path)
    norm = numpy.abs(raw.astype(numpy.float) - 128) / 128.
    quietSample = norm[:100]
    quietThreshold = quietSample.max() + .002
    indicesWithSound = numpy.flatnonzero(norm > quietThreshold)

    out = numpy.zeros((goalSize,), dtype=numpy.float)

    if len(indicesWithSound) == 0:
        print '%s too quiet' % path
        return out
    clip = norm[indicesWithSound[0]:indicesWithSound[-1]]
    if len(clip) > goalSize:
        print '%s too long' % path
        return norm[:goalSize]
    pad = random.randrange(goalSize - len(clip))
    out[pad:pad+len(clip)] = clip
    print '%s padded by %s' % (path, pad)
    return out

def train(callback=None, out_weights='weights.h5'):
    reload(speechmodel)
    model = speechmodel.makeModel()

    model.compile(loss='mean_squared_error',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    top = FilePath('sounds/incoming/test')
    paths = [p for p in sorted(top.walk()) if p.isfile()]
    repeat = 6
    goalSize = 20000
    embedSize = 10

    x = numpy.zeros((len(paths) * repeat, goalSize), dtype=numpy.float)
    y = numpy.zeros((len(paths) * repeat, embedSize), dtype=numpy.float)

    words = ['add', 'click', 'edit', 'text', 'to', 'your']
    def embed(p, embedSize):
        word, _timestamp = p.basename().split('_')
        vec = [0] * embedSize
        vec[words.index(word)] = 1
        return vec

    for row, p in enumerate(paths * repeat):
        x[row,:] = randomPad(p, goalSize)
        y[row,:] = embed(p, embedSize)
        if callback:
            callback.loaded_sound(row, len(paths) * repeat)

    callbacks = []
    #callbacks.append(keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=1, write_graph=True))
    if callback:
        callbacks.append(callback)

    model.fit(x, y, batch_size=100, nb_epoch=50, validation_split=.1,
              callbacks=callbacks)

    model.save_weights(out_weights)
    if callback:
        callback.on_save(out_weights)


if __name__ == '__main__':
    train()
