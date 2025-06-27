# login_gui.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QCheckBox, QMessageBox, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QPixmap, QFontDatabase, QFont, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import json, os

class LoginWindow(QWidget):
    def __init__(self, switch_to_register, switch_to_dashboard, switch_to_forgot):
        super().__init__()
        self.switch_to_register = switch_to_register
        self.switch_to_dashboard = switch_to_dashboard
        self.switch_to_forgot = switch_to_forgot
        self.initUI()

    def initUI(self):
        self.setFixedSize(800, 520)
        self.setWindowTitle("Login")

        base_path = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(base_path, "assets")
        bg_path = os.path.join(asset_path, "space_background.jpg")

        # Background image
        bg_label = QLabel(self)
        bg_label.setGeometry(0, 0, self.width(), self.height())
        bg_label.setPixmap(QPixmap(bg_path).scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        bg_label.lower()

        font_id = QFontDatabase.addApplicationFont(os.path.join(asset_path, "Orbitron-Regular.ttf"))
        orbitron = QFontDatabase.applicationFontFamilies(font_id)[0] if font_id != -1 else "Arial"

        # Login box
        self.loginBox = QWidget(self)
        self.loginBox.setGeometry(250, 110, 300, 360)
        self.loginBox.setStyleSheet("background-color: rgba(10, 10, 30, 0.9); border-radius: 20px;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(60)
        shadow.setColor(QColor(0, 255, 255, 200))
        shadow.setOffset(0, 0)
        self.loginBox.setGraphicsEffect(shadow)

        title = QLabel("SPACE LOGIN", self.loginBox)
        title.setGeometry(0, 20, 300, 40)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont(orbitron, 17, QFont.Bold))
        title.setStyleSheet("color: #00ffff;")

        self.username = QLineEdit(self.loginBox)
        self.username.setPlaceholderText("🧑‍🚀 Galactic ID")
        self.username.setGeometry(30, 80, 240, 38)
        self.username.setStyleSheet(self.input_style())

        self.password = QLineEdit(self.loginBox)
        self.password.setPlaceholderText("🔒 Access Key")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setGeometry(30, 130, 240, 38)
        self.password.setStyleSheet(self.input_style())

        self.showPass = QCheckBox("🔍 Show Access Key", self.loginBox)
        self.showPass.setGeometry(30, 175, 240, 20)
        self.showPass.setStyleSheet("color: #ccc; font-size: 11px;")
        self.showPass.stateChanged.connect(self.toggle_password_visibility)

        loginButton = QPushButton("🚪 ENTER SHIP", self.loginBox)
        loginButton.setGeometry(30, 200, 240, 44)
        loginButton.setStyleSheet(self.button_style("#00ffff", "black"))
        loginButton.clicked.connect(self.handle_login)

        registerLink = QPushButton("🆕 Register New Account", self.loginBox)
        registerLink.setGeometry(30, 255, 240, 30)
        registerLink.setStyleSheet(self.button_style("#33ccff", "white"))
        registerLink.clicked.connect(self.switch_to_register)

        forgotLink = QPushButton("❓ Forgot Password?", self.loginBox)
        forgotLink.setGeometry(30, 290, 240, 30)
        forgotLink.setStyleSheet(self.button_style("#ffaa00", "white"))
        forgotLink.clicked.connect(self.switch_to_forgot)

    def input_style(self):
        return """
        QLineEdit {
            background-color: rgba(255, 255, 255, 0.1);
            color: #ffffff;
            border: 1px solid #00ffff;
            border-radius: 8px;
            padding-left: 12px;
            font-size: 14px;
        }
        QLineEdit:focus {
            border: 2px solid #00ffff;
            background-color: rgba(0, 50, 70, 0.3);
        }
        """

    def button_style(self, bg_color="#00ffff", text_color="black"):
        return f"""
        QPushButton {{
            background-color: {bg_color};
            color: {text_color};
            font-weight: bold;
            font-size: 13px;
            border-radius: 14px;
            padding: 9px;
            border: none;
        }}
        QPushButton:hover {{
            background-color: #1fffff;
            color: #000;
        }}
        """

    def toggle_password_visibility(self):
        self.password.setEchoMode(QLineEdit.Normal if self.showPass.isChecked() else QLineEdit.Password)

    def handle_login(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "users.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                users = json.load(f)
        else:
            users = {}

        if username in users and users[username]["password"] == password:
            self.play_success_animation(username)
        else:
            QMessageBox.warning(self, "Access Denied", "Incorrect credentials.")

    def play_success_animation(self, username):
        sound_path = os.path.join(os.path.dirname(__file__), "assets", "door_open.mp3")
        if os.path.exists(sound_path):
            url = QUrl.fromLocalFile(sound_path)
            content = QMediaContent(url)
            self.player = QMediaPlayer()
            self.player.setMedia(content)
            self.player.setVolume(100)
            self.player.play()

            # Delay chuyển dashboard theo thời gian âm thanh (2.2s là ví dụ)
            QTimer.singleShot(2200, lambda: self.switch_to_dashboard(username))
        else:
            self.switch_to_dashboard(username)

        anim = QPropertyAnimation(self.loginBox, b"geometry")
        anim.setDuration(600)
        anim.setStartValue(self.loginBox.geometry())
        anim.setEndValue(QRect(self.width(), self.loginBox.y(), self.loginBox.width(), self.loginBox.height()))
        anim.setEasingCurve(QEasingCurve.InOutExpo)
        anim.start()
        self.anim = anim
