"""
Read audio files, output model weights file.
"""
from __future__ import division
import os, json
import numpy
from twisted.python.filepath import FilePath
import keras.callbacks
import keras.optimizers
from keras.utils import np_utils
from python_speech_features import mfcc

from loader import load
from soundsdir import soundFields
import audiotransform
import speechmodel

def findSounds(words):
    # incomplete, no user filtering
    top = FilePath('sounds/incoming/')
    for p in sorted(top.walk()):
        if p.isfile():
            word = soundFields(p)['word']
            if word not in words:
                continue
            yield p.path

def sampleSet1():
    return [
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/it/1489522177647.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/it/1489522238741.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/i/1489522116257.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/i/1489522328266.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/going/1489522088184.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/going/1489522204611.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/be/1489522202388.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/be/1489522083075.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/and/1489522113166.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/and/1489522156503.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/and/1489522192902.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/and/1489522247265.webm',
        ]

def sampleSet2():
    return ['sounds/'+p for p in [
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805356819.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805384231.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805398430.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805410225.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805456050.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805480864.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805491211.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805503362.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805514880.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805526988.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805537293.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805549510.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806733030.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806716099.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806698135.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806681162.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806766001.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806780909.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806797739.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806813936.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806831312.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806845887.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806859212.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806878042.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806900746.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806920774.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806345279.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806374091.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806392615.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806410387.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806437045.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806448131.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806461334.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806479076.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806502267.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806527054.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806548987.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806566110.webm',
    ]]

def train(callback=None, out_weights='weights.h5'):
    reload(audiotransform)
    reload(speechmodel)

    model = speechmodel.makeModel()

    model.compile(loss='mean_squared_error',
                  optimizer=keras.optimizers.RMSprop(lr=0.000004),
                  metrics=['accuracy'])

    paths = []
    words = []
    for p in sampleSet2(): # or findSounds(words)
        try:
            raw = load(p, hz=speechmodel.rate)
            crop = audiotransform.autoCrop(raw, rate=speechmodel.rate)
            audiotransform.randomPad(crop, speechmodel.goalSize) # must not error
            print 'using %s autocropped to %s samples' % (p, len(crop))
        except audiotransform.TooQuiet:
            print '%s too quiet' % p
            continue
        paths.append(p)
        word = soundFields(p)['word']
        if word not in words:
            words.append(word)

    repeat = 2
    x = numpy.zeros((len(paths) * repeat, speechmodel.xWidth), dtype=numpy.float)
    y = numpy.zeros((len(paths) * repeat, speechmodel.embedSize), dtype=numpy.float)

    for row, p in enumerate(paths * repeat):
        audio = load(p, hz=speechmodel.rate)
        audio = audiotransform.autoCrop(audio, rate=speechmodel.rate)
        #audio = audiotransform.rightPad(audio, speechmodel.goalSize)
        audio = audiotransform.randomPad(audio, speechmodel.goalSize, path=p)
        #audio = audiotransform.randomScale(audio)
        m = mfcc(audio, samplerate=speechmodel.rate)
        x[row,:] = m.reshape((1, speechmodel.xWidth))
        y[row,:] = np_utils.to_categorical(words.index(soundFields(p)['word']),
                                           speechmodel.embedSize)
        if callback:
            callback.loaded_sound(row, len(paths) * repeat)

    callbacks = []
    #callbacks.append(keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=1, write_graph=True))
    if callback:
        callbacks.append(callback)

    model.fit(x, y, batch_size=500, epochs=300, validation_split=.3,
              shuffle=True,
              callbacks=callbacks)

    model.save_weights(out_weights)
    with open(out_weights + '.words', 'w') as f:
        f.write(json.dumps(words) + '\n')
    if callback:
        callback.on_save(out_weights, fileSize=os.path.getsize(out_weights))

if __name__ == '__main__':
    train()
