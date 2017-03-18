"""
Read audio files, weights file, and new speech audio. Output words and confidence.
"""
from __future__ import division
import json
import numpy
from python_speech_features import mfcc

import speechmodel
reload(speechmodel)
import audiotransform
reload(audiotransform)

class Recognizer(object):
    def __init__(self, weightsPath='weights.h5'):
        self.model = speechmodel.makeModel()
        self.model.load_weights(weightsPath)

        self.words = json.load(open(weightsPath + '.words'))

    def recognize(self, newAudio):
        pad = audiotransform.rightPad(newAudio, goalSize=speechmodel.goalSize)
        m = mfcc(pad, samplerate=speechmodel.rate)

        out = self.model.predict(x=m.reshape((1, speechmodel.xWidth)), verbose=1)

        if max(out[0]) < .1:
            return 'no match'
        topPairs = sorted(zip(out[0], self.words), reverse=True)[:3]
        return '; '.join('%s (%.1f)' % (w,s) for s,w in topPairs if s >= .1)
