import sys
from vis import VisWidget
from waveio import Wave
from mic import Mic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QRadioButton, QGridLayout, QHBoxLayout, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QIcon, QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QCoreApplication, QThread, QRect

class App(QWidget):

    def __init__(self):
        super().__init__()

        self.screen = QCoreApplication.instance().primaryScreen().availableGeometry()
        self.xAdjust = int(self.screen.width() * 0.1)
        self.yAdjust = int(self.screen.height() * 0.1)
        self.width = self.screen.width() - self.xAdjust
        self.height = self.screen.height() - self.yAdjust

        self.vis = VisWidget()

        self.mic_active = False

        self.fileButton = QPushButton('Input File')
        self.startMic = QPushButton('Microphone On')
        self.stopMic = QPushButton('Microphone Off')

        self.threads = []

        self.initWave()

        self.initUI()

    def initWave(self):
        self.waveThread = QThread()
        self.waveObj = Wave()
        self.waveObj.moveToThread(self.waveThread)
        self.waveThread.started.connect(self.waveObj.readWave)
        self.waveObj.update.connect(self.vis.updateVis)
        self.waveObj.finished.connect(self.vis.radiiReset)
        self.waveObj.finished.connect(self.waveThread.quit)

    def initMic(self):
        if self.mic_active:
            return

        micThread = QThread()
        micObj = Mic()
        micObj.moveToThread(micThread)
        self.stopMic.clicked.connect(micObj.stream.stop_stream)
        micThread.started.connect(micObj.listen)
        micObj.update.connect(self.vis.updateVis)
        micObj.finished.connect(self.vis.radiiReset)
        micObj.finished.connect(micThread.quit)
        micObj.finished.connect(self.micOff)
        micThread.start()
        self.mic_active = True
        self.threads.append((micObj, micThread))

    def initUI(self):
        buttonsWidth = int(self.width / 4)

        self.fileButton.setMaximumWidth(buttonsWidth)
        self.fileButton.clicked.connect(self.fileInput)

        self.startMic.setMaximumWidth(buttonsWidth)
        self.startMic.clicked.connect(self.initMic)

        self.stopMic.setMaximumWidth(buttonsWidth)

        buttonsVBox = QVBoxLayout()
        buttonsVBox.addWidget(self.fileButton)
        buttonsVBox.addWidget(self.startMic)
        buttonsVBox.addWidget(self.stopMic)
        buttonsVBox.addStretch()

        mainHBox = QHBoxLayout()
        mainHBox.addWidget(self.vis)
        mainHBox.addLayout(buttonsVBox)
        self.setLayout(mainHBox)

        self.setWindowTitle('Voice Vis 0.1')

        #self.setWindowFlags(Qt.CustomizeWindowHint)
        #self.setWindowFlags(Qt.FramelessWindowHint)

        self.setGeometry(int(self.xAdjust / 2), int(self.yAdjust / 2), self.width, self.height)

        self.show()

    def fileInput(self):
        dialog = QFileDialog()
        fname, _ = dialog.getOpenFileName(self, filter='Wave File (*.wav)')
        if fname is not None:
            self.waveObj.setFileName(fname)
            self.waveThread.start()

    def micOff(self):
        self.mic_active = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
