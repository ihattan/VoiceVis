import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon, QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QRect

"""
VisWidget range C2 - B4, frequencies:
     C     C#    D     D#    E     F     F#    G     G#    A     A#    B
2:  65.4  69.3  73.4  77.8  82.4  87.3  92.5  98.0 103.8 110.0 116.5 123.4
3: 130.8 138.6 146.8 155.6 164.8 174.6 185.0 196.0 207.7 220.0 233.1 247.0
4: 231.6 277.2 293.7 311.1 329.6 349.2 370.0 392.0 415.3 440.0 466.1 493.9
"""

class VisWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.notes_freqs = {}

        self.numSlices = 12 # 12 notes in an octave, 1 circle is 1 octave
        self.spanAngle = int(360 / self.numSlices)


        # a list of size self.numSlices, equidistant points along a circle
        self.slicePoints = []
        self.calcSlicePoints()

        # frames will be used to draw the circles/slices
        # QRect() objects to be utilized by paintEvent()
        self.frstFrame = QRect()
        self.scndFrame = QRect()
        self.thrdFrame = QRect()
        self.frthFrame = QRect()

        self.paintEvent(None)


    def calcSlicePoints(self):
        offset = int(0.5 * self.spanAngle) # want slices centered on axes
        self.slicePoints = [(p * self.spanAngle) + offset for p in range(self.numSlices)]

    def calcFrames(self):
        spanAngle = int(360 / self.numSlices)
        offset = int(0.5 * spanAngle) # want slices centered on axes
        slicePoints = [(p * spanAngle) + offset for p in range(self.numSlices)]

        # first is largest, 1/3 the height of the given area
        # rest of the radii are 2/3 and 1/3 the size of the first
        frstRadius = int(min(self.width(), self.height()) / 2.5)
        scndRadius = int(frstRadius * .75)
        thrdRadius = int(frstRadius * .50)
        frthRadius = int(frstRadius * .25)

        # center of the visualization is offset to the left
        visCenterX = int(self.width() / 2)
        visCenterY = int(self.height() / 2)

        self.frstFrame = QRect(visCenterX - frstRadius, visCenterY - frstRadius, frstRadius*2, frstRadius*2)
        self.scndFrame = QRect(visCenterX - scndRadius, visCenterY - scndRadius, scndRadius*2, scndRadius*2)
        self.thrdFrame = QRect(visCenterX - thrdRadius, visCenterY - thrdRadius, thrdRadius*2, thrdRadius*2)
        self.frthFrame = QRect(visCenterX - frthRadius, visCenterY - frthRadius, frthRadius*2, frthRadius*2)

    def paintEvent(self, event):
        self.calcFrames()

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.drawVis(painter)
        painter.end()

    def drawVis(self, painter):
        angleFrac = 16 # angles measured in 16ths when drawing
        painter.setPen(Qt.white)

        for p in self.slicePoints:
            painter.setBrush(QColor(148, 141, 179))
            painter.drawPie(self.frstFrame, p * angleFrac, self.spanAngle * angleFrac)
            painter.setBrush(QColor(96, 88, 133))
            painter.drawPie(self.scndFrame, p * angleFrac, self.spanAngle * angleFrac)
            painter.setBrush(QColor(67, 59, 103))
            painter.drawPie(self.thrdFrame, p * angleFrac, self.spanAngle * angleFrac)
            painter.setBrush(QColor(50, 35, 75))
            painter.drawPie(self.frthFrame, p * angleFrac, self.spanAngle * angleFrac)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VisWidget()
    ex.show()
    sys.exit(app.exec_())
