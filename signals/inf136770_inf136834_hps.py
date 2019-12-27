#!/usr/bin/python3

import sys
import numpy as np
import wave
from scipy.signal import decimate, correlate
import os

def read_wav_file(filepath):
    wave_read = wave.open(filepath, mode = 'rb')
    length = wave_read.getnframes()
    sample_rate = wave_read.getframerate()
    
    if wave_read.getsampwidth() == 1:
        type = np.uint8
    elif wave_read.getsampwidth() == 2:
        type = np.int16
    elif wave_read.getsampwidth() == 4:
        type = np.int32
    else:
        type = np.int16
        
    data = np.frombuffer(wave_read.readframes(length), count = wave_read.getnchannels() * length, dtype = type)
    if wave_read.getnchannels() >= 2:
        data = np.reshape(data, (length, wave_read.getnchannels()))
    wave_read.close()
    return sample_rate, data

def fft(signal):
    n = len(signal)
    signal_fft = np.fft.fft(signal)
    signal_fft = np.abs(signal_fft)
    
    signal_fft = signal_fft * 2 / n
    signal_fft[0] = signal_fft[0] / 2
    return signal_fft

#harmonic product spectrum
def hps(signal, sample_rate):
    n = len(signal)
    signal = fft(signal)
    
    n_harmonics = 4
    signal = signal[:len(signal)//2]
    result_signal = signal
    for i in range(2, n_harmonics + 1):
        downsampled = decimate(signal, i)
        result_signal = result_signal[:downsampled.shape[0]] * downsampled
    
    i_begin = int(60 * n / sample_rate)
    
    return (np.argmax(result_signal[i_begin:]) + i_begin) * sample_rate / n

def classify_file(filepath):
    method = hps
    try:
        sample_rate, data = read_wav_file(filepath)
    except:
        return 'M'
    
    if len(data.shape) == 1:
        result = method(data, sample_rate)
    else:
        result1 = method(data[:, 0], sample_rate)
        result2 = method(data[:, 1], sample_rate)
        result = (result1 + result2) / 2
    
    if result > 170:
        return 'K'
    else:
        return 'M'

filepath = str(sys.argv[1])
print(classify_file(filepath))

