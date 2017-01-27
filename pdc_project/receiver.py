#!/usr/bin/env python
import pyaudio
import queue
import time
import sys
import threading
from settings import *
from helper import *
from modulation import *

raw_data = queue.Queue()
unprocessed_chunks = queue.Queue()
unprocessed_bits = queue.Queue()

RUNNING = True


def process_bits():
    global RUNNING

    bits_buffer = []
    string = ""
    while RUNNING:
        try:
            bits_buffer.append(unprocessed_bits.get(False))

            if bits_buffer.count(-1) > 8 * FORWARD_ENCODING_LENGTH - 4:
                print("\nEnd of Transmission")
                RUNNING = False
                break

            if len(bits_buffer) == 8 * FORWARD_ENCODING_LENGTH:
                bits = [bit if bit != -1 else 0 for bit in bits_buffer]

                message = decode_data(bits)
                string += message
                #[sys.stdout.write(str(bit)) for bit in bits_buffer]
                #sys.stdout.write(' : ')
                # sys.stdout.write(message)
                # sys.stdout.write("\n")
                # sys.stdout.flush()
                sys.stdout.write(message)
                sys.stdout.flush()

                bits_buffer = []

        except queue.Empty:
            time.sleep(WAITING_TIME)

    print("\nYour complete message is :")
    print(string)


def process_chunks():
    global RUNNING

    SYNCED = False
    duration = int(Fs / Fbit)
    chunks_buffer = np.empty(shape=(0))

    start_signal = get_start_signal()
    sync_signal = get_sync_signal()

    print(len(start_signal))

    while RUNNING:

        try:
            data = unprocessed_chunks.get(False)
            chunks_buffer = np.concatenate([chunks_buffer, data])

            if not SYNCED and len(chunks_buffer) > len(sync_signal) + len(start_signal) + RESEARCH_WINDOW:
                index_start = synchronise_signal(chunks_buffer)
                if index_start + len(sync_signal) < len(chunks_buffer):
                    chunks_buffer = chunks_buffer[
                        index_start + len(sync_signal):]
                    SYNCED = True
                    print("Sync Done", index_start)

            if SYNCED and len(chunks_buffer) > duration:
                rest = len(chunks_buffer) % duration

                for chunk in chunks(chunks_buffer[:-rest], duration):
                    bits = fsk_demodulation(chunk, 2, Fs, Fc, Fdev)
                    for bit in bits:
                        unprocessed_bits.put(bit)

                chunks_buffer = chunks_buffer[-rest:]

        except queue.Empty:
            time.sleep(WAITING_TIME)


def process_raw():
    global RUNNING

    RECEIVED_START = False
    last_chunk = np.empty(shape=(0))
    while RUNNING:
        try:
            data = raw_data.get(False)

            if not RECEIVED_START:
                fft_sample = fft(data)
                if content_at_freq(fft_sample, START_FREQ, Fs, Fbit) > START_FREQ_THRESHOLD:
                    RECEIVED_START = True
                    unprocessed_chunks.put(last_chunk)
                    print("Transmission!")

            if RECEIVED_START:
                unprocessed_chunks.put(data)

            last_chunk = data

        except queue.Empty:
            time.sleep(WAITING_TIME)


def callback(in_data, frame_count, time_info, status):
    data_unpacked = np.array(unpack_buffer(in_data))
    if float(max(abs(data_unpacked))) != 0:
        data_unpacked = data_unpacked / float(max(abs(data_unpacked)))
        raw_data.put(data_unpacked)
    return (in_data, pyaudio.paContinue)


def analyse_audio():
    global RUNNING
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=Fs,
                    input=True,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback)

    stream.start_stream()

    while stream.is_active() and RUNNING:
        time.sleep(WAITING_TIME)

    stream.stop_stream()
    stream.close()

    p.terminate()


if __name__ == '__main__':
    processes = [process_raw, process_chunks, process_bits]

    for process in processes:
        thread = threading.Thread(target=process)
        thread.daemon = True
        thread.start()

    analyse_audio()
    print("See you soon!")
