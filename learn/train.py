"""
Read audio files, output model weights file.


also see
https://github.com/coopie/speech_ml/blob/master/speech_ml/waveform_tools.py numpy code for random padding
"""
import numpy

import speechmodel
from loader import load
import keras.callbacks

def train(callback=None, out_weights='weights.h5'):
    reload(speechmodel)
    model = speechmodel.makeModel()

    model.compile(loss='mean_squared_error',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    x = numpy.array([load('sounds/incoming/sound-1488957441246.webm')[:100],
                     load('sounds/incoming/sound-1488957653394.webm')[:100],
                     load('sounds/incoming/sound-1488959248054.webm')[:100]])
    y = numpy.array([[1,0,0,0,0,0,0,0,0,0],
                     [0,1,0,0,0,0,0,0,0,0],
                     [1,0,0,0,0,0,0,0,0,0]])

    tb = keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=1, write_graph=True)

    callbacks = []
    #callbacks.append(keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=1, write_graph=True))
    if callback:
        callbacks.append(callback)
    
    model.fit(x, y, batch_size=100, nb_epoch=50, validation_split=.34,
              callbacks=callbacks)

    model.fit(x, y,  batch_size=32, nb_epoch=10, validation_split=.34, callbacks=[tb] + ([callback] if callback else []))
    model.save_weights(out_weights)
    if callback:
        callback.on_save(out_weights)


if __name__ == '__main__':
    train()
