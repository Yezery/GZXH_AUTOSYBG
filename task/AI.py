import requests
import json
from PyQt5.QtCore import pyqtSignal,QThread



class QFAI:
    def __init__(self, API_KEY, SECRET_KEY):
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.prompt = "请根据以下内容以第一人称'我'写有一份150字以内的实验报告心得,不要出现文尾总结和开头的总结,心得不要出现标题\n\n"

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
            from task.AI import QFAI
            ai_client = QFAI(self.api_key, self.secret_key)
            result = ai_client.QFAsk(self.doc_content)
            self.finished.emit(result)  # 发射生成成功信号
        except Exception as e:
            self.error.emit(str(e))  # 发射错误信号
