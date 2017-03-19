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

        topPairs = [(score, word) for score, word in
                    sorted(zip(out[0], self.words), reverse=True)
                    if score >= .1][:3]
        return {
            'word': topPairs[0][1] if topPairs else None,
            'matches': topPairs,
            'matchDisplay': '; '.join('%s (%.1f)' % (w,s) for s,w in topPairs),
            }
