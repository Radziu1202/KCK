import pickle
import sys
import numpy as np
import scipy.io.wavfile as wavfile
from scipy.stats import skew
import warnings
import matplotlib.pyplot as plt
from scipy import *
import os
from scipy import signal




def HPS(data,rate):
    #print(len(data))
    #Nsamps = len(data);
    #ham= bla(Nsamps);
    #data=data*ham
    newAudio = [data[i:i+rate] for i in range(0,len(data),rate)]
    FFTSamples= [abs(np.fft.rfft(sample)) for sample in newAudio]
    FFTSamples=FFTSamples[:-1]

    harmonics=[]
    for i in FFTSamples:
        HPS = np.copy(i)
        for h in np.arange(2, 6):
            decimate = signal.decimate(i, h)
            HPS[:len(decimate)] *= decimate
        harmonics.append(HPS)

    result=harmonics[0]

    
    for i in range(1, len(harmonics)):
        result+=harmonics[i]

    dt=1/rate
    freq_vector = np.fft.fftfreq(len(FFTSamples[0]), d=dt)
    
   
  #  x=FFTSamples[0]
   # for i in range (len(FFTSamples)):
    #    x*=FFTSamples[i]


    mean80 = np.mean(result[85:180])
    mean165 = np.mean(result[165:255])

    if mean80>mean165:
        return "M"
    else:
        return "K"

    


'''
def zacznij():
    directory=os.listdir('train');
    samples = []
    maleCount = 0
    femaleCount = 0
    for file_name in directory:
        if file_name=="001_K.wav":
            continue

        
        rate, data = wavfile.read('train/'+file_name)
        if type(data[0]) == type(np.array([])):
            data = data[:,1]
        HPS(data,rate)
'''

def open_file(file_name):
    rate, data = wavfile.read(file_name)
    if type(data[0]) == type(np.array([])):
            data = data[:,1]
    return HPS(data,rate);

if __name__ == '__main__':
    
    #zacznij()
    print(open_file(sys.argv[1]))
    

