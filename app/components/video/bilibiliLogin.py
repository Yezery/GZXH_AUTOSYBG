from PyQt6.QtWidgets import QHBoxLayout,QWidget
from PyQt6.QtGui import QPixmap, QImage,QColor
from PyQt6.QtCore import QTimer, Qt, QPoint
import requests
from http.cookiejar import MozillaCookieJar
from qrcode import QRCode
from io import BytesIO
from os import path
from qfluentwidgets import ImageLabel, PushButton, MessageBox, BodyLabel,MessageBoxBase,RoundMenu,TransparentPushButton,AvatarWidget,CaptionLabel,isDarkTheme
from common.config import cfg
import re
class BilibiliQCodeMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None,slot=None):
        super().__init__(parent)
        slot.scan_code()
        self.slot = slot
        # add widget to view layout
        self.bgImageL = ImageLabel(cfg.resource_path('images/bilibiliL.png'))
        self.bgImageR = ImageLabel(cfg.resource_path('images/bilibiliR.png'))
        self.bgImageL.scaledToHeight(250)
        self.bgImageR.scaledToHeight(250)
        # self.viewLayout.addWidget(self.bgImage)
        self.widgetCode = QWidget(self)
        self.widgetLayout = QHBoxLayout(self.widgetCode)
        self.widgetLayout.addWidget(self.bgImageL,1)
        self.widgetLayout.addWidget(slot.label_image,1)
        self.widgetLayout.addWidget(self.bgImageR,1)

        self.viewLayout.addWidget(self.widgetCode)
        # self.viewLayout.addWidget(self.urlLineEdit)

        # change the text of button
        self.yesButton.hide()
        self.refreshButton = PushButton(self.tr('刷新'))
        self.cancelButton.setText(self.tr('取消'))
        self.buttonLayout.addWidget(self.refreshButton, 1)
        self.widget.setMinimumWidth(360)
        
        # self.yesButton.setDisabled(True)
        self.refreshButton.clicked.connect(slot.scan_code)
        self.cancelButton.clicked.connect(self.closeAndStptimerer)
        
    def closeAndStptimerer(self):
        self.close()
        self.slot.timer.stop()
        self.slot.timer.disconnect()

class ProfileCard(QWidget):
    """ Profile card """

    def __init__(self, user_name: str, vip_type: str, parent=None):
        super().__init__(parent=parent)
        self.nameLabel = BodyLabel(user_name, self)
        self.vipLabel = CaptionLabel(vip_type, self)
        self.logoutButton = TransparentPushButton(
            '退出登录', self)

        color = QColor(206, 206, 206) if isDarkTheme() else QColor(96, 96, 96)
        self.vipLabel.setStyleSheet('QLabel{color: '+color.name()+'}')

        color = QColor(255, 255, 255) if isDarkTheme() else QColor(0, 0, 0)
        self.nameLabel.setStyleSheet('QLabel{color: '+color.name()+'}')
        # setFont(self.logoutButton, 13)

        self.setFixedSize(220, 92)
        self.nameLabel.move(16, 13)
        self.vipLabel.move(16, 32)
        self.logoutButton.move(8, 58)
        

