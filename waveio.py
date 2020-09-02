import numpy as np
import pyaudio
import wave
import time
import matplotlib.pyplot as plt
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class Wave(QObject):
    finished = pyqtSignal()
    update = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.pa = pyaudio.PyAudio()

        self.chunk = 256
        self.filename = None

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


    def setFileName(self, str):
        self.filename = str

    #def readWave(self, callback):
    @pyqtSlot()
    def readWave(self):
        if self.filename is None:
            self.finished.emit()

        waveFile = wave.open(self.filename, 'rb')
        nchannels, sampwidth, framerate, nframes, _, _ = waveFile.getparams()
        waveFormat = self.pa.get_format_from_width(sampwidth)
        npWaveFormat = self.pyAudioToNumpy(waveFormat)

        stream = self.pa.open(
                format=waveFormat,
                channels=nchannels,
                rate=framerate,
                output=True)

        data = waveFile.readframes(self.chunk*15)
        stream.write(data)

        convData = np.frombuffer(data, dtype=npWaveFormat)[::2]

        chunk = waveFile.readframes(self.chunk)

        while len(chunk) > 0:
            stream.write(chunk)

            convChunk = np.frombuffer(chunk, dtype=npWaveFormat)[::2]

            convData = np.append(convData, convChunk)
            #callback(self.analyzeData(convData))
            results = self.analyzeData(convData, framerate)
            self.update.emit(results)

            convData = convData[self.chunk:]

            chunk = waveFile.readframes(self.chunk)

        stream.stop_stream()
        stream.close()

        self.finished.emit()

    #perform fft analysis, requires 1-dimensional data
    def analyzeData(self, data, framerate):
        timestep = np.reciprocal(float(framerate))

        spectrum = np.fft.fft(data)
        frequency = np.fft.fftfreq(spectrum.size, d=timestep)
        index = np.where(np.logical_and(frequency < self.bins[-1], frequency > self.bins[0]))

        fftSpec = np.abs(timestep*spectrum[index].real)
        fftFreq = frequency[index]

        if fftSpec.size == 0 or np.amax(fftSpec) == 0.:
            return []

        fftSpec *= np.reciprocal(np.amax(fftSpec))

        audThreshold = 0.5

        audInd = np.where(fftSpec > audThreshold)
        audFreqs = fftFreq[audInd]
        audSpecs = fftSpec[audInd]

        specs = np.zeros_like(self.notes, dtype=float)

        digiFreqs = np.digitize(audFreqs, self.bins)
        for i in range(digiFreqs.size):
            if specs[digiFreqs[i]] < audSpecs[i]:
                specs[digiFreqs[i]] = audSpecs[i]

        audNotesInd = np.where(specs > 0.)
        audNotes = self.notes[audNotesInd]
        audNotesSpecs = specs[audNotesInd]

        return list(zip(audNotesInd, audNotes, audNotesSpecs))

    def drawPlotlyGraphs(self, data, fftFreq, fftSpec):
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
        data2.plot(fftFreq, fftSpec, color='blue', linestyle='solid', marker='None', label='FFT', linewidth=1.5)
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
    waveio = LoadWave('.\\output.wav')
    waveio.readWave(lambda x: print(x))
