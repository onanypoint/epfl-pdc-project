from settings import *
from helper import *
import itertools

def get_freq_dict(fsk_n, Fc, Fdev):
    binary = list(itertools.product([0, 1], repeat=fsk_n))
    freq = [x*Fdev + Fc for x in range(-fsk_n, fsk_n+1) if x != 0]
    return {b:freq[i] for i,b in enumerate(binary)}

def fsk_freq(binary_list, fsk_n, Fs, Fbit, Fc, Fdev):
    m = np.zeros(0).astype(float)
    freq = get_freq_dict(fsk_n, Fc, Fdev)
    
    for bit in chunks(binary_list, fsk_n):
        m = np.hstack((m, np.multiply(np.ones(int(Fs/Fbit)), freq[tuple(bit)])))
            
    return m

def fsk_modulation(freq_list, A, Fs, Fbit):
    
    def sinusoidal(A, freq_list, time_list):
        y = np.zeros(0)
        y = A * np.sin(2*np.pi*np.multiply(freq_list, time_list))
        return y

    time_list = np.arange(0, len(freq_list)/float(Fs), 1/float(Fs), dtype=np.float)

    return sinusoidal(A, freq_list, time_list), time_list

def fsk_demodulation(chunk, fsk_n, Fs, Fc, Fdev):
    fft_samples = fft(chunk)
    freq = get_freq_dict(fsk_n, Fc, Fdev)
    
    freq_list = freq.values()
    key_list = list(freq.keys())
    
    mag = [content_at_freq(fft_samples, freq, Fs, len(chunk)) for freq in freq_list]
    if mag == [-1 for _ in range(len(key_list))]:
        return [-1 for _ in range(fsk_n)]
    else:
        return list(key_list[mag.index(max(mag))])

def get_start_signal():
    return np.asarray([START_FREQ for _ in range(LENGTH_START*int(Fs/Fbit))])

def get_sync_signal():
    return fsk_freq(BARKER, 1, Fs, Fbit, Fc, Fdev)

def prepare_signal(data, debug=False):
    start_signal = get_start_signal()
    sync_signal = get_sync_signal()
    
    data_signal = fsk_freq(data, 2, Fs, Fbit, Fc, Fdev)

    sig_freq = np.concatenate([start_signal, sync_signal, data_signal])
    sig, t = fsk_modulation(sig_freq, A, Fs, Fbit)
    
    print("Time needed", round(len(sig_freq) * (1 / float(Fs))), "sec")
    
    if debug:
        return sig, t, sig_freq
    else:
        return sig

def synchronise_signal(chunks_buffer):
    sync_freq = get_sync_signal()
    sync_signal, t = fsk_modulation(sync_freq, A, Fs, Fbit)
    sync_with_pad = np.hstack((sync_signal, np.zeros(chunks_buffer.size-sync_signal.size)))
    ccf = np.abs(np.fft.ifft(np.fft.fft(chunks_buffer) * np.conj(np.fft.fft(sync_with_pad))))
    index_sync = np.argmax(ccf)
    return index_sync

