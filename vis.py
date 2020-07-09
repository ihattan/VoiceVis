import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon, QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QRect

class VisWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.numSlices = 12
        self.spanAngle = int(360 / self.numSlices)

        # a list of size self.numSlices, equidistant points along a circle
        self.slicePoints = []
        self.calcSlicePoints()

        # frames will be used to draw the circles/slices
        # QRect() objects to be utilized by paintEvent()
        self.frstFrame = QRect()
        self.scndFrame = QRect()
        self.thrdFrame = QRect()
        #self.calcFrames()

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
        frstRadius = int(min(self.width(), self.height()) / 3)
        scndRadius = int(frstRadius * 2 / 3)
        thrdRadius = int(frstRadius * 1 / 3)

        # center of the visualization is offset to the left
        visCenterX = int(self.width() / 2)
        visCenterY = int(self.height() / 2)

        self.frstFrame = QRect(visCenterX - frstRadius, visCenterY - frstRadius, frstRadius*2, frstRadius*2)
        self.scndFrame = QRect(visCenterX - scndRadius, visCenterY - scndRadius, scndRadius*2, scndRadius*2)
        self.thrdFrame = QRect(visCenterX - thrdRadius, visCenterY - thrdRadius, thrdRadius*2, thrdRadius*2)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VisWidget()
    ex.show()
    sys.exit(app.exec_())
