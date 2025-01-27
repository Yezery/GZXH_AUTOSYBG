
from view.router_interface import RouterInterface
from qfluentwidgets import TransparentPushButton,TextEdit,SmoothScrollArea,IndeterminateProgressBar,CardWidget
from PyQt6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QSizePolicy
from utils import AI
from qfluentwidgets import FluentIcon as FIF
from PyQt6.QtCore import Qt
from components.chat.chatBubble import ChatBubble
class ChatInterface(RouterInterface):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chat_worker = None  # 保存线程对象
        self.current_bubble = None  # 当前正在更新的气泡
        self.init_ui()
        self.history = []
    def init_ui(self):
        # 初始化界面组件
        self.mainWidget = QWidget(self)
        self.mainWidget.setStyleSheet("QWidget{background: transparent}")
        self.setObjectName("chat_interface")

        # 输入区域
        self.inputGroup = QWidget(self)
        self.inputGroupLayout = QHBoxLayout(self.inputGroup)  # 设置布局
        self.send_btn = TransparentPushButton("发 送",self,FIF.SEND,)
        self.send_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.question = TextEdit(self)
        
        # 将输入组件添加到输入区域
        
        self.inputGroupLayout.addWidget(self.question)
        self.inputGroupLayout.addWidget(self.send_btn)

        # 历史消息区域
        self.historyContainerScrollArea = SmoothScrollArea(self)
        self.historyContainerScrollArea.setWidgetResizable(True)  # 允许内容调整大小
        self.historyContainerScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.historyContainerScrollArea.setViewportMargins(0, 0, 0, 0)

        self.historyContainer = QWidget(self)
        self.historyContainerLayout = QVBoxLayout(self.historyContainer)  # 设置布局
        self.historyContainerLayout.setAlignment(Qt.AlignmentFlag.AlignTop)  # 顶部对齐

        # 将历史消息容器添加到滚动区域
        self.historyContainerScrollArea.setWidget(self.historyContainer)

        # 主布局
        main_layout = QVBoxLayout(self.mainWidget)
        main_layout.setSpacing(0)  # 设置间距

        
        
        self.stop_ai_work_box = QWidget(self)
        self.stop_ai_work_btn = TransparentPushButton("停 止",self,FIF.PAUSE)
        self.stop_ai_work_box.hide()
        self.stop_ai_work_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Maximum)
        self.stop_ai_work_box.setLayout(QHBoxLayout())
        self.stop_ai_work_box.layout().addWidget(self.stop_ai_work_btn)
        
        # 添加滚动区域和输入区域到主布局
        main_layout.addWidget(self.historyContainerScrollArea, 9)  # 历史消息区域占 9 份
        # main_layout.addWidget(self.stop_ai_work_box,1)  # 输入区域占 1 份
        main_layout.addWidget(self.inputGroup, 1)  # 输入区域占 1 份

        # 设置主布局
        self.setWidget(self.mainWidget)
        self.historyMessage = []

        self.helloBubble()
        
        self.stop_ai_work_btn.clicked.connect(self.stop_ai_work)
        # 信号连接
        self.send_btn.clicked.connect(self.send_AI)
        
        self.scroll_bar = self.verticalScrollBar()  # 获取垂直滚动条
    
    def stop_ai_work(self):
        if self.chat_worker and self.chat_worker.isRunning():
            # self.stop_ai_work_box.hide()
            # self.chat_worker.terminate()
            self.history.pop()
            self.chat_worker =None
            
    def send_AI(self):
        if self.question.toPlainText() == "":
            return
        self.scrool2bottom()
        # 创建用户气泡
        # 如果已有线程运行则先停止
        if self.chat_worker and self.chat_worker.isRunning():
            self.chat_worker.stop()
        self.createUserBubble()
        
        self.createAIBubble()
       
        # 创建并启动线程
        self.chat_worker = AI.ChatWorker(self.question.toPlainText(),self.history)
        self.chat_worker.update_chunk.connect(self.update_bubble_content)
        self.chat_worker.finished.connect(self.on_thread_finished)
        self.chat_worker.error.connect(self.on_thread_error)
        self.chat_worker.start()
        self.send_btn.setEnabled(False)
        # self.stop_ai_work_box.show()
        # 清空输入框
        self.question.clear()
        

    def helloBubble(self):
        current_bubble = ChatBubble(self, "GEN", "你好呀～ 我是你的AI智能助手 GEN，有什么问题都可以问我哦！")
        self.historyMessage.append(current_bubble)
        self.historyContainer.layout().addWidget(current_bubble)

    def createUserBubble(self):
        message = self.question.toPlainText()
        current_bubble = ChatBubble(self, "USER", message)
        self.historyMessage.append(current_bubble)
        self.historyContainer.layout().addWidget(current_bubble)
        
    def createAIBubble(self):
        self.current_bubble = ChatBubble(self, "GEN")
        self.historyMessage.append(self.current_bubble)
        self.historyContainer.layout().addWidget(self.current_bubble)
        
    def update_bubble_content(self, chunk):
        self.scrool2bottom()
        """实时更新气泡内容"""
        if self.current_bubble:
            self.current_bubble.addMessage(chunk)
       
    def scrool2bottom(self):
        scroll_bar = self.historyContainerScrollArea.verticalScrollBar()  # 获取垂直滚动条
        scroll_bar.setValue(scroll_bar.maximum())
        
    def on_thread_finished(self):
        """线程完成后的清理"""
        self.current_bubble.chat_view.document().contentsChanged.disconnect()
        self.history.append({"role": "assistant", "content": self.current_bubble.chat_view.toPlainText()})
        self.current_bubble.chat_view.setMarkdown(self.current_bubble.chat_view.toPlainText())
        self.stop_ai_work_box.hide()
        if self.chat_worker and self.chat_worker.isRunning():
            self.chat_worker.stop()
        self.send_btn.setEnabled(True)
        self.chat_worker = None
        self.current_bubble = None

    def on_thread_error(self, error_msg):
        """错误处理"""
        print(f"Error: {error_msg}")
        if self.current_bubble:
            self.current_bubble.chat_view.setPlainText(f"错误: {error_msg}")
        self.chat_worker = None
        self.current_bubble = None

    def closeEvent(self, event):
        """窗口关闭时强制停止线程"""
        if self.chat_worker and self.chat_worker.isRunning():
            self.chat_worker.stop()
            self.chat_worker.wait()
        event.accept()