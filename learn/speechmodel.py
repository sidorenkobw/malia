from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, Activation, Dropout, Flatten, Dense

rate = 6000
goalSize = 30000 # samples after padding
embedSize = 5
numcep = 13
mfccFrames = 499  # function of goalSize and mfcc window settings
xWidth = mfccFrames * numcep

def makeModel():
    model = Sequential()
    model.add(Dense(units=1000, input_dim=499*13))
    for d in [1000,1000,100,100,100,5]:
        model.add(Activation('relu'))
        model.add(Dense(units=d))
    model.add(Activation('softmax'))

    return model

