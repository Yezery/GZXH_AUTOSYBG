
from PyQt6.QtCore import Qt
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, OptionsSettingCard, PrimaryPushSettingCard,
                            ExpandLayout, CustomColorSettingCard,setTheme, setThemeColor)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QWidget

from view.router_interface import RouterInterface
from utils.AutoUpdater import AutoUpdater
from components.customerCard import CoustomCard
from common.config import cfg, FEEDBACK_URL, AUTHOR, VERSION, YEAR

from qfluentwidgets import FluentIcon as FIF

# class SettingInterface(GroupHeaderCardWidget):
#     def __init__(self,text, parent=None):
#         super().__init__(parent)
#         self.setObjectName(text.replace(' ', '-'))
#         self.setTitle("基本设置")
#         self.setBorderRadius(8)
#         # 初始化组件
#         self.savePathChooseButton = PushButton("选择")
#         self.nameEdit = LineEdit()
#         self.nameEdit.setPlaceholderText("请输入姓名")
#         self.idEdit = LineEdit()
#         self.idEdit.setPlaceholderText("请输入学号")
#         self.courseEdit = LineEdit()
#         self.courseEdit.setPlaceholderText("请输入班级")
#         self.apiKeyEdit = LineEdit()
#         self.apiKeyEdit.setPlaceholderText("请输入API_KEY")
#         self.secretEdit = LineEdit()
#         self.secretEdit.setPlaceholderText("请输入SECRET_KEY")
#         self.tokenEdit = LineEdit()
#         self.tokenEdit.setPlaceholderText("请输入UPDATE_TOKEN")
#         self.download = PushSettingCard(
#             text="选择文件夹",
#             icon=FIF.DOWNLOAD,
#             title="下载目录",
#             content="D:/Users/下载"
#         )
#         self.refreshButton = ToolButton(FIF.SYNC)
#         self.compileButton = PrimaryPushButton("保存")
#         self.bottomLayout = QHBoxLayout()

#         # 配置组件样式
#         self.init_widgets()
#         self.init_layout()

        
#         # 初始化系统配置
#         self.load_config()

#         # 绑定事件
#         self.savePathChooseButton.clicked.connect(self.select_save_path)
#         self.compileButton.clicked.connect(self.save_to_info)
#         self.refreshButton.clicked.connect(self.load_config)


#     def load_config(self):
#         # 加载系统配置
#         self.Config = get_config()
#         self.Config.refresh_config()
#         self.systemConfig =get_config().config
#         self.nameEdit.setText(self.systemConfig["NAME"])
#         self.idEdit.setText(self.systemConfig["ID"])
#         self.courseEdit.setText(self.systemConfig["COURSE"])
#         self.apiKeyEdit.setText(self.systemConfig["API_KEY"])
#         self.secretEdit.setText(self.systemConfig["SECRET_KEY"])
#         self.tokenEdit.setText(self.systemConfig["UPDATE_TOKEN"])



#         self.NAME.setContent(self.systemConfig["NAME"])
#         self.ID.setContent(self.systemConfig["ID"])
#         self.COURSE.setContent(self.systemConfig["COURSE"])
#         self.APIKEY.setContent(self.systemConfig["API_KEY"])
#         self.SECRETKEY.setContent(self.systemConfig["SECRET_KEY"])
#         self.savePath.setContent(self.systemConfig["SAVE_PATH"])
#         self.UPDATE_TOKEN.setContent(self.systemConfig["UPDATE_TOKEN"])

#     def init_widgets(self):
#         """初始化组件默认值和样式"""
#         self.savePathChooseButton.setFixedWidth(120)
#         for edit in [self.nameEdit, self.idEdit, self.courseEdit, self.apiKeyEdit, self.secretEdit,self.tokenEdit]:
#             edit.setFixedWidth(220)

#     def init_layout(self):
#         """初始化布局"""
#         self.bottomLayout.setSpacing(10)
#         self.bottomLayout.setContentsMargins(24, 15, 24, 20)
#         self.bottomLayout.addStretch(1)
#         self.bottomLayout.addWidget(self.refreshButton, 0, Qt.AlignmentFlag.AlignRight)
#         self.bottomLayout.addWidget(self.compileButton, 0, Qt.AlignmentFlag.AlignRight)
#         self.bottomLayout.setAlignment(Qt.AlignVCenter)
#         self.setContentsMargins(16, 16, 16, 16)
#         self.bottomLayout.addWidget(self.download)
#         # 添加组件到分组中
#         self.NAME =self.addGroup(None, "姓名", "设置姓名", self.nameEdit)
#         self.COURSE = self.addGroup(None, "班级", "设置课程名称", self.courseEdit)
#         self.ID =self.addGroup(None, "学号", "设置学号", self.idEdit)
#         self.APIKEY = self.addGroup(None, "API Key", "设置 API Key", self.apiKeyEdit)
#         self.SECRETKEY = self.addGroup(None, "Secret Key", "设置 Secret Key", self.secretEdit)
#         self.UPDATE_TOKEN = self.addGroup(None, "更新 Token", "设置 UPDATE_TOKEN", self.tokenEdit)
#         self.savePath = self.addGroup(None, "保存路径","", self.savePathChooseButton)


