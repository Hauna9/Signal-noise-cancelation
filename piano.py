import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.fftpack import fft

t = np.linspace(0, 3, 12 * 1024)
d5 = 587.33  # the frequency of every note for the song
d4 = 293.66  # the frequency of every note for the song
a4 = 440  # the frequency of every note for the song
G4 = 415.30  # the frequency of every note for the song
g4 = 392  # the frequency of every note for the song
f4 = 349.23  # the frequency of every note for the song
c4 = 261.63  # the frequency of every note for the song

# n: the array containing the frequencies of the notes
n = [d4, d4, d5, a4, G4, g4, f4, d4, f4, g4, c4, c4, d5, a4, G4, g4, f4, d4, f4, g4]
# ti: the starting time for each note # Ti: the duration that determines how long each note lasts
ti = [0, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.9, 2.1, 2.3, 2.5, 2.7, 2.8, 2.9]
Ti = [0.05, 0.05, 0.05, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05]
x = 0
for i in range(len(n)):
    # s: summing the sin functions for every note. only one hand is used to play the notes
    s = (np.sin(2 * np.pi * n[i] * t)) + (np.sin(2 * np.pi * 0 * t))
    u1 = 10*((t-ti[i]) >= 0)  # first unit step function
    u2 = 10*((t-ti[i]-Ti[i]) >= 0)  # second unit step function
    x = x + np.multiply(s, (u1 - u2))  # the final calculation and adding it to the cumulative sum

plt.subplot(3, 2, 1)  # plotting the summation with time x
plt.plot(t, x)

# start of Project milestone 2

N = 3*1024
f = np.linspace(0, 512, int(N/2))
# x_f is frequency domain of x
x_f = fft(x)
x_f = 2/N * np.abs(x_f[0:int(N/2)])
plt.subplot(3, 2, 2)  # plotting x_f
plt.plot(f, x_f)

fn = np.random.randint(0, 512, 2)
noiseToAdd = np.sin(2*np.pi*fn[0]*t) + np.sin(2*np.pi*fn[1]*t)

# xn is time domain of x with noise
xn = x + noiseToAdd

plt.subplot(3, 2, 3)  # plotting xn
plt.plot(t, xn)

# xn_f is frequency domain of xn
xn_f = fft(xn)
xn_f = 2/N * np.abs(xn_f[0:int(N/2)])

plt.subplot(3, 2, 4)  # plotting xn_f
plt.plot(f, xn_f)

# noiseToCancel is the extracted noise from xn
noiseToCancel = xn_f - x_f
# freq is an array of the added noise frequencies
freq = [0, 0]
# j is the index of the added noise frequencies
j = 0
for i in range(len(noiseToCancel)):   #Loop to find the frequencies at which the noise takes place
    if noiseToCancel[i] > 1:
        freq[j] = f[i]
        j += 1

# xfiltered is the time domain signal after the noise cancellation
xfiltered = xn - (np.sin(2*np.round((freq[0]))*t*np.pi) + np.sin(2*np.round((freq[1]))*t*np.pi))

plt.subplot(3, 2, 5)  # plotting xfiltered
plt.plot(t, xfiltered)

# xfiltered_f is the frequency domain of xfiltered
xfiltered_f = fft(xfiltered)
xfiltered_f = 2/N * np.abs(xfiltered_f[0:int(N/2)])

plt.subplot(3, 2, 6)  # plotting xfiltered_f
plt.plot(f, xfiltered_f)

plt.show()
#sd.play(x,3*1024) # plays the original song
#sd.play(xn,3*1024)  #plays the original song with the distortion/noise added
sd.play(xfiltered, 3 * 1024)  # plays the song after filtering.



