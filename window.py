import sys
from vis import VisWidget
from waveio import WaveIO
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout, QFileDialog
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
        self.vis = VisWidget()

        self.initUI()

    def initUI(self):
        buttonsWidth = int(self.width / 4)

        fileButton = QPushButton('Input File')
        fileButton.setMaximumWidth(buttonsWidth)
        fileButton.clicked.connect(lambda : self.fileInput())

        recButton = QPushButton('Record Audio')
        recButton.setMaximumWidth(buttonsWidth)
        recButton.clicked.connect(lambda : self.recordMic())

        buttonsVBox = QVBoxLayout()
        buttonsVBox.addWidget(fileButton)
        buttonsVBox.addWidget(recButton)
        buttonsVBox.addStretch()

        mainHBox = QHBoxLayout()
        mainHBox.addWidget(self.vis)
        mainHBox.addLayout(buttonsVBox)
        self.setLayout(mainHBox)

        self.setWindowTitle('Voice Vis 0.1')

        #self.setWindowFlags(Qt.CustomizeWindowHint)
        #self.setWindowFlags(Qt.FramelessWindowHint)

        self.setGeometry(int(self.xAdjust / 2), int(self.yAdjust / 2), self.width, self.height)
        #self.setFixedSize(self.width, self.height)

        self.show()

    def fileInput(self):
        dialog = QFileDialog()
        fname, _ = dialog.getOpenFileName(self, filter='Wave File (*.wav)')
        if fname is not None:
            waveObj = WaveIO(fname)
            waveObj.read_wave(self.vis.updateVis)

        self.vis.radiiReset()

    def recordMic(self):
        None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
