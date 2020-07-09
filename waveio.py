from scipy.io import wavfile
import scipy.io
import numpy as np
import matplotlib.pyplot as plt

class WaveIO():

    def __init__(self):
        None

    def read_wave(self, fname):
        rate, data = wavfile.read(fname)
        length = data.shape[0] / rate
        time = np.linspace(0., length, data.shape[0])
        timestep = 1. / rate

        spectrum = np.fft.fft(data[:, 0])
        frequency = np.fft.fftfreq(spectrum.size, d=timestep)
        index = np.where(frequency >= 0.)

        clipped_spectrum = timestep*spectrum[index].real
        clipped_frequency = frequency[index]

        # Create a figure
        fig = plt.figure()
        # Adjust white space between plots
        fig.subplots_adjust(hspace=0.5)
        # Create x-y plots of the amplitude and transform with labeled axes
        data1 = fig.add_subplot(2,1,1)
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title('Damping')
        data1.plot(time,data[:, 0], color='red', label='Amplitude')
        plt.legend()
        plt.minorticks_on()
        data2 = fig.add_subplot(2,1,2)
        plt.xlabel('Frequency')
        plt.ylabel('Signal')
        plt.title('Spectrum of a Damped Oscillator')
        data2.plot(clipped_frequency,clipped_spectrum, color='blue', linestyle='solid', marker='None', label='FFT', linewidth=1.5)
        plt.legend()
        plt.minorticks_on()
        plt.xlim(1., 3000.)
        # Show the data
        plt.show()

if __name__ == '__main__':
    wave = WaveIO()
    wave.read_wave('.\\output.wav')
