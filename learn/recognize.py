"""
Read audio files, weights file, and new speech audio. Output words and confidence.
"""
from __future__ import division
import numpy

import speechmodel
reload(speechmodel)
import audiotransform
reload(audiotransform)

class Recognizer(object):
    def __init__(self, weightsPath='weights.h5'):
        self.model = speechmodel.makeModel()
        self.model.load_weights(weightsPath)

    def recognize(self, newAudio, rate=8000):
        pad = audiotransform.rightPad(newAudio, goalSize=30000)
        out = self.model.predict_classes(x=pad.reshape((1, 30000)), verbose=1)
        return {'out': out.tolist()}
