import platform
import requests
import json
from PyQt6.QtCore import pyqtSignal,QThread
import threading
from llama_cpp import Llama
from common.config import cfg

class QFAI:
    def __init__(self, API_KEY, SECRET_KEY):
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.prompt = "请根据以下内容写有一份150字以内的实验报告心得（不要使用“首先”、“其次”、“然而”、“总的来说”、“总之”这些副词）。尽量用主动句，增加文章力量。避免使用陈词滥调，换成新颖的表达。避免生硬的总结或说教。删除小标题。\n\n"

    def QFAsk(self,content:str):
        try:
            url = (
                "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-tiny-8k?access_token="
                + self.get_access_token()
            )

            payload = json.dumps(
                {
                    "messages": [
                        {"role": "user", "content": f"{self.prompt}{content}"},
                    ],
                    "temperature": 0.95,
                    "top_p": 0.7,
                    "penalty_score": 1,
                }
            )
            headers = {"Content-Type": "application/json"}

            response = requests.request("POST", url, headers=headers, data=payload)

            return str(response.json()["result"])
        except requests.exceptions.ConnectionError:
            raise Exception("生成失败了！网络连接错误，请检查网络连接")
        except Exception as e:
            raise Exception(str(e))

    def get_access_token(self):
        """
            使用 AK，SK 生成鉴权签名（Access Token）
            :return: access_token，或是None(如果错误)
        """
        try:
            url = "https://aip.baidubce.com/oauth/2.0/token"
            params = {
                "grant_type": "client_credentials",
                "client_id": self.API_KEY,
                "client_secret":  self.SECRET_KEY,
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return str(response.json().get("access_token"))
            else:
                raise Exception("生成失败了！请在设置处检查 API_KEY 和 SECRET_KEY")
        # 网络类型错误
        except requests.exceptions.ConnectionError:
            raise Exception("生成失败了！网络连接错误，请检查网络连接")

class QFAIWorker(QThread):
    finished = pyqtSignal(str)  # 生成成功信号，携带 AI 总结结果
    error = pyqtSignal(str)     # 生成失败信号，携带错误信息

    def __init__(self, api_key, secret_key, doc_content):
        super().__init__()
        self.api_key = api_key
        self.secret_key = secret_key
        self.doc_content = doc_content
    def run(self):
        try:
            # 调用 AI 接口生成摘要
            ai_client = QFAI(self.api_key, self.secret_key)
            result = ai_client.QFAsk(self.doc_content)
            self.finished.emit(result)  # 发射生成成功信号
        except Exception as e:
            self.error.emit(str(e))  # 发射错误信号


class summaryWorker(QThread):
    update_chunk = pyqtSignal(str)
    finished = pyqtSignal()  # 生成成功信号，携带 AI 总结结果
    error = pyqtSignal(str)     # 生成失败信号，携带错误信息
    def __init__(self,doc_content):
        super().__init__()
        self.prompt = "请根据以下内容写有一份150字以内的实验报告心得（不要使用“首先”、“其次”、“然而”、“总的来说”、“总之”这些副词）。尽量用主动句，增加文章力量。避免使用陈词滥调，换成新颖的表达。避免生硬的总结或说教。删除小标题。\n\n"
        self.doc_content = doc_content
    def run(self):
        try:
            # 获取流式输出
            full_response = ""  # 用于存储完整的响应
            for chunk in GEN.get_response_stream(self.prompt,self.doc_content):
                # 如果开始输出内容，更新状态标签为“GEN正在输出”
                # if chunk.strip():  # 如果 chunk 不是空内容
                #     self.update_status_label.emit("GEN正在输出")
                # 通过信号更新 GUI
                full_response += chunk  # 将流式输出的内容拼接到完整响应中
                self.update_chunk.emit(full_response)  # 发射信号，更新聊天显示
            # 调用AI生成摘要
            self.finished.emit()  # 发射生成成功信号
        except Exception as e:
            self.error.emit(str(e))  # 发射错误信号
    def stop(self):
        """停止线程"""
        self._is_running = False
        self.quit()  # 退出线程
        self.wait()  # 等待线程结束

class rewriteWorker(QThread):
    update_chunk = pyqtSignal(str)
    finished = pyqtSignal()  # 生成成功信号，携带 AI 总结结果
    error = pyqtSignal(str)     # 生成失败信号，携带错误信息
    def __init__(self,content):
        super().__init__()
        self.prompt = "请帮我把下面的内容进行重写并润色。注意保持原句的格式。\n\n"
        self.content = content
    def run(self):
        try:
            # 获取流式输出
            full_response = ""  # 用于存储完整的响应
            for chunk in GEN.get_response_stream(self.prompt,self.content):
                # 如果开始输出内容，更新状态标签为“GEN正在输出”
                # if chunk.strip():  # 如果 chunk 不是空内容
                #     self.update_status_label.emit("GEN正在输出")
                # 通过信号更新 GUI
                full_response += chunk  # 将流式输出的内容拼接到完整响应中
                self.update_chunk.emit(full_response)  # 发射信号，更新聊天显示
            # 调用AI生成摘要
            self.finished.emit()  # 发射生成成功信号
        except Exception as e:
            self.error.emit(str(e))  # 发射错误信号
    def stop(self):
        """停止线程"""
        self._is_running = False
        self.quit()  # 退出线程
        self.wait()  # 等待线程结束

class ChatWorker(QThread):
    update_chunk = pyqtSignal(str)
    finished = pyqtSignal()  # 生成成功信号，携带 AI 总结结果
    error = pyqtSignal(str)     # 生成失败信号，携带错误信息
    def __init__(self,content,history):
        super().__init__()
        self.history = history
        self.prompt = "要求简洁地回答用户的问题，不要重复之前的问题。\n\n"
        self.content = content
    def run(self):
        try:
            for chunk in GEN.get_response_stream_think(self.prompt,self.content,self.history):
                if not chunk.strip():  # 如果 chunk 不是空内容
                    continue
                self.update_chunk.emit(chunk)  # 发射信号，更新聊天显示
            # 调用AI生成摘要
            self.finished.emit()  # 发射生成成功信号
        except Exception as e:
            print(f"生成失败: {e}")
            self.error.emit(str(e))  # 发射错误信号
    def stop(self):
        """停止线程"""
        self._is_running = False
        self.quit()  # 退出线程
        self.wait()  # 等待线程结束
        
class GENModel:
    def __init__(self):
        model_path = cfg.resource_path("deepSeek-R1-1.5B/model.gguf")
        try:
            self.n_gpu_layers = self._detect_gpu_layers()
            self.llm = Llama(
                model_path=model_path,
                n_gpu_layers=self.n_gpu_layers,  # 根据硬件条件设置
                verbose=False,
                n_ctx=2048,
            )
            self.lock = threading.Lock()  # 创建线程锁
        except Exception as e:
            print(f"加载模型失败: {e}")
    def _detect_gpu_layers(self):
        """
        检测操作系统和硬件配置，返回适合的 n_gpu_layers 值。
        - 如果有 GPU，返回 -1（使用所有可用的 GPU 层）。
        - 如果没有 GPU，返回 0（仅使用 CPU）。
        """
        system = platform.system().lower()

        if system == "darwin":  # macOS
            # macOS 通常使用 Metal 加速
            return -1  # 使用 Metal 加速（如果有）
        elif system == "windows":  # Windows
            try:
                import torch  # 使用 PyTorch 检测 GPU
                if torch.cuda.is_available():
                    return -1  # 使用所有可用的 GPU 层
                else:
                    return 0  # 回退到 CPU
            except ImportError:
                print("未安装 PyTorch，无法检测 GPU。回退到 CPU。")
                return 0  # 回退到 CPU
        else:
            print(f"不支持的操作系统: {system}。回退到 CPU。")
            return 0  # 回退到 CPU
    
    def get_response_stream(self, prompt, user_input):
        messages = [
            {"role": "user", "content": prompt + user_input},
        ]
        try:
            with self.lock:  # 加锁，确保同一时间只有一个线程访问模型
                output = self.llm.create_chat_completion(
                    messages=messages,
                    stream=True  # 开启流式输出
                )

                response = ""
                buffer = ""  # 用于缓存流式输出的内容
                in_think_block = False  # 标记是否在 <think> 块中

                for chunk in output:
                    delta = chunk['choices'][0]['delta']
                    if 'content' in delta:
                        content = delta['content']
                        buffer += content  # 将内容添加到缓存中

                        # 处理 <think> 和 </think> 标记
                        while True:
                            if not in_think_block:
                                # 查找 <think> 标记
                                think_start = buffer.find("<think>")
                                if think_start != -1:
                                    # 输出 <think> 之前的内容
                                    yield buffer[:think_start]
                                    buffer = buffer[think_start + len("<think>"):]
                                    in_think_block = True
                                else:
                                    # 没有 <think>，直接输出缓存内容
                                    yield buffer
                                    buffer = ""
                                    break
                            else:
                                # 查找 </think> 标记
                                think_end = buffer.find("</think>")
                                if think_end != -1:
                                    # 跳过 <think>...</think> 之间的内容
                                    buffer = buffer[think_end + len("</think>"):]
                                    in_think_block = False
                                else:
                                    # 等待 </think> 出现，清空缓存
                                    buffer = ""
                                    break
                        
                        response += content  # 将内容添加到完整响应中

        except Exception as e:
            print(f"\n发生错误: {e}")
            yield ""

    def get_response_stream_think(self, prompt, user_input,history:list):
        history.append({"role": "user", "content": prompt + user_input})
        try:
            with self.lock:  # 加锁，确保同一时间只有一个线程访问模型
                output = self.llm.create_chat_completion(
                    messages=history,
                    stream=True  # 开启流式输出
                )

                # response = ""
                # buffer = ""  # 用于缓存流式输出的内容
                # in_think_block = False  # 标记是否在 <think> 块中

                for chunk in output:
                    delta = chunk['choices'][0]['delta']
                    if 'content' in delta:
                        content = delta['content']
                        yield content

        except Exception as e:
            print(f"\n发生错误: {e}")
            yield ""

# 全局 GEN 实例
GEN = GENModel()