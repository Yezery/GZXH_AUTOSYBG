from itertools import groupby
import platform
from PyQt5.QtCore import QThread, pyqtSignal
from yt_dlp import YoutubeDL
from common.config import cfg

class VideoDownloader(QThread):
    progress = pyqtSignal(bool)  # 用于通知下载状态

    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_url = None
        self.format_id = None
        self.addAudio = False
    def get_video_formats(self, video_url, cookie_file=None):
        options = {
            "cookiefile": cookie_file,  # 使用 cookies 文件（如果有）
            "listformats": True,  # 启用列出格式功能
            "quiet": True,  # 静默模式
            "skip_download": True,  # 跳过下载
        }
        try:
            with YoutubeDL(options) as ydl:
                info = ydl.extract_info(video_url, download=False)
            return info.get("formats", [])
        except Exception as e:
            print(f"获取格式信息失败: {e}")
            return []

    def get_best_format(self, formats):
        # 筛选出包含音频的格式，并确保有有效的文件大小信息
        audio_formats = [f for f in formats if f['audio_ext'] != 'none' and ('filesize' in f or 'filesize_approx' in f)]
        
        # 获取最大音频格式
        largest_audio_format = max(audio_formats, key=lambda f: self.get_file_size(f), default=None)
        
        # 分组并筛选有效的视频格式
        grouped_data = groupby(sorted(formats, key=lambda x: x['resolution']), key=lambda x: x['resolution'])
        
        if largest_audio_format:
            a_size = self.get_file_size(largest_audio_format)
        else:
            a_size = 0  # 如果没有音频格式，a_size 设为 0

        result = []
        
        for key, group in grouped_data:
            # 筛选出有效的视频格式
            group_list = [f for f in group if f['video_ext'] != 'none' and ('filesize' in f or 'filesize_approx' in f)]
            
            if not group_list:
                continue  # 如果没有有效的视频格式，跳过该组
            
            # 计算最大和最小文件大小格式
            max_filesize = max(group_list, key=lambda x: self.get_file_size(x))
            min_filesize = min(group_list, key=lambda x: self.get_file_size(x))

            # 组合最大和最小文件大小格式的描述
            if largest_audio_format:
                vi_size_max = self.get_file_size(max_filesize)
                vi_size_min = self.get_file_size(min_filesize)
                result.append([
                    [max_filesize['format_id'], self.convert_size(vi_size_max + a_size), max_filesize['format'], f"{max_filesize['video_ext']}+{largest_audio_format['audio_ext']}", "效果最好", vi_size_max + a_size],
                    [min_filesize['format_id'], self.convert_size(vi_size_min + a_size), min_filesize['format'], f"{min_filesize['video_ext']}+{largest_audio_format['audio_ext']}", "体积最小", vi_size_min + a_size]
                ])

        # 扁平化二维数组
        flattened_result = [item for sublist in result for item in sublist]

        # 先按效果类型排序（效果最好排前，体积最小排后），再按文件大小递减排序
        flattened_result.sort(key=lambda x: (x[4] != "效果最好", -x[5]))

        return flattened_result


    def get_format(self, formats):
        # 过滤并返回所需字段的值
        return [
            [
                f['format_id'],
                self.convert_size(self.get_file_size(f)),
                f['video_ext'] if f['video_ext'] != 'none' else f"音频 {f['audio_ext']}",
                f['format'],
            ]
            for f in formats
        ][::-1]

    def get_file_size(self, f):
        """获取有效的文件大小，优先使用 filesize_approx"""
        return f.get('filesize_approx', f.get('filesize', 0))


    def convert_size(self, size):
        if size is None:  # 添加检查 None 的条件
            return "未知大小"
        
        units = ["B", "KB", "MB", "GB", "TB"]
        unit_index = 0
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024.0
            unit_index += 1
        return f"{size:.2f} {units[unit_index]}"


    def get_download_video_list(self,video_url):
        cookie_file = cfg.resource_path("config/cookies.txt")
        formats = self.get_video_formats(video_url, cookie_file)
        return self.get_best_format(formats),self.get_format(formats)

    def download_video(self, video_url, format_id, addAudio=False):
        self.video_url = video_url
        self.format_id = format_id
        self.addAudio = addAudio
        self.start()  # 开始线程任务
    
    def run(self):
        cookie_file = cfg.resource_path("config/cookies.txt")
        system = platform.system().lower()

        # 配置下载选项
        if self.addAudio:
            combined_format = f"{self.format_id}+bestaudio"
            options = {
                "cookiefile": cookie_file,
                "format": combined_format,
                "outtmpl": f"{cfg.get(cfg.downloadFolder)}/%(title)s.%(ext)s",
                "merge_output_format": "mp4",
                "ffmpeg_location": cfg.resource_path("bin/ffmpeg.exe") if system == "windows" else cfg.resource_path("bin/ffmpeg"),
                "quiet": True,
            }
        else:
            options = {
                "cookiefile": cookie_file,
                "format": self.format_id,
                "outtmpl": f"{cfg.get(cfg.downloadFolder)}/%(title)s.%(ext)s",
                "quiet": True,
            }

        # 下载视频
        try:
            with YoutubeDL(options) as ydl:
                ydl.download([self.video_url])   
            self.progress.emit(True)  # 通知主线程
            
        except Exception as e:
            self.progress.emit(False)  # 通知主线程


# 单例模式
bilibiliDownloader = None

def get_downloader():
    global bilibiliDownloader
    if bilibiliDownloader is None:
        bilibiliDownloader = VideoDownloader()
    return bilibiliDownloader