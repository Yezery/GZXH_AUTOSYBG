import io
import requests
from PyQt5.QtCore import QThread, pyqtSignal
class ConvertFile:
    def __init__(self):
        self.ip = "https://convert.zivye.asia"
    def convert_docx_to_pdf(self, docx_file_path, output_pdf_path):
        """使用 Gotenberg 服务进行文件转换"""
        url = f"{self.ip}/forms/libreoffice/convert"
        with open(docx_file_path, "rb") as docx_file:
            files = {
                'files': docx_file  # 使用字段 'files' 来传递文件
            }
            # 发送请求到 Gotenberg 服务
            response = requests.post(url, files=files, timeout=60)
            
            # 检查请求是否成功
            if response.status_code == 200:
                # 如果成功，保存返回的 PDF 文件
                with open(output_pdf_path, "wb") as output_pdf:
                    output_pdf.write(response.content)
            else:
                raise Exception(f"File conversion failed with status code {response.status_code}")
    def convert_docx_to_pdf(self, docx_file_path):
        """使用 Gotenberg 服务进行文件转换"""
        url = f"{self.ip}/forms/libreoffice/convert"
        with open(docx_file_path, "rb") as docx_file:
            files = {
                'files': docx_file  # 使用字段 'files' 来传递文件
            }
            # 发送请求到 Gotenberg 服务
            response = requests.post(url, files=files, timeout=60)
            
            # 检查请求是否成功
            if response.status_code == 200:
                return io.BytesIO(response.content)
            else:
                raise Exception(f"File conversion failed with status code {response.status_code}")


class ConvertFileWorker(QThread):
    finished = pyqtSignal(object)  # 转换完成信号，返回转换后的文件路径
    error = pyqtSignal(str)     # 转换失败信号，携带错误信息

    def __init__(self, docx_file_path, output_pdf_path="",_type=1, parent=None):
        super().__init__(parent)
        self.docx_file_path = docx_file_path
        self.output_pdf_path = output_pdf_path
        self._type = _type
    def run(self):
        """执行后台转换任务"""
        try:
            converter = ConvertFile()  # 创建 ConvertFile 实例
            match self._type:
                case 1:
                    converter.convert_docx_to_pdf(self.docx_file_path, self.output_pdf_path)  # 执行转换
                    self.finished.emit(self.output_pdf_path)  # 转换完成，发射信号
                case 2:
                    pdf_in_momery=converter.convert_docx_to_pdf(self.docx_file_path)  # 执行转换
                    self.finished.emit(pdf_in_momery)  # 转换完成，发射信号
            
        except requests.exceptions.RequestException as e:
            self.error.emit(f"Network error: {str(e)}")  # 捕获网络请求异常
        except Exception as e:
            self.error.emit(f"Error: {str(e)}")  # 捕获其他异常

    def stop(self):
        """停止线程的任务"""
        self.quit()  # 停止线程的运行
        self.wait()  # 等待线程结束

    def is_interrupted(self):
        """检查是否有中断请求"""
        return self.isInterruptionRequested()
