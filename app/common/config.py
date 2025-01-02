# coding:utf-8
import os
import sys
from enum import Enum

from PyQt5.QtCore import QLocale
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            OptionsValidator, RangeConfigItem, RangeValidator,
                            Theme, ConfigSerializer)


class Language(Enum):
    """ Language enumeration """

    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    ENGLISH = QLocale(QLocale.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """ Language serializer """

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


class Config(QConfig):
    """ Config of application """

    # base
    userName = ConfigItem("User", "UserName", "")
    userId = ConfigItem("User", "UserId", "")
    userCourse = ConfigItem("User", "UserCourse", "")
    apiKey = ConfigItem("User", "ApiKey", "")
    secretKey = ConfigItem("User", "SecretKey", "")
    updateToken = ConfigItem("User", "UpdateToken", "")
    # downloadFolder = ConfigItem(
    #     "Folders", "Download", "app/download", FolderValidator())

    # main window
    micaEnabled = ConfigItem("MainWindow", "MicaEnabled", isWin11(), BoolValidator())
    dpiScale = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    language = OptionsConfigItem(
        "MainWindow", "Language", Language.AUTO, OptionsValidator(Language), LanguageSerializer(), restart=True)

    # Material
    blurRadius  = RangeConfigItem("Material", "AcrylicBlurRadius", 15, RangeValidator(0, 40))

    # software update
    checkUpdateAtStartUp = ConfigItem("Update", "CheckUpdateAtStartUp", True, BoolValidator())

    def resource_path(self,relative_path):
        """获取资源文件的路径"""
        if getattr(sys, 'frozen', False):  # 检测是否为打包环境
            # PyInstaller 会将资源文件放置在 .app/Contents/Resources 目录（如果是Mac应用）
            base_path = sys._MEIPASS
        else:  # 未打包环境
            base_path = os.path.abspath("./source")
        print(os.path.join(base_path, relative_path))
        return os.path.join(base_path, relative_path)



YEAR = 2024
AUTHOR = "ZivYE"
VERSION = "V 1.1.1"
HELP_URL = "https://github.com/yezery/GZXH_AUTOSYBG"
# REPO_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets"
FEEDBACK_URL = "https://github.com/yezery/GZXH_AUTOSYBG/issues"
RELEASE_URL = "https://github.com/yezery/GZXH_AUTOSYBG/releases/latest"


cfg = Config()
cfg.themeMode.value = Theme.AUTO

qconfig.load(f'{cfg.resource_path("config/config.json")}', cfg)