import subprocess
import numpy

def load(path, hz=8000):
    """
    Read webm opus file, return numpy array of uint8 values.
    
    Other relevant ffmpeg filters:
    ... bandreject  Apply a two-pole Butterworth band-reject filter.
    ... bass        Boost or cut lower frequencies.
    ... compand     Compress or expand audio dynamic range.
    ... dynaudnorm  Dynamic Audio Normalizer. https://ffmpeg.org/ffmpeg-filters.html#dynaudnorm

    """
    out = subprocess.check_output([
        'ffmpeg',
        '-i', path,
        '-f', 'u8', # unsigned 8-bit output
        '-ar', str(hz), # resample
        '-af', 'dynaudnorm=f=50',
        'pipe:1' # write to stdout
        ])
    return numpy.fromstring(out, dtype=numpy.uint8)


if __name__ == '__main__':
    for x in load('sounds/incoming/sound-1488959248054.webm')[::200]:
        print '*' * abs(x-128)
