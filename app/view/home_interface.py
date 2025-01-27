# coding:utf-8
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath, QLinearGradient
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

from qfluentwidgets import SmoothScrollArea, isDarkTheme
from common.style_sheet import StyleSheet
from components.link_card import LinkCardView
from common.config import cfg
class BannerWidget(QWidget):
    """ Banner widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(336)

        self.vBoxLayout = QVBoxLayout(self)
        self.galleryLabel = QLabel('GEN', self)
        self.banner = QPixmap(cfg.resource_path("images/header1.png"))
        self.linkCardView = LinkCardView(self)

        self.galleryLabel.setObjectName('galleryLabel')

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.galleryLabel)
        self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.linkCardView.addCard(
            cfg.resource_path("images/docx.png"),
            self.tr('实验报告生成器'),
            self.tr('一键生成实验报告'),
            routeKey="SYBGInterface",
            index=2
        )
        self.linkCardView.addCard(
            cfg.resource_path("images/docx.png"),
            self.tr('视频解析器'),
            self.tr('Bilibili 视频一键解析下载'),
            routeKey="VideoInterface",
            index=0
        )
        self.linkCardView.addCard(
            cfg.resource_path("images/docx.png"),
            self.tr('心得生成器'),
            self.tr('一键生成心得体会'),
            routeKey="SummaryInterface_1",
            index=3
        )


    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        w, h = self.width(), self.height()
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path.addRect(QRectF(0, h-50, 50, 50))
        path.addRect(QRectF(w-50, 0, 50, 50))
        path.addRect(QRectF(w-50, h-50, 50, 50))
        path = path.simplified()

        # init linear gradient effect
        gradient = QLinearGradient(0, 0, 0, h)

        # draw background color
        if not isDarkTheme():
            gradient.setColorAt(0, QColor(207, 216, 228, 255))
            gradient.setColorAt(1, QColor(207, 216, 228, 0))
        else:
            gradient.setColorAt(0, QColor(0, 0, 0, 255))
            gradient.setColorAt(1, QColor(0, 0, 0, 0))
            
        painter.fillPath(path, QBrush(gradient))

        # draw banner image
        pixmap = self.banner.scaled(
            self.size(), transformMode=Qt.SmoothTransformation)
        painter.fillPath(path, QBrush(pixmap))


class HomeInterface(SmoothScrollArea):
    """ Home interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.enableTransparentBackground()
        self.__initWidget()
        # self.loadSamples()

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('homeInterface')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

    # def loadSamples(self):
    #     """ load samples """
    #     # basic input samples
    #     basicInputView = SampleCardView(
    #         self.tr("Basic input samples"), self.view)
    #     basicInputView.addSampleCard(
    #         icon=":/gallery/images/controls/Button.png",
    #         title="Button",
    #         content=self.tr(
    #             "A control that responds to user input and emit clicked signal."),
    #         routeKey="basicInputInterface",
    #         index=0
    #     )
    #     self.vBoxLayout.addWidget(basicInputView)