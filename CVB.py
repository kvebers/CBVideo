import sys
import cv2
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

class VideoEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Editor (OpenCV)")
        self.setGeometry(100, 100, 1920, 1080)
        self.cap = None
        self.video_label = QLabel("No video loaded.")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.load_button = QPushButton("Load Video")
        self.next_button = QPushButton("Next")
        self.previous_button = QPushButton("Previous")
        self.load_button.clicked.connect(self.load_video)
        self.next_button.clicked.connect(lambda: self.add_decrease_frames(5))
        self.previous_button.clicked.connect(lambda: self.add_decrease_frames(-5))
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.next_button)
        self.layout.addWidget(self.previous_button)
        self.layout.addWidget(self.video_label)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def load_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "For now only .mp4 files are supported"
        )
        if file_path:
            self.cap = cv2.VideoCapture(file_path)
            if not self.cap.isOpened():
                self.video_label.setText("Failed to load video.")
                return
            self.video_label.setText("")

    def add_decrease_frames(self, frame_count):
        if self.cap and self.cap.isOpened():
            current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            new_frame = max(0, current_frame + frame_count)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
            ret, frame = self.cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                self.video_label.setPixmap(pixmap.scaled(
                    self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.cap.release()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoEditorWindow()
    window.show()
    sys.exit(app.exec_())