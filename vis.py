import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon, QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QRect
import numpy as np

class VisWidget(QWidget):

    def __init__(self):
        super().__init__()

        # used for conversion from waveio data
        self.notes = np.array([
        'B1', 'C2', 'C#2', 'D2', 'D#2', 'E2', 'F2', 'F#2', 'G2', 'G#2', 'A2',
        'A#2', 'B2', 'C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3',
        'A3', 'A#3', 'B3', 'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4',
        'G#4', 'A4', 'A#4', 'B4', 'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5',
        'G5', 'G#5', 'A5', 'A#5', 'B5', 'C6'])

        self.radiiCoeffs = np.zeros_like(self.notes, dtype=float)

        self.numSlices = 12 # 12 notes in an octave, 1 circle is 1 octave
        self.angleFrac = 16 # angles measured in 16ths when drawing
        self.spanAngle = int(360 / self.numSlices) * self.angleFrac # degrees covered by a slice

        # want slices centered on axes, starting positive Y
        # 3 slices to start on pos-Y axis, -0.5 to center on axis
        self.offset = int((3 - 0.5) * self.spanAngle)
        self.slicePoints = [(p * self.spanAngle) + self.offset for p in range(self.numSlices)]

        # frames will be used to draw the circles/slices
        # QRect() objects to be utilized by paintEvent()
        self.frstFrame = QRect()
        self.scndFrame = QRect()
        self.thrdFrame = QRect()
        self.frthFrame = QRect()

        self.paintEvent(None)

    def paintEvent(self, event):
        frstRad = min(self.width(), self.height()) / 2.5
        scndRad = frstRad * .75
        thrdRad = frstRad * .50
        frthRad = frstRad * .25

        radInc = frthRad * 0.9

        # visualization is centered on the widget
        visCenterX = int(self.width() / 2)
        visCenterY = int(self.height() / 2)

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        #painter.drawText(self.width/2., 10, 'test')

        painter.setPen(Qt.white)

        for i in range(self.numSlices):
            painter.setBrush(QColor(148, 141, 179))
            rad = int(frstRad + (radInc * self.radiiCoeffs[(0*self.numSlices) + i+1]))
            frame = QRect(visCenterX - rad, visCenterY - rad, rad*2, rad*2)
            painter.drawPie(frame, self.slicePoints[i], self.spanAngle)

            painter.setBrush(QColor(96, 88, 133))
            rad = int(scndRad + (radInc * self.radiiCoeffs[(1*self.numSlices) + i+1]))
            frame = QRect(visCenterX - rad, visCenterY - rad, rad*2, rad*2)
            painter.drawPie(frame, self.slicePoints[i], self.spanAngle)

            painter.setBrush(QColor(67, 59, 103))
            rad = int(thrdRad + (radInc * self.radiiCoeffs[(2*self.numSlices) + i+1]))
            frame = QRect(visCenterX - rad, visCenterY - rad, rad*2, rad*2)
            painter.drawPie(frame, self.slicePoints[i], self.spanAngle)

            painter.setBrush(QColor(50, 35, 75))
            rad = int(frthRad + (radInc * self.radiiCoeffs[(3*self.numSlices) + i+1]))
            frame = QRect(visCenterX - rad, visCenterY - rad, rad*2, rad*2)
            painter.drawPie(frame, self.slicePoints[i], self.spanAngle)

        painter.end()

    def radiiReset(self):
        self.radiiCoeffs = np.zeros_like(self.notes, dtype=float)
        self.repaint()

    def updateVis(self, changeData):
        for noteInd, _, noteVol in changeData:
            self.radiiCoeffs[noteInd] = noteVol

        self.repaint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VisWidget()
    ex.show()
    sys.exit(app.exec_())
