import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtGui import QIcon, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QRect

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Voice Vis 0.1'
        self.left = 150
        self.top = 40
        self.width = 1000
        self.height = 1000
        self.initUI()
        self.paintEvent(None)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def paintEvent(self, event):
        center = (int(self.width/2), int(self.height/2))
        number_of_points = 12
        span_angle = int(360 / number_of_points)
        offset = int(0.5 * span_angle)
        points_on_circle = [(p * span_angle) + offset for p in range(number_of_points)]

        outer_radius = 400
        outer_circle_frame = QRect(center[0] - outer_radius, center[1] - outer_radius, outer_radius*2, outer_radius*2)

        inner_radius = 200
        inner_circle_frame = QRect(center[0] - inner_radius, center[1] - inner_radius, inner_radius*2, inner_radius*2)

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
