from qfluentwidgets import ScrollArea
from PyQt5.QtCore import Qt
class RouterInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # self.view = QWidget(self)
        # self.vBoxLayout = QVBoxLayout(self.view)
        self.enableTransparentBackground()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setWidget(self.view)
        self.setWidgetResizable(True)
        # self.vBoxLayout.setSpacing(30)
        # self.vBoxLayout.setAlignment(Qt.AlignTop)
        # self.vBoxLayout.setContentsMargins(36, 20, 36, 36)
        # self.view.setObjectName('view')
