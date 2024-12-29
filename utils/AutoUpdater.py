import os
import sys
import requests
import subprocess
from PyQt5.QtWidgets import QMessageBox

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

    def check_for_update(self):
        """检测是否有新版本"""
        try:
            url = f"https://api.github.com/repos/{self.github_user}/{self.repo_name}/releases/latest"
            response = requests.get(url)
            if response.status_code == 200:
                release_info = response.json()
                latest_version = release_info["tag_name"]  # 获取最新版本号
                download_url = release_info["assets"][0]["browser_download_url"]  # 获取下载链接

                if latest_version > self.current_version:
                    print(f"发现新版本：{latest_version}")
                    if self.ask_for_update(latest_version):
                        print("正在下载新版本...")
                        self.download_path = self.download_new_version(download_url)
                        if self.download_path:
                            print("下载完成，准备更新...")
                            self.perform_update()
                        else:
                            print("下载失败！")
                    else:
                        print("用户取消了更新。")
                else:
                    print("当前已经是最新版本。")
            else:
                print(f"无法获取更新信息，状态码：{response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"网络请求失败：{e}")
        except Exception as e:
            print(f"检测更新时出错：{e}")

    def ask_for_update(self, latest_version):
        """询问用户是否进行更新"""
        if self.parent is not None:
            reply = QMessageBox.question(
                self.parent,
                "发现新版本",
                f"有新版本 {latest_version} 可用，是否更新？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            return reply == QMessageBox.Yes
        else:
            # 如果没有父窗口，则默认返回 True
            return True

    def download_new_version(self, url):
        """下载新版本文件"""
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                # 下载到临时路径
                temp_dir = os.path.join(os.path.dirname(sys.executable), "temp_update")
                os.makedirs(temp_dir, exist_ok=True)
                download_path = os.path.join(temp_dir, "new_version.exe")
                with open(download_path, "wb") as f:
                    total_size = int(response.headers.get('content-length', 0))
                    downloaded = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            # 显示下载进度
                            progress = int(downloaded / total_size * 100) if total_size > 0 else 0
                            print(f"下载进度: {progress}%")
                return download_path
            else:
                print("下载失败，服务器返回错误。")
                return None
        except requests.exceptions.RequestException as e:
            print(f"下载过程中发生错误：{e}")
            return None
        except Exception as e:
            print(f"下载新版本时出错：{e}")
            return None

    def perform_update(self):
        """执行自动更新"""
        try:
            current_executable = sys.executable
            print(f"当前程序路径：{current_executable}")

            # 构建更新脚本
            update_script = f"""
import os
import time
import shutil
import subprocess

time.sleep(2)

try:
    shutil.move(r"{self.download_path}", r"{current_executable}")
    print("替换完成。")
except Exception as e:
    print(f"替换失败：{e}")
    sys.exit(1)

subprocess.Popen([r"{current_executable}"])
"""
            # 写入脚本
            script_path = os.path.join(os.path.dirname(sys.executable), "update_script.py")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(update_script)

            # 启动更新脚本
            subprocess.Popen([sys.executable, script_path])
            sys.exit(0)
        except Exception as e:
            print(f"执行更新时出错：{e}")
        finally:
            # 清理临时文件
            if self.download_path and os.path.exists(self.download_path):
                try:
                    os.remove(self.download_path)
                except Exception as e:
                    print(f"清理临时文件时出错：{e}")
