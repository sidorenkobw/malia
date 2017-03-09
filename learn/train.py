"""
Read audio files, output model weights file.


also see
https://github.com/coopie/speech_ml/blob/master/speech_ml/waveform_tools.py numpy code for random padding
"""
import numpy

from speechmodel import makeModel
from loader import load
import keras.callbacks

def train(out_weights='weights.h5'):
    model = makeModel()

    model.compile(loss='mean_squared_error',
                  optimizer='rmsprop',
                  metrics=['accuracy'])
    for lyr in model.layers:
        print lyr.input_shape, lyr.output_shape

    x = numpy.array([load('sounds/incoming/sound-1488957441246.webm')[:100],
                     load('sounds/incoming/sound-1488957653394.webm')[:100],
                     load('sounds/incoming/sound-1488959248054.webm')[:100]])
    y = numpy.array([[1,0,0,0,0,0,0,0,0,0],
                     [0,1,0,0,0,0,0,0,0,0],
                     [1,0,0,0,0,0,0,0,0,0]])

    tb = keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=1, write_graph=True)

    model.fit(x, y,  batch_size=32, nb_epoch=10, validation_split=.34, callbacks=[tb])
    model.save_weights(out_weights)


if __name__ == '__main__':
    train()
