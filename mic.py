import numpy as np
import pyaudio
import wave
import time
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class Mic(QObject):
    finished = pyqtSignal()
    update = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.pa = pyaudio.PyAudio()

        inputDevice = self.pa.get_default_input_device_info()
        self.channels = inputDevice['maxInputChannels']
        self.rate = int(inputDevice['defaultSampleRate'])
        self.timestep = np.reciprocal(float(self.rate))

        self.format = pyaudio.paInt16
        self.npFormat = np.int16
        self.chunk = 256

        self.stream = self.pa.open(
            format=self.format,
            channels = self.channels,
            rate = self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

        self.bins = np.array([
        63.571, 67.35, 71.356, 75.598, 80.092, 84.836, 89.882, 95.246, 100.91,
        106.912, 113.27, 120.006, 127.14, 134.7, 142.712, 151.196, 160.184,
        169.672, 179.764, 190.492, 201.82, 213.824, 226.54, 240.012, 254.28,
        269.4, 285.424, 302.392, 320.368, 339.344,359.528, 380.984, 403.64,
        427.648, 453.08, 480.024, 508.56, 538.8,570.848, 604.784, 640.736,
        678.688, 719.056, 761.968, 807.28, 855.296, 906.160, 960.048, 1017.135])

        self.notes = np.array([
        'B1', 'C2', 'C#2', 'D2', 'D#2', 'E2', 'F2', 'F#2', 'G2', 'G#2', 'A2',
        'A#2', 'B2', 'C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3',
        'A3', 'A#3', 'B3', 'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4',
        'G#4', 'A4', 'A#4', 'B4', 'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5',
        'G5', 'G#5', 'A5', 'A#5', 'B5', 'C6'])

    @pyqtSlot()
    def listen(self):
        try:
            data = self.stream.read(self.chunk*15)
            convData = np.frombuffer(data, dtype=self.npFormat)[::2]
            chunk = self.stream.read(self.chunk)

            while self.stream.is_active():
                convChunk = np.frombuffer(chunk, dtype=self.npFormat)[::2]

                convData = np.append(convData, convChunk)
                self.update.emit(self.analyzeData(convData))

                convData = convData[self.chunk:]

                chunk = self.stream.read(self.chunk)
        except:
            self.pa.close(self.stream)
            self.finished.emit()

    #perform fft analysis, requires 1-dimensional data
    def analyzeData(self, data):
        spectrum = np.fft.fft(data)
        frequency = np.fft.fftfreq(spectrum.size, d=self.timestep)
        index = np.where(np.logical_and(frequency < self.bins[-1], frequency > self.bins[0]))

        fftSpec = np.abs(self.timestep*spectrum[index].real)
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

if __name__ == '__main__':
    mic = Mic()

    print('Listening....')
    print('Press Ctrl+C to stop listening')

    try:
        mic.listen(lambda x: print(x))
    except KeyboardInterrupt:
        mic.stop()
        print(f"Done, status: {mic.listening}")
