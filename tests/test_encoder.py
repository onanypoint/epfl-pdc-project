from nose.tools import *
from pdc_project.encoder import *

def test_encoder():
    assert_equal(encode("h"), [0,1,1,0,1,0,0,0])

def test_decoder():
    assert_equal(decode([0,1,1,0,1,0,0,0]), 'h')
    
def test_channel_encoding():
    s = "This is a test"
    assert_equal(decode(encode(s)), s)

def test_scramble():
    key = encode('z')
    assert_equal(scramble([0,1,1,0,1,0,0,0], key), [0,0,0,1,0,0,1,0])

def test_unscramble():
    key = encode('z')
    assert_equal( unscramble([0,0,0,1,0,0,1,0], key), [0,1,1,0,1,0,0,0])
    
def test_channel_scrambler():
    l = encode("This is a text")
    key = encode('z')
    assert_equal(unscramble(scramble(l, key) , key), l)
    
def test_forward_encode():
    l = [0, 1]
    assert_equal(forward_encode(l,2), [0,0,1,1])
    assert_equal(forward_encode(l,3), [0,0,0,1,1,1])

def test_forward_decode():
    l = [0,0,1,1]
    assert_equal(forward_decode(l,2), [0,1])
    l = [0,0,0,1,1,1]
    assert_equal(forward_decode(l,3), [0,1])

def test_forward_channel():
   l = [0, 1, 0, 1, 1, 0]
   assert_equal(forward_decode(forward_encode(l,2),2),l)

def test_channel_through():
    message = "hello, this is a test"
    assert_equal(decode_data(encode_data(message)), message)