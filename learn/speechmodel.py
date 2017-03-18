from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, Activation, Dropout, Flatten, Dense

def makeModel():
    model = Sequential()
    model.add(Dense(units=64, input_dim=30000))
    for d in [64,10]:
        model.add(Activation('relu'))
        model.add(Dense(units=d))
    model.add(Activation('softmax'))

    return model

