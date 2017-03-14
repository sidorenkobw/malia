from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, Activation, Dropout, Flatten, Dense

def makeModel():
    model = Sequential()
    model.add(Dense(output_dim=64, input_dim=10000))
    for d in [64,64,32,32,30]:
        model.add(Activation('relu'))
        model.add(Dense(output_dim=d))
    model.add(Activation('softmax'))

    return model

