#!/usr/bin/python3

import sys
import numpy as np
import wave
from scipy.signal import decimate, correlate
from scipy.stats import mode
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

#cross correlation
def cross_correlation(signal, sample_rate):
    window_len = len(signal)
    window = signal
    window = window - np.mean(window)
    
    result = correlate(window, window, method = 'fft')
    
    high = sample_rate//300
    left = window_len - 1 + high
    right = window_len + sample_rate//60
    result = result[left:right]
    return sample_rate / (np.argmax(result) + high)

def classify_file(sample_rate, data, method = hps):
    if len(data.shape) == 1:
        result = method(data, sample_rate)
    else:
        result1 = method(data[:, 0], sample_rate)
        result2 = method(data[:, 1], sample_rate)
        result = (result1 + result2) / 2
    
    if result > 175:
        return 'K'
    else:
        return 'M'

def decision_tree_classification(w, signal):
    if(len(signal.shape)==2 and signal.shape[1]==2):
        signal = [s[0] for s in signal]
    signum=abs(np.fft.fft(signal))[:len(signal)//2]

    conn=(w/(len(signum)*2))
    d1=int(60//conn)
    d2=int(290//conn+1)

    dp=signum[d1:d2]*conn
    kv=sum(dp)
    asum=0

    p3=[0]*3
    for jj in range(len(dp)):
        asum+=dp[jj]
        for ij in range(1,4):
            if (asum>kv*ij*0.25 and p3[ij-1]==0):
                p3[ij-1]=jj*conn

    mode=(np.argmax(dp)+d1)*conn

    summa=0
    if (p3[0]<70):
        if (mode>207):
            cl='K'
        else:
            cl='M'

    elif (mode>=200):
        if (p3[0]<90):
            cl='M'
        else:
            cl='K'
    elif (p3[0]>95):
        cl='K'
    else:
        cl='M'
    return cl

try:
    filepath = str(sys.argv[1])
    sample_rate, data = read_wav_file(filepath)
    result1 = classify_file(sample_rate, data, method = hps)
    result2 = classify_file(sample_rate, data, method = cross_correlation)
    result3 = decision_tree_classification(sample_rate, data)
    result = mode([result1, result2, result3])[0][0]
except:
    result = 'M'
print(result)


