from settings import *
import numpy as np
import struct

def chunks(l, n):
    for i in range(0, len(l), n):
        data = l[i:i+n]
        if len(data) % n != 0 :
            data = data + [0 for i in range(n - len(data)%n)]
        
        yield data

def pack_buffer(buffer) :
    return ''.join([struct.pack('h', frame) for frame in buffer])

def unpack_buffer(buffer) :
    return struct.unpack('%dh' % (len(buffer)/2), buffer)

def fft(sig) :
    fft = np.abs(np.fft.rfft(sig))
    return fft

def average_power(fft_samples):
    return np.average(fft_samples)

def index_freq(f, Fs, Fbit) :
    return int(round((float(f) / Fs) * int(Fs/Fbit)))

def content_at_freq(fft_sample, f, Fs, Fbit) :
    indexFreqs = [index_freq(f, Fs, int(Fs/Fbit)) for f in range(f - 100, f + 100, 5)]
    freqSample = max([fft_sample[index] for index in indexFreqs])
    if freqSample > average_power(fft_sample) + MARGIN_ERROR_THRESHOLD :
        return freqSample
    else :
        return -1