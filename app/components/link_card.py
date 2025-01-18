# coding:utf-8
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap, QDesktopServices
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget, QHBoxLayout

from qfluentwidgets import IconWidget, FluentIcon, TextWrap, SingleDirectionScrollArea
from common.signal_bus import signalBus
from common.style_sheet import StyleSheet


class LinkCard(QFrame):

    def __init__(self, icon, title, content, routeKey,index, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.index = index
        self.routekey = routeKey
        self.setFixedSize(198, 220)
        self.iconWidget = IconWidget(icon, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(TextWrap.wrap(content, 28, False)[0], self)
        self.urlWidget = IconWidget(FluentIcon.LINK, self)

        self.__initWidget()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        signalBus.switchTo.emit(self.routekey, self.index)

    def __initWidget(self):
        self.setCursor(Qt.PointingHandCursor)

        self.iconWidget.setFixedSize(54, 54)
        self.urlWidget.setFixedSize(16, 16)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(24, 24, 0, 13)
        self.vBoxLayout.addWidget(self.iconWidget)
        self.vBoxLayout.addSpacing(16)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(8)
        self.vBoxLayout.addWidget(self.contentLabel)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.urlWidget.move(170, 192)

        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')

class LinkCardView(SingleDirectionScrollArea):
    """ Link card view """

    def __init__(self, parent=None):
        super().__init__(parent, Qt.Orientation.Horizontal)
        self.view = QWidget(self)
        self.hBoxLayout = QHBoxLayout(self.view)

        self.hBoxLayout.setContentsMargins(36, 0, 0, 0)
        self.hBoxLayout.setSpacing(12)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.view.setObjectName('view')
        StyleSheet.LINK_CARD.apply(self)

    def addCard(self, icon, title, content, routeKey, index):
        """ add link card """
        card = LinkCard(icon, title, content, routeKey, index, self.view)
        self.hBoxLayout.addWidget(card, 0, Qt.AlignmentFlag.AlignLeft)
