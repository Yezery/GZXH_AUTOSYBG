from PyQt6.QtCore import QPoint, QRect, QSize, Qt
from PyQt6.QtGui import QIcon, QIconEngine, QImage, QPixmap, QPainter
class PixmapIconEngine(QIconEngine):
    """ Pixmap icon engine """

    def __init__(self, iconPath: str):
        self.iconPath = iconPath
        super().__init__()

    def paint(self, painter: QPainter, rect: QRect, mode: QIcon.Mode, state: QIcon.State):
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        painter.drawImage(rect, QImage(self.iconPath))

    def pixmap(self, size: QSize, mode: QIcon.Mode, state: QIcon.State) -> QPixmap:
        pixmap = QPixmap(size)
        pixmap.fill(Qt.GlobalColor.transparent)
        self.paint(QPainter(pixmap), QRect(QPoint(0, 0), size), mode, state)
        return pixmap


class Icon(QIcon):

    def __init__(self, iconPath: str):
        self.iconPath = iconPath
        super().__init__(PixmapIconEngine(iconPath))
