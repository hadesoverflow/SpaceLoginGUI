# dashboard_gui.py
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import os

class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🛰 Cabin Phi Hành Đoàn")
        self.setFixedSize(800, 520)
        self.initUI()

    def initUI(self):
        asset_path = os.path.join(os.path.dirname(__file__), "assets")
        bg_path = os.path.join(asset_path, "space_background.jpg")

        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, 800, 520)
        self.bg_label.setPixmap(QPixmap(bg_path).scaled(self.size(), Qt.KeepAspectRatioByExpanding))

        self.welcome_label = QLabel("👨‍🚀 Welcome Aboard!", self)
        self.welcome_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setGeometry(0, 30, 800, 50)

        self.username_label = QLabel("", self)
        self.username_label.setStyleSheet("color: #00ffff; font-size: 18px;")
        self.username_label.setAlignment(Qt.AlignCenter)
        self.username_label.setGeometry(0, 80, 800, 40)

    def set_username(self, username):
        self.username_label.setText(f"🪐 Galactic ID: {username}")
