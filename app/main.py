import os
import sys
import webbrowser
from qfluentwidgets import FluentIcon as FIF
from PyQt6.QtWidgets import QFrame,QHBoxLayout,QApplication
from PyQt6.QtCore import Qt,QSize,QTimer
from qfluentwidgets import SubtitleLabel,setFont,MSFluentWindow,NavigationItemPosition,SplashScreen,TeachingTip,TeachingTipTailPosition,TeachingTipView,isDarkTheme
from view.chat_interface import ChatInterface
from utils.AutoUpdater import AutoUpdater
from view.router_interface import RouterInterface
from view.video_interface import VideoInterface
from view.home_interface import HomeInterface
from components.Icon import Icon
from view.sybg_interface import SYBGInterface
from view.setting_interface import SettingInterface
from view.summary_interface import SummaryInterface
from PyQt6.QtGui import QGuiApplication
from common.config import cfg
from common.signal_bus import signalBus
class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)
        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))

class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()
        # self.themeListener = SystemThemeListener(self)
        self.initWindow()
        # create sub interface
        # self.homeInterface = HomeInterface(self)
        self.chatInterface = ChatInterface(self)
        self.sybgInterface = SYBGInterface(self)
        self.summaryInterface = SummaryInterface(1,self)
        # self.serviceInterface = Widget('文件转换服务...开发中', self)
        self.videoInterface =  VideoInterface(self)
        self.settingInterface = SettingInterface(self)
        self.connectSignalToSlot()
        self.initNavigation()
        # self.themeListener.start()
        self.splashScreen.finish()
    
    def connectSignalToSlot(self):
        # signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signalBus.switchTo.connect(self.switchToRouter)
        # signalBus.supportSignal.connect(self.onSupport)

    def initNavigation(self):
        # self.addSubInterface(self.homeInterface, FIF.HOME, '首页')
        self.addSubInterface(self.sybgInterface, FIF.LABEL, '实验报告')
        self.addSubInterface(self.chatInterface, FIF.CHAT, 'GEN')
        self.addSubInterface(self.summaryInterface, FIF.ROBOT, 'AI心得')
        # # self.addSubInterface(self.serviceInterface, FIF.TILES, '文档转换')
        self.addSubInterface(self.videoInterface, FIF.VIDEO, '视频解析')
        

        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', FIF.SETTING, NavigationItemPosition.BOTTOM)

        # 添加自定义导航组件
        self.navigationInterface.addItem(
            routeKey='Help',
            icon=FIF.EXPRESSIVE_INPUT_ENTRY,
            text='帮助',
            onClick=self.toReward,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.setCurrentItem(self.sybgInterface.objectName())

    def initWindow(self):
        self.resize(1000, 800)
        logo_path = cfg.resource_path("images/logo.png")
        self.setWindowIcon(Icon(logo_path))
        self.setWindowTitle('GEN')

        # 1. 创建启动页面
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()
        desktop = QGuiApplication.primaryScreen().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()
        # 4. 隐藏启动页面
        self.splashScreen.finish()
    
    def closeEvent(self, e):
        # self.themeListener.terminate()
        # self.themeListener.deleteLater()
        super().closeEvent(e)

    def _onThemeChangedFinished(self):
        super()._onThemeChangedFinished()

        # retry
        if self.isMicaEffectEnabled():
            QTimer.singleShot(100, lambda: self.windowEffect.setMicaEffect(self.winId(), isDarkTheme()))

    def switchToRouter(self, routeKey, index):
            """ switch to sample """
            interfaces = self.findChildren(RouterInterface)
            for w in interfaces:
                if w.objectName() == routeKey:
                    self.stackedWidget.setCurrentWidget(w, False)
    
    def toReward(self):
            # pos = TeachingTipTailPosition.LEFT_BOTTOM
            # view = TeachingTipView(
            #     icon=None,
            #     title='支持作者🥰',
            #     content="开发不易，如果这个项目帮助到了您，可以考虑请作者喝一杯咖啡。\n 您的支持就是作者开发和维护项目的动力🚀",
            #     isClosable=True,
            #     tailPosition=pos,
            #     image=cfg.resource_path("images/my.jpg")
            # )
            # t = TeachingTip.make(view, self.navigationInterface.children()[-1], 3000, pos, self)
            # view.closed.connect(t.close)
            webbrowser.open("http://www.zivye.asia/zh/support")

if __name__ == '__main__':
    if cfg.get(cfg.dpiScale) == "Auto":
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_Use96Dpi)
    else:
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

    QApplication.setAttribute(Qt.ApplicationAttribute.AA_Use96Dpi)
    
    

    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_Use96Dpi)
    w = Window()
    w.setMinimumWidth(1000)
    w.setMinimumHeight(800)
    w.show()
    if cfg.get(cfg.checkUpdateAtStartUp):
        # 检测更新
        update = AutoUpdater(parent=w)
        update.check_for_updates()
    app.exec()
    
