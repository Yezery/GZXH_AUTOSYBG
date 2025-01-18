import os
import platform
import re
import shutil
import sys
import requests
import subprocess
from packaging.version import Version
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from qfluentwidgets import MessageBox, ProgressRing, MessageBoxBase
from components.Message import createMessage
from common.config import VERSION
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
        self.yesButton.setText(self.tr('是'))
        self.cancelButton.setText(self.tr('取消'))
        # 将组件添加到布局中
        self.viewLayout.deleteLater()
        self.vBoxLayout.setContentsMargins(40, 40, 40, 40)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addWidget(self.ring)
        self.hide()

class UpdateCheckThread(QThread):
    """检测更新的线程"""
    update_check_complete = pyqtSignal(bool, str, str)  # 成功标志、提示信息、下载链接

    def __init__(self, parent=None):
        super().__init__(parent)
    def run(self):
        """执行更新检测"""
        try:
            url = f"https://gen.zivye.asia//service/rest/v1/components?repository=GEN"
            response = requests.get(url)
            if response.status_code == 200:
                release_info = response.json()
                items = release_info['items']
                release_version = items[-1]['group']

                if Version(release_version.lstrip("/V")) > Version(VERSION.lstrip("V")):
                    system = platform.system().lower()
                    for item in items:
                        if release_version in item.values() and re.search(rf"{system}", item['name']):
                            self.update_check_complete.emit(True,release_version.lstrip("/"), item['assets'][0]['downloadUrl'])
                            break
            else:
                self.update_check_complete.emit(False, f"无法获取更新信息，状态码：{response.status_code}", "")
        except Exception as e:
            print(e)
            self.update_check_complete.emit(False, f"检测更新失败", "")

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

class MountAndInstallThread(QThread):
    """后台线程处理 DMG 挂载和安装"""
    update_progress = pyqtSignal(int)  # 用于更新进度条的信号
    install_complete = pyqtSignal(bool)  # 安装完成的信号

    def __init__(self, dmg_path, target_path, parent=None):
        super().__init__(parent)
        self.dmg_path = dmg_path
        self.target_path = target_path

    def run(self):
        """在后台线程中执行 DMG 挂载和安装"""
        try:
            # 挂载 DMG 文件并解析输出以获取挂载点
            mount_output = subprocess.check_output(["hdiutil", "attach", self.dmg_path]).decode("utf-8")
            self.update_progress.emit(20)  # 进度更新，模拟值

            # 查找挂载点，通常位于输出的最后一列
            mount_point = None
            for line in mount_output.splitlines():
                if "/Volumes/" in line:
                    mount_point = line.split("\t")[-1]
                    break

            if not mount_point:
                self.install_complete.emit(False)
                return

            # 列出挂载点的内容，查看实际的文件和目录
            app_path = None
            for item in os.listdir(mount_point):
                if item.endswith(".app"):
                    app_path = os.path.join(mount_point, item)
                    break

            if not app_path:
                self.install_complete.emit(False)
                return

            # 如果目标路径下已经存在 GEN.app，先删除
            if os.path.exists(self.target_path):
                shutil.rmtree(self.target_path)  # 删除目标路径
                self.update_progress.emit(50)  # 进度更新，模拟值

            # 复制新的应用到 /Applications
            shutil.copytree(app_path, self.target_path)
            self.update_progress.emit(80)  # 进度更新，模拟值

            # 卸载挂载点
            subprocess.run(["hdiutil", "detach", mount_point], check=True)
            self.update_progress.emit(100)  # 进度更新，模拟值

            self.install_complete.emit(True)  # 通知安装完成

        except subprocess.CalledProcessError as e:
            self.install_complete.emit(False)
            print(f"DMG 安装过程中出错：{e}")
        except Exception as e:
            self.install_complete.emit(False)
            print(f"其他错误：{e}")
