import os
import sys
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QFrame,QHBoxLayout,QApplication
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtGui import QIcon
from qfluentwidgets import SubtitleLabel,setFont,MSFluentWindow,NavigationItemPosition,SplashScreen,TeachingTip,TeachingTipTailPosition,TeachingTipView
from utils.AutoUpdater import AutoUpdater
from view.app_interface import AppInterface
from view.setting_interface import SettingInterface
from view.summary_interface import SummaryInterface

class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)
        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))

class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()
        # create sub interface
        self.appInterface = AppInterface("任务",self)
        self.summaryInterface = SummaryInterface("Summary Interface",self)
        self.serviceInterface = Widget('文件转换服务...开发中', self)
        self.settingInterface = SettingInterface('setting Interface',self)
        self.initNavigation()
        self.splashScreen.finish()


    def initNavigation(self):
        self.addSubInterface(self.appInterface, FIF.LABEL, '任务')
        self.addSubInterface(self.summaryInterface, FIF.ROBOT, 'AI心得')
        self.addSubInterface(self.serviceInterface, FIF.TILES, '文档转换')
        

        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', FIF.SETTING, NavigationItemPosition.BOTTOM)

        # 添加自定义导航组件
        self.navigationInterface.addItem(
            routeKey='Help',
            icon=FIF.HELP,
            text='帮助',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.setCurrentItem(self.appInterface.objectName())

    def initWindow(self):
        self.resize(900, 700)
        logo_path = self.resource_path("logo.png")
        self.setWindowIcon(QIcon(logo_path))
        self.setWindowTitle('SYBG-GEN')

        # 1. 创建启动页面
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()
        # 4. 隐藏启动页面
        self.splashScreen.finish()

    def resource_path(self,relative_path):
        """获取资源文件的路径"""
        if getattr(sys, 'frozen', False):  # 检测是否为打包环境
            # PyInstaller 会将资源文件放置在 .app/Contents/Resources 目录（如果是Mac应用）
            base_path = sys._MEIPASS
        else:  # 未打包环境
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


    
    def showMessageBox(self):
            pos = TeachingTipTailPosition.LEFT_BOTTOM
            view = TeachingTipView(
                icon=None,
                title='支持作者🥰',
                content="开发不易，如果这个项目帮助到了您，可以考虑请作者喝一杯咖啡。\n 您的支持就是作者开发和维护项目的动力🚀",
                isClosable=True,
                tailPosition=pos,
            )
            t = TeachingTip.make(view, self.navigationInterface.children()[-1], 3000, pos, self)
            view.closed.connect(t.close)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
    QWidget {
        background-color: white;  
        color: #000000;           
    }
""")

    w = Window()
    w.setMinimumWidth(900)
    w.setMinimumHeight(700)
    w.show()
    #  初始化自动更新器
    updater = AutoUpdater(github_user="yezery", repo_name="GZXH_AUTOSYBG", current_version="v 1.1.1", parent=w)
    # 检测更新
    updater.check_for_update()
    app.exec()
    
