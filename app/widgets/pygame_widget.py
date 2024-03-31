from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QImage, QPixmap, QPainter

from PyQt5.QtWidgets import QWidget


class PygameWidget(QWidget):
    def __init__(self, parent=None):
        super(PygameWidget, self).__init__(parent)
        self.setMinimumSize(400, 300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.surface = None

    def set_surface(self, surface):
        self.surface = surface
        self.update()

    def paintEvent(self):
        if self.surface:
            image = QImage(self.surface.get_buffer().raw, self.surface.get_width(), self.surface.get_height(),
                           QImage.Format_RGB32)
            pixmap = QPixmap.fromImage(image)
            painter = QPainter(self)
            painter.drawPixmap(0, 0, self.width(), self.height(), pixmap)