class BilibiliLogin(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("LoginWidget")
        self.user_name = ""
        self.vip_type = ""
        self.init_ui()
        self.init_session()
        self.avatar_btn.clicked.connect(lambda: self.info_Menu(
            self.mapToGlobal(QPoint(-130, 60))))
    
    def info_Menu(self, pos):
        menu = RoundMenu(parent=self)

        # add custom widget
        self.card = ProfileCard( self.user_name, self.vip_type, menu)
        menu.addWidget(self.card, selectable=False)

        menu.exec(pos)
        self.card.logoutButton.clicked.connect(self.cancel_login)

    def init_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bqcmb = None
        # QR code image label
        self.label_image = ImageLabel(self)

        # avatar button
        self.avatar_btn = AvatarWidget()
        self.avatar_btn.setRadius(20)
        self.avatar_btn.setVisible(True)
        self.layout.addWidget(self.avatar_btn)

        # Login button
        self.btn_login = PushButton('登录 Bilibili 解锁更多清晰度', self)
        self.btn_login.clicked.connect(self.showBilibiliQCodeDialog)
        self.layout.addWidget(self.btn_login)
        
        # Timer for QR code polling
        self.timer = QTimer(self)
        self.timer.setInterval(1000) 
        self.elapsed_time = 0

    def init_session(self):
        self.temp_cookie = cfg.resource_path("config/cookies.txt")
        if not path.exists(self.temp_cookie):
            with open(self.temp_cookie, 'w', encoding='utf-8') as f:
                f.write("# Netscape HTTP Cookie File\n")
        self.session = requests.session()
        self.session.cookies = MozillaCookieJar(filename=self.temp_cookie)
        self.login_status = False
        self.headers = {
            'authority': 'api.vc.bilibili.com',
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://message.bilibili.com',
            'referer': 'https://message.bilibili.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
        try:
            self.session.cookies.load(ignore_discard=True)
        except Exception as e:
            print(f"Error loading cookies: {e}")
        self.is_login()

    def is_login(self):
        try:
            response = self.session.get("https://api.bilibili.com/x/web-interface/nav", verify=False, headers=self.headers,timeout=3000).json()
            if response['code'] == 0:
                self.vip_type = '普通会员'
                if response['data']['vipType'] != 0 :
                    self.vip_type = '大会员'
                self.update_ui(show_logout=True, show_login=False)
                self.show_user_avatar(response['data']['face'])
                self.user_name=response['data']['uname']
                self.login_status = True
                self.bqcmb.cancelButton.click()
                return True
            else:
                self.update_ui(show_logout=False, show_login=True)
                self.login_status = False
                return False
        except Exception as e:
            print(f"Error during login check: {e}")
        return False

    def scan_code(self):
        if self.login_status:
            return
        # 如果计时器正在运行，先停止并清理旧信号
        if self.timer.isActive():
            self.timer.stop()
            try:
                self.timer.timeout.disconnect()  # 解除绑定的旧信号，确保不会重复绑定
            except TypeError:
                pass  # 如果没有绑定，直接忽略错误

        # 重置累计时间
        self.elapsed_time = 0

        # 更新 UI 显示
        self.update_ui(show_logout=False, show_login=True)

        try:
            response = self.session.get('https://passport.bilibili.com/x/passport-login/web/qrcode/generate?source=main-fe-header', headers=self.headers).json()
            qrcode_key = response['data']['qrcode_key']
            qr = QRCode()
            qr.add_data(response['data']['url'])
            img = qr.make_image()

            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qimage = QImage.fromData(buffer.getvalue())
            pixmap = QPixmap.fromImage(qimage.scaled(230, 230, Qt.AspectRatioMode.KeepAspectRatio))
            self.label_image.setPixmap(pixmap)
            self.label_image.setContentsMargins(40,40,40,40)

            # 绑定新的轮询信号到定时器
            cookies_url = f'https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qrcode_key}&source=main-fe-header'
            self.timer.timeout.connect(lambda: self.timer_callback(cookies_url))
            self.timer.start()
        except Exception as e:
            print(f"Error generating QR code: {e}")

    def timer_callback(self, cookies_url):
        self.elapsed_time += self.timer.interval()
        if self.elapsed_time >= 120000:
            self.update_ui(show_logout=False, show_login=True)
            self.timer.stop()
            self.timer.disconnect()
        else:
            try:
                response = self.session.get(cookies_url, headers=self.headers).json()
                if response['data']['code'] == 0:
                    self.timer.stop()
                    self.session.get(response['data']['url'], headers=self.headers)
                    self.session.cookies.save()
                    self.is_login()
            except Exception as e:
                print(f"Error checking QR code status: {e}")

    def show_user_avatar(self, face_url):
        try:
            image_bytes = requests.get(face_url).content
            pixmap = QPixmap.fromImage(QImage.fromData(image_bytes).scaled(39, 39, Qt.AspectRatioMode.KeepAspectRatio))
            self.avatar_btn.setPixmap(pixmap)
        except Exception as e:
            print(f"Error displaying avatar: {e}")

    def cancel_login(self):
        w = MessageBox("退出登录", '是否退出登录？', self.window())
        w.yesButton.setText(self.tr('是'))
        w.cancelButton.setText(self.tr('取消'))
        if w.exec():
            url = 'https://passport.bilibili.com/login/exit/v2'
            data = {'biliCSRF': self.extract_sessdata(self.temp_cookie)}
            self.session.post(url, headers=self.headers, data=data)
            with open(self.temp_cookie, 'w', encoding='utf-8') as file:
                file.write('# Netscape HTTP Cookie File\n')
            self.update_ui(show_logout=False, show_login=True)
            self.login_status = False

    def update_ui(self, show_logout=False, show_login=True):
        self.avatar_btn.setVisible(show_logout)
        self.btn_login.setVisible(show_login)

    def showBilibiliQCodeDialog(self):
        self.bqcmb = BilibiliQCodeMessageBox(self.window(),self)
        if self.bqcmb.exec():
            pass
            # print(w.urlLineEdit.text())
    @staticmethod
    def extract_sessdata(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        matches = re.findall(r'SESSDATA="(.*?)"', content)
        return matches[0] if matches else ''
