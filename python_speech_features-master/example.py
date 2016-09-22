#!/usr/bin/env python

import scipy.io.wavfile as wav

from python_speech_features import logfbank
from python_speech_features import mfcc

(rate,sig) = wav.read("english.wav")
mfcc_feat = mfcc(sig,rate)
fbank_feat = logfbank(sig,rate)

print(fbank_feat[1:3,:])

import pyplot as plt