class AutoUpdater:
    """自动更新管理器"""

    def __init__(self,parent=None):
        self.parent = parent
        self.download_thread = None
        self.cmb = CustomMessageBox(self.parent)

    def check_for_updates(self):
        """启动更新检测线程"""
        self.update_check_thread = UpdateCheckThread(
           self.parent
        )
        self.update_check_thread.start()
        self.update_check_thread.update_check_complete.connect(self.ask_for_update)
 
    def ask_for_update(self, success, latest_version, download_url):
        """询问用户是否进行更新"""
        if success:
            w = MessageBox(f"发现新版本 {latest_version}", f"有新版本是否更新？", self.parent)
            if w.exec():
                self.start_download(download_url)
            else:
                return
            
    def start_download(self, download_url):
        """启动下载线程"""
        try:
            self.cmb.show()
            system = platform.system().lower()
            if system == "darwin":
                download_path = os.path.join("/tmp", "GEN-darwin.dmg")
            elif system == "windows":
                download_path = os.path.join(self.get_user_download_directory(), "GEN-windows.exe")
            else:
                createMessage(self.parent, "更新失败", "当前系统不支持自动更新", 0)
                return

            self.download_thread = DownloadThread(download_url, download_path, self.parent)
            self.download_thread.update_progress.connect(self.update_progress)  # 连接信号
            self.download_thread.download_complete.connect(self.on_download_complete)
            self.download_thread.start()
        except Exception as e:
            createMessage(self.parent, "启动失败", f"更新启动失败：{e}", 0)

    def update_progress(self, progress):
        if self.cmb:
            """更新进度条"""
            self.cmb.ring.setValue(progress)

    def on_download_complete(self, download_path):
        """处理下载完成事件"""
        if download_path == "error":
            createMessage(self.parent, "下载失败", "下载失败，请稍后重试", 0)
        else:
            system = platform.system().lower()
            if system == "darwin":
                self.install_on_mac(download_path)
            elif system == "windows":
                self.install_on_windows(download_path)

    def install_on_mac(self, dmg_path):
            """挂载 DMG 并自动更新"""
            # 这里使用后台线程处理挂载和安装
            target_path = "/Applications/GEN.app"
            self.mount_and_install_thread = MountAndInstallThread(dmg_path, target_path, self.parent)
            self.mount_and_install_thread.update_progress.connect(self.update_progress)
            self.mount_and_install_thread.install_complete.connect(self.install_complete_mac)
            self.mount_and_install_thread.start()
            
    def install_on_windows(self, exe_path):
        """Windows 自动安装"""
        createMessage(self.parent, "更新中", f"准备执行安装程序：{exe_path}", 1)
        try:
            subprocess.Popen([exe_path])  # 自动执行安装程序
            createMessage(self.parent, "更新成功", "安装程序已启动", 3)
            sys.exit(0)
        except Exception as e:
            createMessage(self.parent, "更新失败", f"启动安装程序失败：{e}", 0)

    def get_user_download_directory(self):
        """获取用户下载目录"""
        return os.path.expanduser("~/Downloads")
    
    def install_complete_mac(self, success):
        """安装完成后的处理（macOS）"""
        if success:
            self.close_existing_app("GEN")
            createMessage(self.parent, "更新成功", "应用程序已成功更新！请重启应用", 3)
        else:
            createMessage(self.parent, "更新失败", "更新过程中出现问题，请稍后重试。", 0)
        self.cmb.hide()  # 删除进度条

    def close_existing_app(self, app_name):
        """关闭正在运行的应用"""
        try:
            # 使用 ps 命令查找进程，并获取进程 PID
            ps_output = subprocess.check_output(["ps", "aux"])
            # 搜索包含应用名的进程行
            process_lines = [line for line in ps_output.decode().splitlines() if app_name in line]
            
            if process_lines:
                # 提取 PID
                for line in process_lines:
                    pid = line.split()[1]  # 获取进程的 PID
                    subprocess.run(["kill", "-9", pid], check=True)  # 强制终止进程
                print(f"已强制关闭 {app_name} 应用")
            else:
                print(f"{app_name} 没有在运行")

        except subprocess.CalledProcessError as e:
            print(f"关闭应用失败: {e}")
        except Exception as e:
            print(f"其他错误: {e}")