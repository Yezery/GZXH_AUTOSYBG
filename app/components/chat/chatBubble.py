from qfluentwidgets import IndeterminateProgressBar,BodyLabel,SwitchButton
from PyQt6.QtWidgets import QWidget,QVBoxLayout,QSizePolicy,QFrame,QTextBrowser,QHBoxLayout
from PyQt6.QtCore import Qt

class ThinkBubble(QTextBrowser):
    def __init__(self,parent):
        super().__init__(parent)
        # 设置文字大小
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,  # 水平方向
            QSizePolicy.Policy.Fixed  # 垂直方向
        )
        self.setFixedHeight(0)
        self.setFixedWidth(0)
        # 隐藏边框
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setStyleSheet("background-color: transparent; color: gray; border-radius: 10px; padding: 10px;")
        self.document().contentsChanged.connect(lambda:adjust_size(self))
             

class MarkdownBubble(QTextBrowser):
    def __init__(self,parent):
        super().__init__(parent)
        # 设置文字大小
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,  # 水平方向
            QSizePolicy.Policy.Fixed  # 垂直方向
        )
        self.setFixedHeight(0)
        self.setFixedWidth(0)
        # 隐藏边框
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setStyleSheet("background-color: #DCDCDC; color: #363636; border-radius: 10px; padding: 10px;")
        self.document().contentsChanged.connect(lambda:adjust_size(self,80))
        
class ChatBubble(QWidget):
    def __init__(self,parent, userName, message=None):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.tip = QWidget(self)
        self.thinkBubble = ThinkBubble(self)
        self.chat_view = MarkdownBubble(self)
        self.inProgressBar = IndeterminateProgressBar(self)
        self.showThink = SwitchButton()
        self.showThink.setChecked(False)
        
        chat_box=QWidget(self)
        chat_box.setSizePolicy(
            QSizePolicy.Policy.Expanding,  # 水平方向
            QSizePolicy.Policy.Fixed  # 垂直方向
        )
        chat_box.setLayout(QHBoxLayout())
        chat_box.layout().addWidget(self.chat_view)
        chat_box.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)
        
    
        
        
        
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        
        
        self.showThink.setOffText("查看思考")
        self.showThink.setOnText("隐藏思考")
        
        self.tip.setFixedWidth(200)
        self.tip.setLayout(QVBoxLayout())
        self.layout().addWidget(self.showThink)
        self.tip.layout().addWidget(BodyLabel("正在思考..."))
        self.tip.layout().addWidget(self.inProgressBar)
        match userName:
            case "GEN":
                self.inProgressBar.show()
                self.layout().addWidget(self.showThink)
                if message:
                    self.showThink.deleteLater()
                    self.thinkBubble.deleteLater()
                    self.tip.deleteLater()
                    self.chat_view.setMarkdown(message)
                    adjust_size(self.chat_view,50,380)
                    self.inProgressBar.deleteLater()
            case "USER":
                self.chat_view.setStyleSheet("background-color: #3879FF; color: white; border-radius:10px; padding: 10px;")
                chat_box.layout().setAlignment(Qt.AlignmentFlag.AlignRight)
                self.thinkBubble.deleteLater()
                self.showThink.deleteLater()
                self.tip.deleteLater()
                self.chat_view.setMarkdown(message)
                adjust_size(self.chat_view,80,580)
            case _:
                pass
        self.layout().addWidget(self.tip)
        self.layout().addWidget(self.thinkBubble)
        self.layout().addWidget(chat_box)
        self.thinkBubble.hide()
        self.showThink.checkedChanged.connect(lambda checked:self.thinkBubble.setVisible(checked))
        self.message_buffer = ""
        self.in_code_block = False
        self.finish_think_tag = False
        
    def addMessage(self, chunk):
            # 处理特殊标签
            if chunk in {"<think>", "</think>"}:
                self._handle_tag(chunk)
            else:
                # 普通消息直接追加到缓冲区
                self.message_buffer += chunk

            # 更新显示内容
            if not self.finish_think_tag:
                self.thinkBubble.setPlainText(self.message_buffer)
            else:
                self.chat_view.setPlainText(self.message_buffer)
                
    def _handle_tag(self, tag):
        """统一处理标签逻辑"""
        if tag == "<think>":
            # 处理 <think> 标签
            return  # 暂时不需要处理
        elif tag == "</think>":
            # 处理 </think> 标签
            self.finish_think_tag = True
            if self.tip:
                self.tip.deleteLater()
            self.thinkBubble.document().contentsChanged.disconnect()
            self.message_buffer = ""
            self.thinkBubble.toPlainText().replace("</think>", "")
            self.thinkBubble.setMarkdown(self.thinkBubble.toPlainText())
            if self.thinkBubble.toPlainText() == "":
                self.thinkBubble.deleteLater()
                self.showThink.deleteLater()
                self.thinkBubble = None
        
 #    1.9和1.11谁大
        
    def __init_widgets__(self):
       pass
    def add_code_area(self):
        pass
def adjust_size(bubble:QTextBrowser,h=20,w=45):
    """根据内容动态调整高度和长度"""
    # 获取文档的理想高度和宽度
    document = bubble.document()
    document_height = document.size().height()
    document_width = document.idealWidth()
    # 设置控件高度
    bubble.setFixedHeight(int(document_height) + h)  # 添加一些边距
    # 设置控件长度
    max_width = 756  # 最大长度
    if document_width > max_width:
        return
    else:
        bubble.setFixedWidth(int(document_width) + w)  # 添加一些边距