#         # 添加底部工具栏
#         self.vBoxLayout.addLayout(self.bottomLayout)

#     def select_save_path(self):
#         """选择保存路径"""
#         save_path = QFileDialog.getExistingDirectory(self, "选择保存路径")
#         if save_path:  # 只有用户选择路径时才更新
#             self.savePath.setContent(save_path)
            


#     def save_to_info(self):
#         """将输入框的值保存到 JSON 文件中"""
#         try:
#             # 获取输入框值
#             name = self.nameEdit.text().strip()
#             config_id = self.idEdit.text().strip()
#             course = self.courseEdit.text().strip()
#             api_key = self.apiKeyEdit.text().strip()
#             secret_key = self.secretEdit.text().strip()
#             save_path = self.savePath.contentLabel.text().strip()
#             update_token = self.tokenEdit.text().strip()

#             # 检查输入值是否为空
#             if not all([name, config_id, course, api_key, secret_key]):
#                 createMessage(self,title="保存失败", message=f"所有字段都不能为空！",_type=2)
#                 return

#             # 更新系统配置
#             self.systemConfig.update({
#                 "NAME": name,
#                 "ID": config_id,
#                 "COURSE": course,
#                 "API_KEY": api_key,
#                 "SECRET_KEY": secret_key,
#                 "SAVE_PATH":  save_path,
#                 "UPDATE_TOKEN": update_token,
#             })

#             self.Config.save_config(self.systemConfig)
#             createMessage(self,title="保存成功", message="配置信息已成功保存！",_type=1)

#         except Exception as e:
#             createMessage(self,title="保存失败", message=f"保存配置信息失败",_type=0)
#         finally:
#             self.load_config()

