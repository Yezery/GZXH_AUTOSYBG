
from PyQt5.QtWidgets import QHBoxLayout,QFileDialog
from PyQt5.QtCore import Qt
from qfluentwidgets import GroupHeaderCardWidget,ToolButton,PrimaryPushButton,PushButton,LineEdit

from qfluentwidgets import FluentIcon as FIF
from components.Message import createMessage
from task.LoadConfig import get_config

class SettingInterface(GroupHeaderCardWidget):
    def __init__(self,text, parent=None):
        super().__init__(parent)
        self.setObjectName(text.replace(' ', '-'))
        self.setTitle("基本设置")
        self.setBorderRadius(8)
        # 初始化组件
        self.savePathChooseButton = PushButton("选择")
        self.nameEdit = LineEdit()
        self.nameEdit.setPlaceholderText("请输入姓名")
        self.idEdit = LineEdit()
        self.idEdit.setPlaceholderText("请输入学号")
        self.courseEdit = LineEdit()
        self.courseEdit.setPlaceholderText("请输入班级")
        self.apiKeyEdit = LineEdit()
        self.apiKeyEdit.setPlaceholderText("请输入API_KEY")
        self.secretEdit = LineEdit()
        self.secretEdit.setPlaceholderText("请输入SECRET_KEY")
        self.refreshButton = ToolButton(FIF.SYNC)
        self.compileButton = PrimaryPushButton("保存")
        self.bottomLayout = QHBoxLayout()

        # 配置组件样式
        self.init_widgets()
        self.init_layout()

        
        # 初始化系统配置
        self.load_config()

        # 绑定事件
        self.savePathChooseButton.clicked.connect(self.select_save_path)
        self.compileButton.clicked.connect(self.save_to_info)
        self.refreshButton.clicked.connect(self.load_config)


    def load_config(self):
        # 加载系统配置
        self.Config = get_config()
        self.Config.refresh_config()
        self.systemConfig =get_config().config
        self.nameEdit.setText(self.systemConfig["NAME"])
        self.idEdit.setText(self.systemConfig["ID"])
        self.courseEdit.setText(self.systemConfig["COURSE"])
        self.apiKeyEdit.setText(self.systemConfig["API_KEY"])
        self.secretEdit.setText(self.systemConfig["SECRET_KEY"])
        self.savePath.setContent(self.systemConfig["SAVE_PATH"])
        self.NAME.setContent(self.systemConfig["NAME"])
        self.ID.setContent(self.systemConfig["ID"])
        self.COURSE.setContent(self.systemConfig["COURSE"])
        self.APIKEY.setContent(self.systemConfig["API_KEY"])
        self.SECRETKEY.setContent(self.systemConfig["SECRET_KEY"])
        self.savePath.setContent(self.systemConfig["SAVE_PATH"])

    def init_widgets(self):
        """初始化组件默认值和样式"""
        self.savePathChooseButton.setFixedWidth(120)
        for edit in [self.nameEdit, self.idEdit, self.courseEdit, self.apiKeyEdit, self.secretEdit]:
            edit.setFixedWidth(220)

    def init_layout(self):
        """初始化布局"""
        self.bottomLayout.setSpacing(10)
        self.bottomLayout.setContentsMargins(24, 15, 24, 20)
        self.bottomLayout.addStretch(1)
        self.bottomLayout.addWidget(self.refreshButton, 0, Qt.AlignRight)
        self.bottomLayout.addWidget(self.compileButton, 0, Qt.AlignRight)
        self.bottomLayout.setAlignment(Qt.AlignVCenter)
        self.setContentsMargins(16, 16, 16, 16)
        # 添加组件到分组中
        self.NAME =self.addGroup(None, "姓名", "设置姓名", self.nameEdit)
        self.COURSE = self.addGroup(None, "班级", "设置课程名称", self.courseEdit)
        self.ID =self.addGroup(None, "学号", "设置学号", self.idEdit)
        self.APIKEY = self.addGroup(None, "API Key", "设置 API Key", self.apiKeyEdit)
        self.SECRETKEY = self.addGroup(None, "Secret Key", "设置 Secret Key", self.secretEdit)
        self.savePath = self.addGroup(None, "保存路径","", self.savePathChooseButton)

        # 添加底部工具栏
        self.vBoxLayout.addLayout(self.bottomLayout)

    def select_save_path(self):
        """选择保存路径"""
        save_path = QFileDialog.getExistingDirectory(self, "选择保存路径")
        if save_path:  # 只有用户选择路径时才更新
            self.savePath.setContent(save_path)
            


    def save_to_info(self):
        """将输入框的值保存到 JSON 文件中"""
        try:
            # 获取输入框值
            name = self.nameEdit.text().strip()
            config_id = self.idEdit.text().strip()
            course = self.courseEdit.text().strip()
            api_key = self.apiKeyEdit.text().strip()
            secret_key = self.secretEdit.text().strip()
            save_path = self.savePath.contentLabel.text().strip()
            # 检查输入值是否为空
            if not all([name, config_id, course, api_key, secret_key]):
                createMessage(self,title="保存失败", message=f"所有字段都不能为空！",_type=2)
                return

            # 更新系统配置
            self.systemConfig.update({
                "NAME": name,
                "ID": config_id,
                "COURSE": course,
                "API_KEY": api_key,
                "SECRET_KEY": secret_key,
                "SAVE_PATH":  save_path
            })

            self.Config.save_config(self.systemConfig)
            createMessage(self,title="保存成功", message="配置信息已成功保存！",_type=1)

        except Exception as e:
            createMessage(self,title="保存失败", message=f"保存配置信息失败",_type=0)
        finally:
            self.load_config()