import os
import platform
import sys
import webbrowser
import requests
import subprocess
from packaging.version import Version
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from qfluentwidgets import MessageBox, ProgressRing, MessageBoxBase
from components.Message import createMessage
from common.config import cfg
class CustomMessageBox(MessageBoxBase):
    """ Custom message box """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.buttonGroup.deleteLater()
        self.ring = ProgressRing(self)
        # 设置进度环取值范围和当前值
        self.ring.setRange(0, 100)
        # 显示进度环内文本
        self.ring.setTextVisible(True)
        # 调整进度环大小
        self.ring.setFixedSize(150, 150)
        # 调整厚度
        self.ring.setStrokeWidth(15)
        # 将组件添加到布局中
        self.viewLayout.deleteLater()
        self.vBoxLayout.setContentsMargins(40, 40, 40, 40)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.ring)

class DownloadThread(QThread):
    """后台线程下载文件"""
    update_progress = pyqtSignal(int)  # 用于更新进度条的信号
    download_complete = pyqtSignal(str)  # 用于通知下载完成的信号

    def __init__(self, url, download_path, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.url = url
        self.download_path = download_path

    def run(self):
        """在后台线程中执行下载"""
        try:
            response = requests.get(self.url, stream=True)
            if response.status_code == 200:
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0

                with open(self.download_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            # 更新进度条
                            progress = int(downloaded / total_size * 100) if total_size > 0 else 0
                            self.update_progress.emit(progress)
                self.download_complete.emit(self.download_path)
            else:
                createMessage(self.parent, "下载失败", "服务器返回错误", 0)
        except requests.exceptions.RequestException as e:
            createMessage(self.parent, "下载失败", f"下载过程中发生错误：{e}", 0)
        except Exception as e:
            createMessage(self.parent, "下载失败", f"下载新版本时出错：{e}", 0)
            self.download_complete.emit("error")

class UpdateCheckThread(QThread):
    """检测更新的线程"""
    update_check_complete = pyqtSignal(bool, str, str)  # 成功标志、提示信息、下载链接

    def __init__(self, github_user, repo_name, current_version, headers, parent=None):
        super().__init__(parent)
        self.github_user = github_user
        self.repo_name = repo_name
        self.current_version = current_version
        self.headers = headers

    def compare_versions(self, version1, version2):
        """比较版本号"""
        v1 = Version(version1.lstrip("v"))  # 去掉 'v' 前缀
        v2 = Version(version2.lstrip("v"))
        return v1 < v2
    
    def run(self):
        """执行更新检测"""
        try:
            url = f"https://api.github.com/repos/{self.github_user}/{self.repo_name}/releases/latest"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                release_info = response.json()
                latest_version = release_info["tag_name"]  # 获取最新版本号

                # 获取当前操作系统和架构
                system = platform.system().lower()

                # 筛选适合当前系统的安装包
                download_url = None
                for asset in release_info["assets"]:
                    if system in asset["name"].lower():
                        download_url = asset["browser_download_url"]
                        break

                if not download_url:
                    return

                # 版本比较
                if self.compare_versions(self.current_version, latest_version):
                    self.update_check_complete.emit(True, latest_version, download_url)
                else:
                    return
            else:
                print(response.json())
                self.update_check_complete.emit(False, f"无法获取更新信息，状态码：{response.status_code}", "")
        except Exception as e:
            self.update_check_complete.emit(False, f"检测更新失败", "")


class AutoUpdater:
    def __init__(self, github_user, repo_name, current_version, parent=None):
        """
        初始化更新器
        :param github_user: GitHub 用户名
        :param repo_name: 仓库名
        :param current_version: 当前版本号（如 '1.0.0'）
        :param parent: 父窗口，用于显示对话框（PyQt）
        """
        self.github_user = github_user
        self.repo_name = repo_name
        self.current_version = current_version
        self.download_path = None
        self.parent = parent
        self.headers = {
            "authorization": f"bearer {cfg.get(cfg.updateToken)}",
            "Accept": "application/json",  # 指定响应数据格式为 JSON
            "User-Agent": "Awesome-Octocat-App"
        }
        self.cmb = CustomMessageBox(self.parent)

    def check_for_update(self):
        """启动检查更新的线程"""
        self.update_check_thread = UpdateCheckThread(self.github_user, self.repo_name, self.current_version, self.headers, self.parent)
        self.update_check_thread.update_check_complete.connect(self.handle_update_check_result)
        self.update_check_thread.start()
        
    def handle_update_check_result(self, success, message, download_url):
        """处理更新检查的结果"""
        if success:
            self.ask_for_update(download_url)  # 传递下载链接
        else:
            createMessage(self.parent, "警告", message, 2)

    def ask_for_update(self, download_url):
        """询问用户是否进行更新"""
        w = MessageBox("发现新版本", f"有新版本是否更新？", self.parent)

        if w.exec():
            self.download_new_version(download_url)
        else:
            return

    def get_user_download_directory(self):
        """获取当前操作系统的下载文件夹路径"""
        user_home = os.path.expanduser("~")  # 获取用户主目录
        system = platform.system().lower()

        if system == "windows":
            # Windows 系统，下载文件夹通常在用户目录下的 "Downloads" 文件夹
            return os.path.join(user_home, "Downloads")
        elif system == "darwin" or system == "linux":
            # macOS 和 Linux 系统，下载文件夹通常在用户目录下的 "Downloads" 文件夹
            return os.path.join(user_home, "Downloads")
        else:
            createMessage(self.parent, "下载失败", f"不支持的操作系统: {system}", 0)
            return None
        
    def download_new_version(self, url):
        """下载新版本文件"""
        try:
            # 获取操作系统类型
            system = platform.system().lower()
            
            # 如果是 macOS
            if system == "darwin":  # macOS
                self.perform_update(url)

            elif system == "windows":  # Windows
                self.cmb.show()
                # 获取用户的下载目录
                download_dir = self.get_user_download_directory()
                if not download_dir:
                    return
                system = platform.system().lower()
                # 目标下载路径
                download_path = os.path.join(download_dir, f"GEN-{system}.exe")
                # 创建并启动后台下载线程
                self.download_thread = DownloadThread(url, download_path,self.parent)
                self.download_thread.update_progress.connect(self.update_progress)  # 连接信号
                self.download_thread.download_complete.connect(self.download_complete)  # 连接下载完成信号
                self.download_thread.start()

        except Exception as e:
            createMessage(self.parent, "下载失败", "请稍后重试", 0)

    def update_progress(self, progress):
        if self.cmb:
            """更新进度条"""
            self.cmb.ring.setValue(progress)
                

    def download_complete(self, download_path):
        """处理下载完成"""
        if download_path == "error":
            createMessage(self.parent, "下载失败", "下载失败，请稍后重试。", 0)
            return
        self.cmb.deleteLater()  # 删除进度条
        self.perform_update(download_path)

    def perform_update(self, download_path):
        """执行自动更新"""
        try:
            system = platform.system().lower()

            if system == "darwin":  # macOS
                createMessage(self.parent, "提醒", "打开浏览器以继续安装", 3)
                self.open_browser(download_path)
                return

            elif system == "windows":  # Windows
                # 执行 Windows 自动更新过程
                createMessage(self.parent, "更新中", f"准备执行安装程序：{download_path}", 1)

                # 执行安装程序
                subprocess.Popen([download_path])  # 自动执行安装程序
                sys.exit(0)

        except Exception as e:
            createMessage(self.parent, "下载失败", f"执行更新时出错：{e}", 0)

    def open_browser(self, url):
        """打开浏览器"""
        try:
            webbrowser.open(url)
        except Exception as e:
            createMessage(self.parent, "打开浏览器失败", f"无法打开浏览器：{e}", 0)