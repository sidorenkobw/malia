from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, Activation, Dropout, Flatten, Dense

rate = 8000
goalSize = 18000 # samples after padding
embedSize = 26
numcep = 13
mfccFrames = 2912/numcep  # function of goalSize and mfcc window settings
xWidth = mfccFrames * numcep

def makeModel():
    model = Sequential()
    model.add(Dense(units=100, input_dim=mfccFrames * numcep))
    for d in [1000,1000,1000,100,100,100,100,100,100,100,100,100,embedSize]:
        model.add(Activation('relu'))
        model.add(Dense(units=d))
    model.add(Activation('softmax'))

    return model

