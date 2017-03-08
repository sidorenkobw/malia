"""
Read audio files, output model weights file.


also see
https://github.com/coopie/speech_ml/blob/master/speech_ml/waveform_tools.py numpy code for random padding
"""

from speechmodel import makeModel
from loader import load

def train(out_weights='weights.h5'):
    model = makeModel()

    model.compile(loss='mean_squared_error',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    x = [load('sounds/incoming/sound-1488957441246.webm'),
         load('sounds/incoming/sound-1488957653394.webm'),
         load('sounds/incoming/sound-1488959248054.webm')]
    y = ['word1', 'word2', 'word1']
    model.fit(x, y,  batch_size=32, nb_epoch=10, validation_split=.34)
    model.save_weights(out_weights)


if __name__ == '__main__':
    train()
