import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QRect, QCoreApplication

class App(QWidget):

    def __init__(self):
        super().__init__()

        self.screen = QCoreApplication.instance().primaryScreen().availableGeometry()
        self.x_adjust = int(self.screen.width() * 0.1)
        self.y_adjust = int(self.screen.height() * 0.1)
        self.width = self.screen.width() - self.x_adjust
        self.height = self.screen.height() - self.y_adjust

        self.initUI()
        self.paintEvent(None)

    def initUI(self):
        self.setWindowTitle('Voice Vis 0.1')

        #self.setWindowFlags(Qt.CustomizeWindowHint)
        #self.setWindowFlags(Qt.FramelessWindowHint)

        self.setGeometry(int(self.x_adjust / 2), int(self.y_adjust / 2), self.width, self.height)
        self.setFixedSize(self.width, self.height)

        self.show()

    def paintEvent(self, event):
        centerX = int(self.width / 2)
        centerY = int(self.height / 2)

        number_of_points = 12
        span_angle = int(360 / number_of_points)
        offset = int(0.5 * span_angle)
        points_on_circle = [(p * span_angle) + offset for p in range(number_of_points)]

        outer_radius = int(min(self.width, self.height) / 3)
        outer_circle_frame = QRect(centerX - outer_radius, centerY - outer_radius, outer_radius*2, outer_radius*2)

        inner_radius = int(outer_radius / 2)
        inner_circle_frame = QRect(centerX - inner_radius, centerY - inner_radius, inner_radius*2, inner_radius*2)

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.black)

        for p in points_on_circle:
            painter.setBrush(Qt.gray)
            painter.drawPie(outer_circle_frame, p * 16, span_angle * 16)
            painter.setBrush(Qt.red)
            painter.drawPie(inner_circle_frame, p * 16, span_angle * 16)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
