from qfluentwidgets import SettingCard,LineEdit
from PyQt5.QtCore import Qt
from common.config import cfg
# class NameCard(SettingCard):    

#     def __init__(self, title,parent=None):
#         super().__init__(FIF.DICTIONARY, title,cfg.get(cfg.userName), parent)
#         self.nameEdit = LineEdit(self)
#         self.hBoxLayout.addWidget(self.nameEdit, 0, Qt.AlignRight)
#         self.hBoxLayout.addSpacing(16)
#         self.nameEdit.setText(cfg.get(cfg.userName))
#         self.nameEdit.setPlaceholderText("请输入姓名")
#         self.nameEdit.setFixedWidth(200)
#         self._onNameEditChanged(cfg.get(cfg.userName))
#         self.nameEdit.textChanged.connect(self._onNameEditChanged)

#     def _onNameEditChanged(self, text):
#         cfg.set(cfg.userName, text)
#         if text != "":
#             self.setContent(cfg.get(cfg.userName))
#         else:
#             self.setContent("未设置")

# class IdCard(SettingCard):    

#     def __init__(self,title, parent=None):
#         super().__init__(FIF.FINGERPRINT, title, cfg.get(cfg.userId), parent)
#         self.idEdit = LineEdit(self)
#         self.hBoxLayout.addWidget(self.idEdit, 0, Qt.AlignRight)
#         self.hBoxLayout.addSpacing(16)
#         self.idEdit.setText(cfg.get(cfg.userId))
#         self.idEdit.setPlaceholderText("请输入学号")
#         self.idEdit.setFixedWidth(200)
#         self._onIdEditChanged(cfg.get(cfg.userId))
#         self.idEdit.textChanged.connect(self._onIdEditChanged)
        
#     def _onIdEditChanged(self, text):
#         cfg.set(cfg.userId, text)
#         if text != "":
#             self.setContent(cfg.get(cfg.userId))
#         else:
#             self.setContent("未设置")

# class CourseCard(SettingCard):    

#     def __init__(self,title, parent=None):
#         super().__init__(FIF.CERTIFICATE, title, cfg.get(cfg.userCourse), parent)
#         self.courseEdit = LineEdit(self)
#         self.hBoxLayout.addWidget(self.courseEdit, 0, Qt.AlignRight)
#         self.hBoxLayout.addSpacing(16)
#         self.courseEdit.setText(cfg.get(cfg.userCourse))
#         self.courseEdit.setPlaceholderText("请输入学号")
#         self.courseEdit.setFixedWidth(200)
#         self._onIdEditChanged(cfg.get(cfg.userCourse))
#         self.courseEdit.textChanged.connect(self._onIdEditChanged)
        
#     def _onIdEditChanged(self, text):
#         cfg.set(cfg.userCourse, text)
#         if text != "":
#             self.setContent(cfg.get(cfg.userCourse))
#         else:
#             self.setContent("未设置")

class CoustomCard(SettingCard):
    def __init__(self, icon, title, config_key, placeholder_text, parent=None):
        """
        初始化一个通用的自定义卡片。
        :param icon: 图标类型。
        :param title: 卡片标题。
        :param config_key: 配置项的键。
        :param placeholder_text: 输入框的占位符。
        :param parent: 父组件。
        """
        super().__init__(icon, title, cfg.get(config_key), parent)
        self.config_key = config_key
        self.edit = LineEdit(self)
        self.hBoxLayout.addWidget(self.edit, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.edit.setText(cfg.get(config_key))
        self.edit.setPlaceholderText(placeholder_text)
        self.edit.setFixedWidth(200)
        self._onEditChanged(cfg.get(config_key))
        self.edit.textChanged.connect(self._onEditChanged)

    def _onEditChanged(self, text):
        cfg.set(self.config_key, text)
        if text != "":
            self.setContent(cfg.get(self.config_key))
        else:
            self.setContent("未设置")