class SettingInterface(RouterInterface):
    """ Setting interface """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.scrollWidget.setStyleSheet("QWidget{background: transparent}")
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.enableTransparentBackground()
        # base folders
        # self.baseSetting = SettingCardGroup(
        #     self.tr("基本设置"), self.scrollWidget)
        # # self.DownLoadFolderCard = FolderListSettingCard(
        # #     cfg.DownloadFolders,
        # #     self.tr("Local music library"),
        # #     directory=QStandardPaths.writableLocation(
        # #         QStandardPaths.MusicLocation),
        # #     parent=self.baseSetting
        # # )
        # self.nameCard = CoustomCard(FIF.DICTIONARY, self.tr("姓名"), cfg.userName, "请输入姓名", self.baseSetting)
        # self.idCard = CoustomCard(FIF.FINGERPRINT, self.tr("学号"), cfg.userId, "请输入学号", self.baseSetting)
        # self.courseCard = CoustomCard(FIF.CERTIFICATE, self.tr("班级"), cfg.userCourse, "请输入班级", self.baseSetting)
        # self.downloadFolderCard = PushSettingCard(
        #             self.tr('选择文件夹'),
        #             FIF.DOWNLOAD,
        #             self.tr("下载目录"),
        #             cfg.get(cfg.downloadFolder),
        #             self.baseSetting
        #         )
       
        self.proSetting = SettingCardGroup(
            self.tr("高级设置"), self.scrollWidget)
        self.apiKeyCard = CoustomCard(FIF.IOT, self.tr("Api Key"), cfg.apiKey, "请输入Api Key", self.proSetting)
        self.secretKeyCard = CoustomCard(FIF.VPN, self.tr("Secret Key"), cfg.secretKey, "请输入Secret Key", self.proSetting)
        self.apiKeyCard.setDisabled(True)
        self.secretKeyCard.setDisabled(True)

        # personalization
        self.personalGroup = SettingCardGroup(
            self.tr('个性化'), self.scrollWidget)
        # self.micaCard = SwitchSettingCard(
        #     FIF.TRANSPARENT,
        #     self.tr('云母效果'),
        #     self.tr('窗口和表面显示半透明'),
        #     cfg.micaEnabled,
        #     self.personalGroup
        # )
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            self.tr('应用主题'),
            self.tr("调整你的应用的外观"),
            texts=[
                self.tr('浅色'), self.tr('深色'),
                self.tr('跟随系统设置')
            ],
            parent=self.personalGroup
        )
        self.themeColorCard = CustomColorSettingCard(
            cfg.themeColor,
            FIF.PALETTE,
            self.tr('主题色'),
            self.tr('调整你的应用的主题色'),
            self.personalGroup
        )
        self.zoomCard = OptionsSettingCard(
            cfg.dpiScale,
            FIF.ZOOM,
            self.tr("界面缩放"),
            self.tr("调整小部件和字体的大小"),
            texts=[
                "100%", "125%", "150%", "175%", "200%",
                self.tr("跟随系统")
            ],
            parent=self.personalGroup
        )
        # self.languageCard = ComboBoxSettingCard(
        #     cfg.language,
        #     FIF.LANGUAGE,
        #     self.tr('语言'),
        #     self.tr('选择界面所使用的语言'),
        #     texts=['简体中文', 'English', self.tr('跟随系统')],
        #     parent=self.personalGroup
        # )


        # update software
        self.updateSoftwareGroup = SettingCardGroup(
            self.tr("软件更新"), self.scrollWidget)
        self.updateOnStartUpCard = SwitchSettingCard(
            FIF.UPDATE,
            self.tr('在应用程序启动时检查更新'),
            self.tr('新版本将更加稳定并拥有更多功能（建议启用此选项）'),
            configItem=cfg.checkUpdateAtStartUp,
            parent=self.updateSoftwareGroup
        )

        # application
        self.aboutGroup = SettingCardGroup(self.tr('关于'), self.scrollWidget)
        # self.helpCard = HyperlinkCard(
        #     HELP_URL,
        #     self.tr('Open help page'),
        #     FIF.HELP,
        #     self.tr('Help'),
        #     self.tr(
        #         'Discover new features and learn useful tips about PyQt-Fluent-Widgets'),
        #     self.aboutGroup
        # )
        self.feedbackCard = PrimaryPushSettingCard(
            self.tr('提供反馈'),
            FIF.FEEDBACK,
            self.tr('提供反馈'),
            self.tr('通过提供反馈帮助我改进 GEN'),
            self.aboutGroup
        )
        self.aboutCard = PrimaryPushSettingCard(
            self.tr('检查更新'),
            FIF.INFO,
            self.tr('关于'),
            '© ' + self.tr('版权所有') + f" {YEAR}, {AUTHOR}. " +
            self.tr('当前版本') + " " + VERSION,
            self.aboutGroup
        )
        updater=AutoUpdater(self.window())
        self.aboutCard.button.clicked.connect(lambda:updater.check_for_updates())

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 20, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('settingInterface')

        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        # self.settingLabel.setObjectName('settingLabel')
        # StyleSheet.SETTING_INTERFACE.apply(self)

        # self.micaCard.setEnabled(isWin11())

        # initialize layout
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        # self.settingLabel.move(36, 30)

        # add cards to group
        # self.baseSetting.addSettingCard(self.musicFolderCard)
        # self.baseSetting.addSettingCard(self.nameCard)
        # self.baseSetting.addSettingCard(self.courseCard)
        # self.baseSetting.addSettingCard(self.idCard)
        # self.baseSetting.addSettingCard(self.downloadFolderCard)

        self.proSetting.addSettingCard(self.apiKeyCard)
        self.proSetting.addSettingCard(self.secretKeyCard)


        # self.personalGroup.addSettingCard(self.micaCard)
        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.themeColorCard)
        self.personalGroup.addSettingCard(self.zoomCard)
        # self.personalGroup.addSettingCard(self.languageCard)

        # self.materialGroup.addSettingCard(self.blurRadiusCard)

        self.updateSoftwareGroup.addSettingCard(self.updateOnStartUpCard)

        # self.aboutGroup.addSettingCard(self.helpCard)
        self.aboutGroup.addSettingCard(self.feedbackCard)
        self.aboutGroup.addSettingCard(self.aboutCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        # self.expandLayout.addWidget(self.baseSetting)
        self.expandLayout.addWidget(self.proSetting)
        self.expandLayout.addWidget(self.personalGroup)
        # self.expandLayout.addWidget(self.materialGroup)
        self.expandLayout.addWidget(self.updateSoftwareGroup)
        self.expandLayout.addWidget(self.aboutGroup)

    def __showRestartTooltip(self):
        """ show restart tooltip """
        InfoBar.success(
            self.tr('更新成功'),
            self.tr('配置在重启软件后生效'),
            duration=1500,
            parent=self
        )

    # def __onDownloadFolderCardClicked(self):
    #     """ download folder card clicked slot """
    #     folder = QFileDialog.getExistingDirectory(
    #         self, self.tr("选择文件夹"), "./")
    #     if not folder or cfg.get(cfg.downloadFolder) == folder:
    #         return

    #     cfg.set(cfg.downloadFolder, folder)
    #     self.downloadFolderCard.setContent(folder)

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.appRestartSig.connect(self.__showRestartTooltip)

        # self.downloadFolderCard.clicked.connect(
        #     self.__onDownloadFolderCardClicked)

        # personalization
        cfg.themeChanged.connect(setTheme)
        self.themeColorCard.colorChanged.connect(lambda c: setThemeColor(c))
        # self.micaCard.checkedChanged.connect(signalBus.micaEnableChanged)

        # feedback
        self.feedbackCard.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))
        
        # # about
        # self.aboutCard.clicked.connect(
            
        # )