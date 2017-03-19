"""
Read audio files, output model weights file.
"""
from __future__ import division
import os, json
import numpy
from twisted.python.filepath import FilePath
import keras.callbacks
import keras.optimizers
from keras.utils import np_utils
from python_speech_features import mfcc

from loader import load
from soundsdir import soundFields
import audiotransform
import speechmodel

def findSounds(words):
    # incomplete, no user filtering
    top = FilePath('sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/will')
    for p in sorted(top.walk()):
        if p.isfile():
            word = soundFields(p.path)['word']
            yield p.path

def sampleSet1():
    return [
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/it/1489522177647.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/it/1489522238741.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/i/1489522116257.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/i/1489522328266.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/going/1489522088184.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/going/1489522204611.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/be/1489522202388.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/be/1489522083075.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/and/1489522113166.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/and/1489522156503.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/and/1489522192902.webm',
        'sounds/incoming/13EubbAsOYgy3eZX4LAHsB5Hzq72/and/1489522247265.webm',
        ]

def sampleSet2():
    return ['sounds/'+p for p in [
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805356819.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805384231.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805398430.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805410225.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805456050.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805480864.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805491211.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805503362.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805514880.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805526988.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805537293.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805549510.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806733030.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806716099.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806698135.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806681162.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806766001.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806780909.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806797739.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806813936.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806831312.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806845887.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806859212.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806878042.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806900746.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806920774.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806345279.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806374091.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806392615.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806410387.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806437045.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806448131.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806461334.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806479076.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806502267.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806527054.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806548987.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806566110.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805356819.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805370426.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805384231.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805398430.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805410225.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805421422.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805456050.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805480864.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805491211.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805503362.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805514880.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805526988.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805537293.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/5th/1489805549510.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/am/1489805352986.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/am/1489805367192.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/am/1489805380510.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/am/1489805393151.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/am/1489805407197.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/am/1489805418261.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/am/1489805451676.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/am/1489805475152.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/am/1489805488619.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/am/1489805501036.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/am/1489805510568.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/am/1489805523130.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/am/1489805534286.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/am/1489805546827.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/and/1489806687785.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/and/1489806703474.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/and/1489806720570.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/and/1489806737453.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/and/1489806752325.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/and/1489806771021.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/and/1489806785778.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/and/1489806803169.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/and/1489806818209.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/and/1489806835898.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/and/1489806850489.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/and/1489806863645.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/and/1489806885641.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/and/1489806905888.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/and/1489806924720.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489805947801.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489805948814.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489805997694.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489805998438.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489806017208.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489806018099.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489806034938.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489806046309.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489806048205.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489806067410.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489806069422.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489806088501.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489806089580.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489806111225.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489806112364.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489806129146.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489806130340.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489806166288.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489806167330.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489806193261.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489806195702.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489806217841.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/chocolate/1489806228890.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806681162.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806698135.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806716099.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806733030.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806766001.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806748208.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806780909.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806797739.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806813936.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806831312.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806845887.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806859212.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806878042.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806900746.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/color/1489806920774.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489805935164.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489805936852.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489805952333.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489805985375.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489805986216.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489806000795.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489806006976.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489806020917.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489806023915.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489806036197.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489806039157.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489806051208.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489806056383.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489806075643.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489806079769.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489806096997.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489806099316.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489806114948.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489806117877.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489806152742.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489806153945.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489806177298.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489806180699.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489806208871.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489806221639.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/do/1489806233001.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/favorite/1489806679095.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/favorite/1489806696236.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/favorite/1489806714622.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/favorite/1489806731364.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/favorite/1489806745585.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/favorite/1489806764071.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/favorite/1489806779325.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/favorite/1489806795240.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/favorite/1489806811776.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/favorite/1489806829085.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/favorite/1489806843828.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/favorite/1489806857373.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/favorite/1489806875514.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/favorite/1489806897128.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/favorite/1489806911450.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/favorite/1489806918556.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806345279.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806347427.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806374091.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806375232.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806392615.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806410387.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806424797.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806437045.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806448131.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806461334.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806479076.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806502267.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806527054.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806548987.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/friend/1489806566110.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/grade/1489805385978.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/grade/1489805400334.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/grade/1489805411721.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/grade/1489805446563.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/grade/1489805482967.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/grade/1489805493008.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/grade/1489805506095.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/grade/1489805517008.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/grade/1489805528437.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/grade/1489805539476.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/hi/1489805072694.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/hi/1489805084831.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/hi/1489805109791.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/hi/1489805133365.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/hi/1489805148200.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/hi/1489805161897.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/hi/1489805191579.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/hi/1489805211790.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/hi/1489805226721.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/hi/1489805244983.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/hi/1489805255129.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/hi/1489805264866.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805350146.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805364955.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805378931.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805391156.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805405605.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805416273.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805450162.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805473300.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805486656.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805499049.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805508654.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805520514.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805533078.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805545314.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805648619.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805658644.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805667598.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805676066.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805684248.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805693768.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805703956.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805715007.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805724688.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805734967.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805745247.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489805757786.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489806326479.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489806327349.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489806361693.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489806363105.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489806385543.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489806403434.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489806417194.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489806430968.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489806442359.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489806455668.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489806470307.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489806520364.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489806495076.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489806542372.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489806559059.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/i/1489806570987.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/in/1489805355062.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/in/1489805369237.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/in/1489805382136.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/in/1489805396510.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/in/1489805408623.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/in/1489805420323.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/in/1489805453497.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/in/1489805477919.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/in/1489805489745.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/in/1489805502070.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/in/1489805513016.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/in/1489805525130.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/in/1489805535438.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/in/1489805548107.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489805079332.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489805092688.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489805138701.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489805153371.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489805123119.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489805184724.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489805197683.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489805216932.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489805235966.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489805250386.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489805258881.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489805270466.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489806683648.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489806699479.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489806717836.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489806734632.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489806749685.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489806767447.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489806782198.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489806799484.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489806814937.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489806832698.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489806847344.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489806860681.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489806880461.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489806902768.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/is/1489806922074.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/la/1489805655155.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/la/1489805664564.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/la/1489805673149.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/la/1489805680674.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/la/1489805689633.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/la/1489805700104.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/la/1489805709342.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/la/1489805721736.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/la/1489805729939.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/la/1489805741630.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/la/1489805752981.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489805942825.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489805944021.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489805992246.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489805992947.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489806012860.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489806013552.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489806028625.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489806029366.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489806043359.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489806061822.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489806044109.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489806062819.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489806084653.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489806085219.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489806106131.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489806106715.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489806123136.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489806123698.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489806160363.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489806161768.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489806191090.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489806192556.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489806213987.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489806225280.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/like/1489806244125.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/malia/1489805096174.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/malia/1489805127167.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/malia/1489805142542.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/malia/1489805188091.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/malia/1489805220647.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/malia/1489805242525.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/malia/1489805252634.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/malia/1489805262020.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489805074960.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489805087133.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489805111631.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489805135318.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489805149806.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489805166299.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489805193744.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489805213989.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489805230255.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489805247338.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489805256804.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489805266900.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806335834.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806337906.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806370890.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806371491.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806390865.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806408963.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806422675.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806435397.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806446723.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806459583.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806476374.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806500176.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806525185.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806547411.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806563876.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806575336.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806675879.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806694039.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806711905.webm',
        'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806728200.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806743297.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806761070.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806776998.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806792284.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806807530.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806826738.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806841125.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806854455.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806871865.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806894223.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/my/1489806911244.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/name/1489805076938.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/name/1489805089662.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/name/1489805119191.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/name/1489805137113.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/name/1489805151349.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/name/1489805182706.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/name/1489805195808.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/name/1489805215189.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/name/1489805233260.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/name/1489805249167.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/name/1489805257816.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/name/1489805268396.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/purple/1489806689719.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/purple/1489806706560.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/purple/1489806722478.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/purple/1489806739167.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/purple/1489806756296.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/purple/1489806772828.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/purple/1489806787867.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/purple/1489806804959.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/purple/1489806821617.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/purple/1489806837789.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/purple/1489806852256.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/purple/1489806866285.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/purple/1489806887864.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/purple/1489806909025.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/see/1489806332211.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/see/1489806332964.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/see/1489806367923.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/see/1489806368570.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/see/1489806389309.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/see/1489806406857.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/see/1489806420769.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/see/1489806433747.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/see/1489806445346.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/see/1489806457942.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/see/1489806474583.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/see/1489806498383.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/see/1489806523510.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/see/1489806545884.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/see/1489806561850.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/see/1489806573946.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/to/1489805652867.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/to/1489805662207.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/to/1489805670638.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/to/1489805678680.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/to/1489805687323.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/to/1489805696870.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/to/1489805707119.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/to/1489805719414.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/to/1489805727746.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/to/1489805738883.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/to/1489805749932.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/to/1489805760100.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/tomorrow/1489806323279.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/tomorrow/1489806324844.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/tomorrow/1489806351700.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/tomorrow/1489806360119.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/tomorrow/1489806379481.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/tomorrow/1489806398318.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/tomorrow/1489806415431.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/tomorrow/1489806429632.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/tomorrow/1489806440789.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/tomorrow/1489806454027.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/tomorrow/1489806468496.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/tomorrow/1489806493670.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/tomorrow/1489806518633.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/tomorrow/1489806540621.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/tomorrow/1489806557791.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/tomorrow/1489806569305.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/went/1489805650984.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/went/1489805660646.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/went/1489805669096.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/went/1489805677395.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/went/1489805685438.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/went/1489805695443.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/went/1489805705547.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/went/1489805717623.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/went/1489805726429.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/went/1489805736689.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/went/1489805746764.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/went/1489805759026.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/will/1489806329569.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/will/1489806330322.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/will/1489806364907.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/will/1489806365532.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/will/1489806387603.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/will/1489806405309.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/will/1489806418867.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/will/1489806432441.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/will/1489806443586.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/will/1489806456770.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/will/1489806472381.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/will/1489806496785.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/will/1489806522183.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/will/1489806544129.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/will/1489806560528.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/will/1489806572343.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/yellow/1489806686411.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/yellow/1489806701583.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/yellow/1489806719324.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/yellow/1489806736583.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/yellow/1489806751341.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/yellow/1489806769413.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/yellow/1489806784482.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/yellow/1489806801786.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/yellow/1489806816682.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/yellow/1489806834424.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/yellow/1489806849437.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/yellow/1489806862446.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/yellow/1489806884066.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/yellow/1489806904737.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/yellow/1489806923788.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489805938483.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489805941016.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489805989382.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489805990205.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489806009616.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489806010610.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489806026174.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489806026781.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489806039635.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489806041694.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489806058627.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489806059358.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489806081709.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489806082299.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489806101743.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489806102355.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489806119996.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489806120559.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489806156773.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489806157503.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489806187899.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489806188868.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489806211240.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489806223183.webm',
	'incoming/4GGUPEPZYNahAwZpQSG6n4QIR913/you/1489806242188.webm',
    ]]

