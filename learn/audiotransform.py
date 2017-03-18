from __future__ import division
import random
import numpy

class TooQuiet(ValueError):
    pass

def autoCrop(raw, rate=8000, marginSec=.1):
    marginSamples = min(int(len(raw) / 2 - 1), int(marginSec * rate))
    middle = raw[marginSamples:-marginSamples]
    norm = numpy.abs(middle.astype(numpy.float) - 128) / 128.

    quietSample = norm[:100]
    quietThreshold = quietSample.max() + .01
    indicesWithSound = numpy.flatnonzero(norm > quietThreshold)

    if len(indicesWithSound) == 0:
        print 'raw %s middle %s quietThreshold %s' % (
            raw.shape, middle.shape, quietThreshold)
        raise TooQuiet()

    return raw[marginSamples + indicesWithSound[0]:
               marginSamples + indicesWithSound[-1]]

def rightPad(clip, goalSize=20000):
    out = numpy.zeros((goalSize,), dtype=numpy.uint8)
    out[:min(goalSize, len(clip))] = clip[:goalSize]
    return out

def randomPad(clip, goalSize=20000, path='<unknown>'):
    if len(clip) > goalSize:
        print '%s too long (%s), cropping' % (path, len(clip))
        return clip[:goalSize]
    out = numpy.zeros((goalSize,), dtype=numpy.uint8)
    pad = random.randrange(goalSize - len(clip))
    out[pad:pad+len(clip)] = clip
    return out

def randomScale(clip, lo=.2, hi=2):
    scl = lo + random.random() * (hi - lo)
    clip = numpy.clip((clip.astype(numpy.int16) - 128) * scl, -127, 128)
    return (clip + 128).astype(numpy.uint8)
