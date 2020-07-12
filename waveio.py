import numpy as np
import pyaudio
import wave
import time
import matplotlib.pyplot as plt

class WaveIO():

    def __init__(self, fname):
        self.pa = pyaudio.PyAudio()
        self.wave_file = wave.open(fname, 'rb')
        self.wave_data = np.empty([0, 2], dtype=np.int16)
        self.nchannels, self.sampwidth, self.framerate, self.nframes, _, _ = self.wave_file.getparams()

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

    def read_wave(self):
        frame_byte_length = self.sampwidth * self.nchannels

        def callback(in_data, frame_count, time_info, status):
            curr_data = self.wave_file.readframes(frame_count)
            data_nframes = int(len(curr_data) / frame_byte_length)
            if len(curr_data) != 0:
                conv_data = np.frombuffer(curr_data, dtype=np.int16)
                shaped = np.reshape(conv_data, newshape=(data_nframes, self.nchannels))
                self.wave_data = np.append(self.wave_data, shaped, axis=0)
            return (curr_data, pyaudio.paContinue)

        # open stream using callback (3)
        stream = self.pa.open(
                format=self.pa.get_format_from_width(self.sampwidth),
                channels=self.nchannels,
                rate=self.framerate,
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
        self.wave_file.close()

        print(self.analyze_fft(self.wave_data[:, 0]))

    def analyze_fft(self, data):
        length = self.nframes / self.framerate
        time_lin = np.linspace(0, length, self.nframes)
        timestep = 1 / self.framerate

        spectrum = np.fft.fft(data)
        frequency = np.fft.fftfreq(spectrum.size, d=timestep)
        index = np.where(np.logical_and(frequency <= 1000, frequency >= 65))

        fft_spec = np.abs(timestep*spectrum[index].real)
        fft_freq = frequency[index]

        audible_ind = np.where(fft_spec >= 250.)
        audible_freqs = fft_freq[audible_ind]
        audible_specs = fft_spec[audible_ind]

        specs = np.zeros_like(self.notes, dtype=int)

        digi_freqs = np.digitize(audible_freqs, self.bins)
        for i in range(len(audible_freqs)):
            if specs[digi_freqs[i]] < audible_specs[i]:
                specs[digi_freqs[i]] = audible_specs[i]

        audible_notes_ind = np.where(specs > 0)
        audible_notes = self.notes[audible_notes_ind]
        audible_specs = specs[audible_notes_ind]

        return list(zip(audible_notes, audible_specs))

    def drawPlotlyGraphs(self, time_lin):
        # Create a figure
        fig = plt.figure()
        # Adjust white space between plots
        fig.subplots_adjust(hspace=0.5)
        # Create x-y plots of the amplitude and transform with labeled axes
        data1 = fig.add_subplot(2,1,1)
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title('Damping')
        data1.plot(time_lin, self.wave_data[:, 0], color='red', label='Amplitude')
        plt.legend()
        plt.minorticks_on()
        data2 = fig.add_subplot(2,1,2)
        plt.xlabel('Frequency')
        plt.ylabel('Signal')
        plt.title('Spectrum')
        data2.plot(self.fft_freq, self.fft_spec, color='blue', linestyle='solid', marker='None', label='FFT', linewidth=1.5)
        plt.legend()
        plt.minorticks_on()
        # Show the data
        plt.show()

if __name__ == '__main__':
    waveio = WaveIO('.\\output.wav')
    waveio.read_wave()
