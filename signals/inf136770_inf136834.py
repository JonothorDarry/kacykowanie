#!/usr/bin/python

import sys
import numpy as np
import scipy.io.wavfile
import matplotlib.pyplot as plt
import os

pathway=str(sys.argv[1])

try:
	w, signal=scipy.io.wavfile.read(pathway)
except:
	print('Błąd odczytu')
	sys.exit(0)
	
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

dt=[i*x*conn for i,x in enumerate(dp)]
dt=sum(dt)/sum(dp)

mode=(np.argmax(dp)+d1)*conn
meanf=dt
iqr=p3[2]-p3[0]

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
#elif (iqr[i]<=70 and p3[i][2]>140):
elif (p3[0]>95):
	cl='K'
else:
	cl='M'
print(cl)
