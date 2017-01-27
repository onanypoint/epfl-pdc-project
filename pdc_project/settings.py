import pyaudio

Fc = 10000       #simulate a carrier frequency of 1kHz
Fs = 44100       #sampling frequency for the simulator, must be higher than twice the carrier frequency
Fbit = 10        #simulated bitrate of data
Fdev = 3000      #frequency deviation, make higher than bitrate
A = 12000        #transmitted signal amplitude

START_FREQ = 17000
START_FREQ_THRESHOLD = 100
LENGTH_START = 1
FORWARD_ENCODING_LENGTH = 1
BARKER = [1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]
BARKER = BARKER + BARKER
RESEARCH_WINDOW = 512*5
MARGIN_ERROR_THRESHOLD = 10
SCRAMBLE_KEY = 'z'
WAITING_TIME = 0.1

CHANNELS = 1
FORMAT = pyaudio.paInt16
CHUNK = 1024