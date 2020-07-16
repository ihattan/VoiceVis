import numpy as np
import pyaudio
import wave
import time
import matplotlib.pyplot as plt

class WaveIO():

    def __init__(self, fname):
        self.pa = pyaudio.PyAudio()
        self.wave_file = wave.open(fname, 'rb')
        self.nchannels, self.sampwidth, self.framerate, self.nframes, _, _ = self.wave_file.getparams()
        self.timestep = np.reciprocal(float(self.framerate))
        self.wave_format = self.pa.get_format_from_width(self.sampwidth)
        self.np_wave_format = self.pyAudioToNumpy(self.wave_format)
        self.chunk = 256

        self.bins = np.array([
        63.571, 67.35, 71.356, 75.598, 80.092, 84.836, 89.882, 95.246, 100.91,
        106.912, 113.27, 120.006, 127.14, 134.7, 142.712, 151.196, 160.184,
        169.672, 179.764, 190.492, 201.82, 213.824, 226.54, 240.012, 254.28,
        269.4, 285.424, 302.392, 320.368, 339.344,359.528, 380.984, 403.64,
        427.648, 453.08, 480.024, 508.56, 538.8,570.848, 604.784, 640.736,
        678.688, 719.056, 761.968, 807.28, 855.296, 906.160, 960.048, 1017.135])

        # starts at B1 because np.digitize() bins starting at 0, off-by-one
        self.notes = np.array([
        'B1', 'C2', 'C#2', 'D2', 'D#2', 'E2', 'F2', 'F#2', 'G2', 'G#2', 'A2',
        'A#2', 'B2', 'C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3',
        'A3', 'A#3', 'B3', 'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4',
        'G#4', 'A4', 'A#4', 'B4', 'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5',
        'G5', 'G#5', 'A5', 'A#5', 'B5', 'C6'])

    def read_wave(self, callback):
        # open stream using callback (3)
        stream = self.pa.open(
                format=self.wave_format,
                channels=self.nchannels,
                rate=self.framerate,
                output=True)

        data = self.wave_file.readframes(self.chunk*15)
        stream.write(data)

        conv_data = np.frombuffer(data, dtype=self.np_wave_format)[::2]

        chunk = self.wave_file.readframes(self.chunk)

        while len(chunk) > 0:
            stream.write(chunk)

            conv_chunk = np.frombuffer(chunk, dtype=self.np_wave_format)[::2]

            conv_data = np.append(conv_data, conv_chunk)
            callback(self.analyze_data(conv_data))

            conv_data = conv_data[self.chunk:]

            chunk = self.wave_file.readframes(self.chunk)

        stream.stop_stream()
        stream.close()

    #perform fft analysis, requires 1-dimensional data
    def analyze_data(self, data):
        spectrum = np.fft.fft(data)
        frequency = np.fft.fftfreq(spectrum.size, d=self.timestep)
        index = np.where(np.logical_and(frequency < self.bins[-1], frequency > self.bins[0]))

        fft_spec = np.abs(self.timestep*spectrum[index].real)
        fft_freq = frequency[index]

        if fft_spec.size == 0 or np.amax(fft_spec) == 0.:
            return []

        fft_spec *= np.reciprocal(np.amax(fft_spec))

        aud_threshold = 0.5

        aud_ind = np.where(fft_spec > aud_threshold)
        aud_freqs = fft_freq[aud_ind]
        aud_specs = fft_spec[aud_ind]

        specs = np.zeros_like(self.notes, dtype=float)

        digi_freqs = np.digitize(aud_freqs, self.bins)
        for i in range(digi_freqs.size):
            if specs[digi_freqs[i]] < aud_specs[i]:
                specs[digi_freqs[i]] = aud_specs[i]

        aud_notes_ind = np.where(specs > 0.)
        aud_notes = self.notes[aud_notes_ind]
        aud_notes_specs = specs[aud_notes_ind]

        #self.drawPlotlyGraphs(data, fft_freq, fft_spec)
        return list(zip(aud_notes, aud_notes_specs))

    def drawPlotlyGraphs(self, data, fft_freq, fft_spec):
        length = data.shape[0] / self.framerate
        time_lin = np.linspace(0, length, data.shape[0])

        # Create a figure
        fig = plt.figure()
        # Adjust white space between plots
        fig.subplots_adjust(hspace=0.5)
        # Create x-y plots of the amplitude and transform with labeled axes
        data1 = fig.add_subplot(2,1,1)
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title('Damping')
        data1.plot(time_lin, data, color='red', label='Amplitude')
        plt.legend()
        plt.minorticks_on()
        data2 = fig.add_subplot(2,1,2)
        plt.xlabel('Frequency')
        plt.ylabel('Signal')
        plt.title('Spectrum')
        data2.plot(fft_freq, fft_spec, color='blue', linestyle='solid', marker='None', label='FFT', linewidth=1.5)
        plt.legend()
        plt.minorticks_on()
        # Show the data
        plt.show()

    def pyAudioToNumpy(self, format):
        formats = {
            pyaudio.paFloat32: np.float32,
            pyaudio.paUInt8: np.uint8,
            pyaudio.paInt8: np.int8,
            pyaudio.paInt16: np.int16,
            pyaudio.paInt24: np.int32
        }

        return formats[format]

if __name__ == '__main__':
    waveio = WaveIO('.\\output.wav')
    waveio.read_wave(lambda x: print(x))
