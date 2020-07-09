import sys
from vis import VisWidget
from read_wave import WaveIO
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

        self.initUI()

    def initUI(self):
        fileButton = QPushButton('Input File')
        fileButton.setMaximumWidth(int(self.width / 4))
        fileButton.clicked.connect(lambda : self.fileInput())

        mainHBox = QHBoxLayout()
        mainHBox.addWidget(VisWidget())
        mainHBox.addWidget(fileButton)
        self.setLayout(mainHBox)

        self.setWindowTitle('Voice Vis 0.1')

        #self.setWindowFlags(Qt.CustomizeWindowHint)
        #self.setWindowFlags(Qt.FramelessWindowHint)

        self.setGeometry(int(self.xAdjust / 2), int(self.yAdjust / 2), self.width, self.height)
        #self.setFixedSize(self.width, self.height)

        self.show()

    def fileInput(self):
        fin = QFileDialog()
        fname, _ = fin.getOpenFileName(self, filter='Wave File (*.wav)')
        if fname is not None:
            waveObj = WaveIO()
            waveObj.read_wave(fname)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
