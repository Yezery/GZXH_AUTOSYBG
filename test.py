from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QSlider, QLabel
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, Qt, QTimer

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("视频播放器")
        self.setGeometry(100, 100, 800, 600)

        # 媒体播放器组件
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # 视频显示组件
        self.videoWidget = QVideoWidget()
        self.mediaPlayer.setVideoOutput(self.videoWidget)

        # 播放/暂停按钮
        self.playButton = QPushButton("播放")
        self.playButton.clicked.connect(self.togglePlayPause)

        # 进度条
        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.setPosition)

        # 当前时间和总时间显示
        self.timeLabel = QLabel("00:00 / 00:00")
        self.updateTimer = QTimer(self)
        self.updateTimer.timeout.connect(self.updateSlider)
        self.updateTimer.start(100)

        # 打开文件按钮
        self.openButton = QPushButton("打开文件")
        self.openButton.clicked.connect(self.openFile)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)
        layout.addWidget(self.slider)
        layout.addWidget(self.timeLabel)
        layout.addWidget(self.playButton)
        layout.addWidget(self.openButton)

        # 设置中心窗口
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # 连接信号
        self.mediaPlayer.durationChanged.connect(self.updateDuration)
        self.mediaPlayer.positionChanged.connect(self.updateSlider)

    def openFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "打开视频文件", "", "视频文件 (*.mp4 *.avi *.mkv)")
        if filePath:
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filePath)))
            self.playButton.setText("播放")

    def togglePlayPause(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.playButton.setText("播放")
        else:
            self.mediaPlayer.play()
            self.playButton.setText("暂停")

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def updateSlider(self):
        position = self.mediaPlayer.position()
        duration = self.mediaPlayer.duration()
        if duration > 0:
            self.slider.setValue(int((position / duration) * 100))
            self.updateTimeLabel(position, duration)

    def updateDuration(self, duration):
        self.slider.setRange(0, 100)
        self.updateTimeLabel(self.mediaPlayer.position(), duration)

    def updateTimeLabel(self, position, duration):
        def formatTime(ms):
            seconds = ms // 1000
            minutes = seconds // 60
            seconds = seconds % 60
            return f"{minutes:02}:{seconds:02}"

        self.timeLabel.setText(f"{formatTime(position)} / {formatTime(duration)}")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
