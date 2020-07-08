import sys
from vis import Vis
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon, QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QCoreApplication, QRect #, QPoint, QSize

class App(QWidget):

    def __init__(self):
        super().__init__()

        self.screen = QCoreApplication.instance().primaryScreen().availableGeometry()
        self.xAdjust = int(self.screen.width() * 0.1)
        self.yAdjust = int(self.screen.height() * 0.1)
        self.width = self.screen.width() - self.xAdjust
        self.height = self.screen.height() - self.yAdjust
        self.vis = Vis(self.width, self.height)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Voice Vis 0.1')

        #self.setWindowFlags(Qt.CustomizeWindowHint)
        #self.setWindowFlags(Qt.FramelessWindowHint)

        self.setGeometry(int(self.xAdjust / 2), int(self.yAdjust / 2), self.width, self.height)
        self.setFixedSize(self.width, self.height)

        self.paintEvent(None)
        self.show()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.drawVis(painter)
        painter.end()

    def drawVis(self, painter):
        angleFrac = 16 # angles measured in 16ths when drawing
        painter.setPen(Qt.white)

        for p in self.vis.slicePoints:
            painter.setBrush(QColor(148, 141, 179))
            painter.drawPie(self.vis.frstFrame, p * angleFrac, self.vis.spanAngle * angleFrac)
            painter.setBrush(QColor(96, 88, 133))
            painter.drawPie(self.vis.scndFrame, p * angleFrac, self.vis.spanAngle * angleFrac)
            painter.setBrush(QColor(67, 59, 103))
            painter.drawPie(self.vis.thrdFrame, p * angleFrac, self.vis.spanAngle * angleFrac)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
