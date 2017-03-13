import subprocess
import numpy
from twisted.python.filepath import FilePath
from cachetools import LRUCache

_files = LRUCache(maxsize=100)

def load(path, hz=8000):
    """
    Read webm opus file, return numpy array of uint8 values.
    
    Other relevant ffmpeg filters:
    ... bandreject  Apply a two-pole Butterworth band-reject filter.
    ... bass        Boost or cut lower frequencies.
    ... compand     Compress or expand audio dynamic range.
    ... dynaudnorm  Dynamic Audio Normalizer. https://ffmpeg.org/ffmpeg-filters.html#dynaudnorm

    """
    if isinstance(path, FilePath):
        path = path.path

    if path in _files:
        return _files[path]

    raw = subprocess.check_output([
        'ffmpeg',
        '-loglevel', '0',
        '-i', path,
        '-f', 'u8', # unsigned 8-bit output
        '-ar', str(hz), # resample
        '-af', 'dynaudnorm=f=50',
        'pipe:1' # write to stdout
        ])
    out = numpy.fromstring(raw, dtype=numpy.uint8)
    _files[path] = out
    return out

if __name__ == '__main__':
    for x in load('sounds/incoming/sound-1488959248054.webm')[::200]:
        print '*' * abs(x-128)
