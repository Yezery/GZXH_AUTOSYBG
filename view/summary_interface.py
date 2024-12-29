from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout,QApplication,QSizePolicy
from PyQt5.QtCore import Qt,pyqtSlot
from qfluentwidgets import TextEdit,PrimaryPushButton,CardWidget,PushButton,pyqtSignal
from components.DropFileUpload import DropFileUploadDOCX
from docx.document import Document as DocumentObject
class SummaryInterface(CardWidget):
    gen_signal = pyqtSignal() 
    isUpload = pyqtSignal(bool)
    docx_emit = pyqtSignal(DocumentObject)
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setObjectName(text.replace(' ', '-'))

        # 主布局
        main_layout = QVBoxLayout()
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 上传文件部分（水平布局）
        upload_layout = QHBoxLayout()
        self.upload_input = None
        if QApplication.activeWindow()==self.parent:
            if self.upload_input is None:
                self.upload_input = DropFileUploadDOCX(self)
            else:
                self.upload_input.deleteLater()
        else:
            if self.upload_input is None:
                self.upload_input = DropFileUploadDOCX(self.parent)
            else:
                self.upload_input.deleteLater()
          
        # self.upload_input.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        # upload_layout.setAlignment(self.upload_input, Qt.AlignLeft)


        # 调整大小策略和高度
        # upload_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # upload_label.setFixedHeight(30)
        self.upload_input.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        # self.upload_input.setMinimumHeight(30)

        # upload_layout.addWidget(upload_label)
        upload_layout.addWidget(self.upload_input, stretch=1)

        # AI 心得部分（垂直布局）
        summary_layout = QVBoxLayout()
        summary_layout.setAlignment(Qt.AlignTop)
        # summary_label = BodyLabel("AI 心得：")
        self.summary_text = TextEdit()
        # self.summary_text.setFixedHeight(300)
        self.summary_text.setPlaceholderText("在此修改或编辑 AI 总结的内容")

        # 调整大小策略
        # summary_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # summary_label.setFixedHeight(30)

        # summary_layout.addWidget(summary_label)
        summary_layout.addWidget(self.summary_text)

        # 按钮部分（水平布局）
        button_layout = QHBoxLayout()
        # button_layout.addStretch()
        self.copy_button = PushButton("复制")
        self.submit_button = PrimaryPushButton("生成")

        # # 调整按钮的大小策略
        # self.copy_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.submit_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.submit_button)

        # 嵌套布局到主布局
        main_layout.addLayout(upload_layout)
        main_layout.addLayout(summary_layout)
        main_layout.addLayout(button_layout)

        self.copy_button.clicked.connect(self.copy_summary)
        self.submit_button.clicked.connect(self.trigger_drop_upload)
        self.submit_button.setDisabled(True)

        # 将主布局设置为窗口的布局
        self.setLayout(main_layout)

        # 信号槽连接
        self.upload_input.ai_summary_generated.connect(self.update_summary)
        self.upload_input.isUpload.connect(self.is_upload)
        self.upload_input.docx_emit.connect(self.c_docx_emit)

    def c_docx_emit(self,docx):
        self.docx_emit.emit(docx)

    def copy_summary(self):
        self.summary_text.selectAll()
        self.summary_text.copy()
    
    @pyqtSlot(str)
    def update_summary(self, summary):
        """更新 AI 总结内容"""
        self.summary_text.setText(summary)
        self.submit_button.setDisabled(False)
        
        
    @pyqtSlot(bool)
    def is_upload(self, r:bool):
        """是否上传文件"""
        self.submit_button.setDisabled(not r)
        self.isUpload.emit(not r)
  

    def trigger_drop_upload(self):
        """按钮点击时发射信号"""
        self.submit_button.setDisabled(True)
        self.upload_input.start_process_signal.emit()  # 发射信号