def train(callback=None, out_weights='weights.h5'):
    reload(audiotransform)
    reload(speechmodel)

    model = speechmodel.makeModel()

    model.compile(loss='mean_squared_error',
                  optimizer=keras.optimizers.RMSprop(lr=0.000004),
                  metrics=['accuracy'])

    paths = []
    words = []
    for p in sampleSet2(): # or findSounds(words)
        try:
            raw = load(p, hz=speechmodel.rate)
            crop = audiotransform.autoCrop(raw, rate=speechmodel.rate)
            audiotransform.randomPad(crop, speechmodel.goalSize) # must not error
            print 'using %s autocropped to %s samples' % (p, len(crop))
        except audiotransform.TooQuiet:
            print '%s too quiet' % p
            continue
        paths.append(p)
        word = soundFields(p)['word']
        if word not in words:
            words.append(word)

    repeat = 2
    x = numpy.zeros((len(paths) * repeat, speechmodel.xWidth), dtype=numpy.float)
    y = numpy.zeros((len(paths) * repeat, speechmodel.embedSize), dtype=numpy.float)

    for row, p in enumerate(paths * repeat):
        audio = load(p, hz=speechmodel.rate)
        audio = audiotransform.autoCrop(audio, rate=speechmodel.rate)
        #audio = audiotransform.rightPad(audio, speechmodel.goalSize)
        audio = audiotransform.randomPad(audio, speechmodel.goalSize, path=p)
        #audio = audiotransform.randomScale(audio)
        m = mfcc(audio, samplerate=speechmodel.rate)
        x[row,:] = m.reshape((1, speechmodel.xWidth))
        y[row,:] = np_utils.to_categorical(words.index(soundFields(p)['word']),
                                           speechmodel.embedSize)
        if callback:
            callback.loaded_sound(row, len(paths) * repeat)

    callbacks = []
    #callbacks.append(keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=1, write_graph=True))
    if callback:
        callbacks.append(callback)

    model.fit(x, y, batch_size=500, epochs=300, validation_split=.3,
              shuffle=True,
              callbacks=callbacks)

    model.save_weights(out_weights)
    with open(out_weights + '.words', 'w') as f:
        f.write(json.dumps(words) + '\n')
    if callback:
        callback.on_save(out_weights, fileSize=os.path.getsize(out_weights))

if __name__ == '__main__':
    train()
