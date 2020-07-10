from scipy.io import wavfile
import scipy.io
import numpy as np
import pyaudio
import wave
import time
import matplotlib.pyplot as plt

class WaveIO():

    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.pa_chunk = 1024
        self.np_data = np.empty([0, 2], dtype=np.int16)

    def check_np_data(self, data, fname):
        _, sci_data = wavfile.read(fname)

        if sci_data.shape != data.shape:
            print('failed')
            print(sci_data)
            print(data)

    def read_wave(self, fname):
        wf = wave.open(fname, 'rb')
        nchannels, sampwidth, framerate, nframes, _, _ = wf.getparams()

        # CALLBACK DOESN"T WORK CORRECTLY
        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            data_nframes = int(len(data) / 4)
            if len(data) != 0:
                conv_data = np.frombuffer(data, dtype=np.int16)
                shaped = np.reshape(conv_data, newshape=(data_nframes, 2))
                self.np_data = np.append(self.np_data, shaped, axis=0)
                #print(wf.tell(), shaped)
            return (data, pyaudio.paContinue)

        # open stream using callback (3)
        stream = self.pa.open(
                format=self.pa.get_format_from_width(sampwidth),
                channels=nchannels,
                rate=framerate,
                output=True,
                stream_callback=callback)

        # start the stream (4)
        stream.start_stream()

        # wait for stream to finish (5)
        while stream.is_active():
            time.sleep(0.1)

        # stop stream (6)
        stream.stop_stream()
        stream.close()
        wf.close()

        length = nframes / framerate
        time_lin = np.linspace(0, length, nframes)
        timestep = 1 / framerate

        spectrum = np.fft.fft2(self.np_data)
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
        data1.plot(time_lin,self.np_data[:, 0], color='red', label='Amplitude')
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
    waveio = WaveIO()
    waveio.read_wave('.\\output.wav')
