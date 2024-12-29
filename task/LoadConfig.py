import json
import os
import sys


class LoadConfig:
    def __init__(self):
        # 默认配置
        self.default_config = {
            "NAME": "默认姓名",
            "ID": "默认学号",
            "COURSE": "默认班级",
            "API_KEY": "默认API_KEY",
            "SECRET_KEY": "默认SECRET_KEY",
            "SAVE_PATH": os.path.join(os.path.expanduser("~"), "Desktop"),
        }
        self.config_path = self.get_config_path()
        self.config = self.load_config()

    def get_app_path(self):
        """
        获取应用程序运行目录：
        - 在未打包时，返回当前脚本所在目录
        - 在打包时，根据平台获取资源路径
        """
        if getattr(sys, "frozen", False):  # 检测是否为打包环境
            if sys.platform == "darwin":  # macOS 的 .app 文件
                return os.path.join(os.path.dirname(sys.executable), "../Resources")
            else:  # Windows/Linux 的打包目录
                return os.path.dirname(sys.executable)
        else:
            # 未打包时，返回脚本所在目录
            return os.path.abspath(os.path.dirname(__file__))

    def get_config_path(self):
        """获取配置文件路径"""
        config_dir = os.path.join(self.get_app_path(), "config")
        os.makedirs(config_dir, exist_ok=True)  # 确保配置文件夹存在
        return os.path.join(config_dir, "config.json")

    def load_config(self):
        """加载或初始化配置信息"""
        try:
            # 如果配置文件存在，加载文件
            if os.path.exists(self.config_path):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                # 文件不存在，写入默认配置
                self.save_config(self.default_config)
                return self.default_config
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return self.default_config

    def save_config(self, config_data):
        """保存配置信息"""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(config_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存配置文件失败: {e}")

    # def resource_path(self, relative_path):
    #     """获取资源文件路径"""
    #     if getattr(sys, "frozen", False):  # 打包环境
    #         base_path = sys._MEIPASS
    #     else:  # 未打包环境
    #         base_path = os.path.abspath(".")
    #     return os.path.join(base_path, relative_path)
    def resource_path(self,relative_path):
        """获取资源文件的路径"""
        if getattr(sys, 'frozen', False):  # 检测是否为打包环境
            # PyInstaller 会将资源文件放置在 .app/Contents/Resources 目录（如果是Mac应用）
            base_path = sys._MEIPASS
        else:  # 未打包环境
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


    def refresh_config(self):
        """重新加载配置"""
        self.config = self.load_config()


# 创建全局配置实例
Config = LoadConfig()


def get_config():
    """获取全局配置实例"""
    Config.refresh_config()
    print("当前应用路径:", Config.get_app_path())
    return Config
