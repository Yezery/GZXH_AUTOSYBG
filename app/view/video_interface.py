import os
import re
from PyQt6.QtCore import Qt,QPoint,QEasingCurve,QUrl
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout,QWidget,QFileDialog,QTableWidgetItem,QTableWidget
from qfluentwidgets import SmoothScrollArea,LineEdit,PrimaryPushButton,CaptionLabel,InfoBar,InfoBarPosition,FluentIcon,PushButton,TableWidget,BodyLabel,SwitchButton,StateToolTip,FlowLayout,MaskDialogBase,Action,MessageBox,CardWidget,RoundMenu,MenuAnimationType
from qfluentwidgets.multimedia import VideoWidget
from qfluentwidgets import FluentIcon as FIF
from PyQt6.QtWidgets import QVBoxLayout,QHBoxLayout,QSizePolicy
from common.config import cfg
from view.router_interface import RouterInterface
from components.video.bilibiliLogin import BilibiliLogin
from components.video.videoDownloader import get_downloader

class MoreTableFrame(TableWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parentObject = parent
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # 禁用编辑
        
        self.verticalHeader().hide()  # 隐藏垂直头部
        self.setBorderRadius(8)  # 设置圆角
        self.setBorderVisible(True)  # 显示边框
        self.setColumnCount(5)  # 设置列数
        self.setColumnHidden(0, True)
        self.setRowCount(0)  # 初始行数为 0
        self.setHorizontalHeaderLabels([
            self.tr(""),self.tr('文件大小'), self.tr('文件格式'),self.tr('分辨率'), self.tr('选择下载')
        ])
        # 初始数据
        self.datas = [[]
        ]

        # 设置布局
        layout = QVBoxLayout(self)
        layout.addWidget(self)
        self.horizontalHeader().setStretchLastSection(True)
        

    def update_table_data(self, data):
        """
        动态更新表格内容。
        :param data: 新的二维数组，包含每行的表格数据
        """
        if not data:
            return
        self.setRowCount(len(data))  # 根据数据调整行数
        self.setColumnHidden(0, True)
        for i, row in enumerate(data):
            for j in range(4):  # 填充前 5 列
                self.setItem(i, j, QTableWidgetItem(row[j]))
            # 创建下载按钮并添加到最后一列
            download_button = PushButton("下载")
            download_button_row = QWidget()
            download_button_row.setLayout(QHBoxLayout())
            download_button_row.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
            download_button_row.layout().setContentsMargins(0, 0, 0, 0)
            download_button_row.layout().addWidget(download_button)
            
            # 将行号传递给按钮点击事件
            download_button.clicked.connect(self.on_download_button_clicked)
            self.setCellWidget(i, 4, download_button_row)  
        
    def on_download_button_clicked(self):
        # 获取点击按钮所在行的索引
        button = self.sender()  # 获取发送信号的对象（即按钮）
        row = self.indexAt(button.parent().position()).row()  # 获取该按钮所在的行索引
        if self.parentObject.stateTooltip is not None:
            InfoBar.warning(
            title='警告',
            content="有任务在进行中，请等待任务完成后再进行下载",
            orient=Qt.Orientation.Horizontal,
            isClosable=False,   # disable close button
            position=InfoBarPosition.BOTTOM,
            duration=2000,
            parent=self.parentObject.parentWidget().parentWidget()
            )
            return
        self.parentObject.stateTooltip = StateToolTip('正在下载视频中', '请耐心等待哦～', self.parentObject.parentWidget().parentWidget())
        self.parentObject.stateTooltip.move(self.parentObject.parentWidget().parentWidget().geometry().bottomLeft() - QPoint(-585,150))
        self.parentObject.stateTooltip.show()
        self.parentObject.downloader.download_video(self.parentObject.video_input.text(),self.item(row, 0).text())

class BestTableFrame(TableWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parentObject = parent
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # 禁用编辑
        self.verticalHeader().hide()  # 隐藏垂直头部
        self.setBorderRadius(8)  # 设置圆角
        self.setBorderVisible(True)  # 显示边框
        self.setColumnCount(6)  # 设置列数
        self.setColumnHidden(0, True)
        self.setRowCount(0)  # 初始行数为 0
        self.setHorizontalHeaderLabels([
            self.tr(""),self.tr('文件大小'), self.tr('分辨率'),self.tr('文件格式'),self.tr('描述'), self.tr('选择下载')
        ])
        # 初始数据
        self.datas = [[]
        ]

        # 设置布局
        layout = QVBoxLayout(self)
        layout.addWidget(self)
        self.horizontalHeader().setStretchLastSection(True)

        
    def update_table_data(self, data):
        """
        动态更新表格内容。
        :param data: 新的二维数组，包含每行的表格数据
        """
        if not data:
            return
        self.setRowCount(len(data))  # 根据数据调整行数
        
        for i, row in enumerate(data):
            for j in range(5): 
                self.setItem(i, j, QTableWidgetItem(row[j]))
            
            # 创建下载按钮并添加到最后一列
            download_button = PushButton("下载")
            download_button_row = QWidget()
            download_button_row.setLayout(QHBoxLayout())
            download_button_row.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
            download_button_row.layout().setContentsMargins(0, 0, 0, 0)
            download_button_row.layout().addWidget(download_button)
            
            # 将行号传递给按钮点击事件
            download_button.clicked.connect(self.on_download_button_clicked)
            self.setCellWidget(i, 5, download_button_row) 



    def on_download_button_clicked(self):
        # 获取点击按钮所在行的索引
        button = self.sender()  # 获取发送信号的对象（即按钮）
        row = self.indexAt(button.parent().pos()).row()  # 获取该按钮所在的行索引
        if self.parentObject.stateTooltip is not None:
            InfoBar.warning(
            title='警告',
            content="有任务在进行中，请等待任务完成后再进行下载",
            orient=Qt.Orientation.Horizontal,
            isClosable=False,   # disable close button
            position=InfoBarPosition.BOTTOM,
            duration=2000,
            parent=self.parentObject.parentWidget().parentWidget()
            )
            return
        self.parentObject.stateTooltip = StateToolTip('正在下载视频中', '请耐心等待哦～', self.parentObject.parentWidget().parentWidget())
        self.parentObject.stateTooltip.move(self.parentObject.parentWidget().parentWidget().geometry().bottomLeft() - QPoint(-585,150))
        self.parentObject.stateTooltip.show()
        self.parentObject.downloader.download_video(self.parentObject.video_input.text(),self.item(row, 0).text(),True)

class VideoMessageBox(MaskDialogBase):
    def __init__(self, parent=None,fileName=None):
        super().__init__(parent)
        # 创建布局
        # self.setLayout() = QVBoxLayout(self)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().setContentsMargins(0, 0, 0, 0)
        # VideoWidget
        self.videoWidget = VideoWidget(self)
        self.videoWidget.setVideo(QUrl.fromLocalFile(f"{cfg.get(cfg.downloadFolder)}"+f"/{fileName}")) 
        self.videoWidget.setFixedSize(700, 500)
        self.layout().addWidget(self.videoWidget)

        self.videoWidget.play()

    def mousePressEvent(self, event):
        """ 处理鼠标点击事件，点击对话框外部时关闭 """
        try:
            # 将 event.position() 转换为 QPoint
            mouse_pos = event.position().toPoint()

            if not self.videoWidget.geometry().contains(mouse_pos):
                self.close()  # 点击透明遮罩部分关闭对话框
            else:
                super().mousePressEvent(event)
        except Exception as e:
            print(f"Error: {e}")
            pass


    def resizeEvent(self, event):
        """ 窗口大小调整时手动设置 videoWidget 的位置 """
        super().resizeEvent(event)
        if self.videoWidget:
            # 确保 videoWidget 居中
            videoWidgetX = (self.width() - self.videoWidget.width()) // 2
            videoWidgetY = (self.height() - self.videoWidget.height()) // 2
            self.videoWidget.move(videoWidgetX, videoWidgetY)
        
class VideoReusltItem(CardWidget):
    def __init__(self, parent,fileName):
        super().__init__(parent)
        self.fileName = fileName
        self.setBorderRadius(6)
        # self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.clicked.connect(self.createCommandBarFlyout)
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_parts = fileName.split('.')  # 分割文件名和扩展名
        base_name = name_parts[0]  # 获取文件名部分（去掉扩展名）
        self.layout().addWidget(BodyLabel(base_name, self))

    def showVideoDialog(self):
        w = VideoMessageBox(self.window(),self.fileName)
        w.exec()
    def createCommandBarFlyout(self):
        menu = RoundMenu(parent=self)
        menu.addAction(Action(FIF.VIEW, self.tr('查看视频'), triggered=self.showVideoDialog))
        menu.addAction(Action(FIF.DELETE, self.tr('删除视频'), triggered=self.deleteVideo))
        x = self.width()  # 获取当前组件的宽度
        pos = self.mapToGlobal(QPoint(x-60, -30))
        menu.exec(pos, aniType=MenuAnimationType.DROP_DOWN)

    def deleteVideo(self):
        """ 删除视频文件 """
        reply = MessageBox('删除视频', '确定要删除该视频吗？', self.window())
        reply.yesButton.setText(self.tr('是'))
        reply.cancelButton.setText(self.tr('取消'))
        if reply.exec():
            try:
                os.remove(f"{cfg.get(cfg.downloadFolder)}/{self.fileName}")
            except:
                pass
            self.deleteLater()
            self.parent().flowLayout.removeWidget(self)
            self.parent().flowLayout.update()
        

class VideoResultWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.download_result_widget = SmoothScrollArea(self)
        self.download_result_widget.setVisible(False)

        self.flowLayout = FlowLayout(self, needAni=True)
        self.flowLayout.setAnimation(250, QEasingCurve.Type.OutQuad)
        self.flowLayout.setContentsMargins(10, 10, 10, 10)
        self.refreshItem()
    

    def refreshItem(self):
        self.flowLayout.removeAllWidgets()
        """ 添加视频项目到布局 """
        # 获取文件夹下的所有视频文件
        video_files = self.get_video_files(cfg.get(cfg.downloadFolder))

        for video_file in video_files:
            item = VideoReusltItem(self, video_file)
            self.flowLayout.addWidget(item)
            
    def get_video_files(self, folder_path):
        """ 获取指定文件夹下的所有视频文件 """
        video_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(('.mp4', '.avi', '.mkv')):  # 可根据需要添加更多视频格式
                    video_files.append(file)
        return video_files
    

class VideoInterface(RouterInterface):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.downloader = get_downloader()
        self.setObjectName('VideoInterface')
        self.__initWidget()
        self.__initLayout()
        self.stateTooltip =None
    def __initWidget(self):
        # 创建主布局
        self.main_layout = QHBoxLayout(self)

        # 在左侧滚动区域中放置一个 QWidget 作为容器
        self.left_widget = SmoothScrollArea(self)
        
        # 创建左侧内容布局
        self.MoretableFrame = MoreTableFrame(self)
        self.MoretableFrame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.BestTableFrame = BestTableFrame(self)
        self.BestTableFrame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # 将布局设置为left_widget的内容
        left_container = QWidget(self)
        left_layout = QVBoxLayout(left_container)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        left_container.setContentsMargins(10, 0, 10, 0)
        self.left_widget.setWidget(left_container)  # 设置可以滚动的区域

        self.bilibiliLogin = BilibiliLogin(self)

        # 创建输入框
        self.searcher = QWidget(self)
        self.searcher.setLayout(QHBoxLayout())
        self.video_input = LineEdit(self)
        self.video_input.setPlaceholderText("请输入视频链接")
        self.video_btn = PrimaryPushButton("搜索", self)
        self.video_btn.setDisabled(True)

        # 创建右侧区域
        self.videoResultWidget = VideoResultWidget(self)
        
        self.savePath = CaptionLabel(f"{cfg.get(cfg.downloadFolder)}", self)
        self.saveBtn = PushButton("选择保存路径", self)
        

        self.searcher.layout().addWidget(self.video_input)
        self.searcher.layout().addWidget(self.video_btn)
        self.searcher.layout().addWidget(self.bilibiliLogin)
        # 添加左侧内容布局
        left_layout.addWidget(self.searcher)
        left_layout.addWidget(self.BestTableFrame)
        self.more_switch = SwitchButton(self.tr('查看更多'))
        self.tool_group = QWidget(self)
        self.tool_group.setLayout(QHBoxLayout())
        self.tool_group.layout().addWidget(self.more_switch)
        self.saveBtn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.savePath.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.tool_group.layout().addWidget(self.savePath)
        self.tool_group.layout().addWidget(self.saveBtn)
        left_layout.addWidget(self.tool_group)
        self.more_label = BodyLabel("音频 视频分离", self)
        left_layout.addWidget(self.more_label)
        left_layout.addWidget(self.MoretableFrame)
        self.more_label.hide()
        self.MoretableFrame.hide()
        left_layout.addWidget(self.videoResultWidget)
        # 将左侧和右侧区域添加到主布局
        self.main_layout.addWidget(self.left_widget)
        # self.main_layout.addWidget(self.right_widget, 1)



        infoBar = InfoBar(
            icon=FluentIcon.PIN,
            title=self.tr('支持'),
            content=self.tr("只支持下载 Bilibili、YouTube 视频"),
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            duration=-1,
            position=InfoBarPosition.BOTTOM_RIGHT,
            parent=self.left_widget
        )
        infoBar.setCustomBackgroundColor("white", "#2a2a2a")

        self.video_input.textChanged.connect(self.rePath)
        self.saveBtn.clicked.connect(self.select_save_path)
        self.video_btn.clicked.connect(self.get_download_video)
        self.more_switch.checkedChanged.connect(self.onSwitchCheckedChanged)
        self.downloader.progress.connect(self.update_progress)
    
    def update_progress(self, progress):
        if progress:
            if self.stateTooltip:
                self.stateTooltip.setContent('下载完成啦 😆')
                self.stateTooltip.setState(True)
                self.stateTooltip = None
                self.videoResultWidget.refreshItem()
        else:
            if self.stateTooltip:
                self.stateTooltip.setContent(f'下载失败了 😭')
                self.stateTooltip.setState(True)
                self.stateTooltip = None

    def onSwitchCheckedChanged(self, isChecked):
        if isChecked:
            self.more_switch.setText(self.tr('查看更多'))
            self.more_label.show()
            self.MoretableFrame.show()
        else:
            self.more_switch.setText(self.tr('关闭更多'))
            self.more_label.hide()
            self.MoretableFrame.hide()
            
            
    def rePath(self):
        # 匹配 Bilibili 或 YouTube 的视频链接
        match = re.search(r"(BV[1-9A-Za-z]{10}|https://www\.youtube\.com/watch\?v=[\w-]{11})", self.video_input.text())
        if match:
            self.video_btn.setDisabled(False)
        else:
            self.video_btn.setDisabled(True)

    def get_download_video(self):
        best,more = self.downloader.get_download_video_list(self.video_input.text())
        self.BestTableFrame.update_table_data(best)
        self.MoretableFrame.update_table_data(more)
        self.BestTableFrame.updateGeometry()  
        self.BestTableFrame.viewport().update()
        
    def __initLayout(self):
        # self.left_widget.setAutoFillBackground(True)
        self.left_widget.enableTransparentBackground()
        self.left_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.left_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.left_widget.setViewportMargins(0, 0, 0, 0)
        self.left_widget.setWidgetResizable(True)
        self.left_widget.setAlignment(Qt.AlignmentFlag.AlignTop)

        # self.right_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        # self.right_widget.setStyleSheet("background:transparent;border:none;")
        # self.right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # self.right_layout.setContentsMargins(0,0, 0, 0)

        # self.bilibiliLogin.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
    def select_save_path(self):
        """选择保存路径"""
        save_path = QFileDialog.getExistingDirectory(self, "选择保存路径")
        if save_path!= "":  # 只有用户选择路径时才更新
            self.savePath.setText(save_path)
            cfg.set(cfg.downloadFolder, save_path)
