import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon, QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QCoreApplication, QRect #, QPoint, QSize

class App(QWidget):

    def __init__(self):
        super().__init__()

        self.screen = QCoreApplication.instance().primaryScreen().availableGeometry()
        self.x_adjust = int(self.screen.width() * 0.1)
        self.y_adjust = int(self.screen.height() * 0.1)
        self.width = self.screen.width() - self.x_adjust
        self.height = self.screen.height() - self.y_adjust

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Voice Vis 0.1')

        #self.setWindowFlags(Qt.CustomizeWindowHint)
        #self.setWindowFlags(Qt.FramelessWindowHint)

        self.setGeometry(int(self.x_adjust / 2), int(self.y_adjust / 2), self.width, self.height)
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
        num_points_on_circle = 12
        span_angle = int(360 / num_points_on_circle)
        offset = int(0.5 * span_angle)
        points_on_circle = [(p * span_angle) + offset for p in range(num_points_on_circle)]

        frst_radius = int(self.height / 3)
        scnd_radius = int(frst_radius * 2 / 3)
        thrd_radius = int(frst_radius * 1 / 3)

        vis_centerX = int(self.width / 4)
        vis_centerY = int(self.height / 2)

        frst_frame = QRect(vis_centerX - frst_radius, vis_centerY - frst_radius, frst_radius*2, frst_radius*2)
        scnd_frame = QRect(vis_centerX - scnd_radius, vis_centerY - scnd_radius, scnd_radius*2, scnd_radius*2)
        thrd_frame = QRect(vis_centerX - thrd_radius, vis_centerY - thrd_radius, thrd_radius*2, thrd_radius*2)

        angle_frac = 16 # angles measured in 16ths when drawing
        painter.setPen(Qt.white)

        for p in points_on_circle:
            painter.setBrush(QColor(148, 141, 179))
            painter.drawPie(frst_frame, p * angle_frac, span_angle * angle_frac)
            painter.setBrush(QColor(96, 88, 133))
            painter.drawPie(scnd_frame, p * angle_frac, span_angle * angle_frac)
            painter.setBrush(QColor(67, 59, 103))
            painter.drawPie(thrd_frame, p * angle_frac, span_angle * angle_frac)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
