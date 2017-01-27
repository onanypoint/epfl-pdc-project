from settings import *
import numpy as np
from helper import *

def encode(string):
    binary = bin(int.from_bytes(string.encode(), 'big'))
    return [0] + [int(d) for d in str(binary)[2:]]

def decode(binary_list):
    n = int("0b"+"".join([ str(c) for c in binary_list]), 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

def scramble(binary_list, key):
    return [v ^ key[i % len(key)] for i,v in enumerate(binary_list)]

def unscramble(binary_list, key):
    return scramble(binary_list, key)

def forward_encode(data, n) :
    return [bit for bit in data for i in range(n)]

def forward_decode(data, n) :
    return [1 if np.mean(chunk) >= 0.5 else 0 for chunk in chunks(data, n)] 
    
error_control_encode = forward_encode
error_control_decode = forward_decode

def encode_data(message):
    message = message.lower()
    data = encode(message)
    data = forward_encode(data, FORWARD_ENCODING_LENGTH)
    data = scramble(data, encode(SCRAMBLE_KEY))
    return data

def decode_data(bits):
    bits = unscramble(bits, encode(SCRAMBLE_KEY))
    bits = forward_decode(bits, FORWARD_ENCODING_LENGTH)
    try:
        message = decode(bits)
        return message
    except:
        return "?"
