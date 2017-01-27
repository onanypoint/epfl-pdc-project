#!/usr/bin/env python

import pyaudio
import argparse
from settings import *
from helper import *
from encoder import *
from modulation import *


p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=Fs, output=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True,
                        help="Input message file")

    message = "One morning, when Gregor Samsa woke from troubled dreams"

    args = parser.parse_args()
    
    with open(args.input, 'r') as f:
        lines = f.read()
        f.close

    if lines and len(lines) > 0:
        message = lines

    try:
        print()

        print("Message : \n")
        print(message)

        data = encode_data(message)
        sig = prepare_signal(data)

        stream.start_stream()
        stream.write(sig.astype(np.float32))

        stream.stop_stream()
        stream.close()
        p.terminate()

    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        p.terminate()
