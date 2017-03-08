"""
Read model weights file, accept multiple audio inputs, output text.
"""

from speechmodel import makeModel


class Classifier(object):
    def __init__(self, weights='weights.h5'):
        self.model = makeModel()
        self.model.load_weights(weights)
        
    def classify(self, array):
        return self.model.predict_classes(x=[array.reshape((1, 150, 150, 3))], verbose=0)[0][0]
        # still need to turn this into a word

