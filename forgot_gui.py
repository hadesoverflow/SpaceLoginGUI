# forgot_gui.py
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QFontDatabase, QFont, QColor
from PyQt5.QtCore import Qt
import os, json

class ForgotPasswordWindow(QWidget):
    def __init__(self, switch_to_login):
        super().__init__()
        self.switch_to_login = switch_to_login
        self.initUI()

    def initUI(self):
        self.setFixedSize(800, 520)
        self.setWindowTitle("🔑 Quên Mật Khẩu")

        base_path = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(base_path, "assets")
        bg_path = os.path.join(asset_path, "space_background.jpg")

        # Background
        bg_label = QLabel(self)
        bg_label.setGeometry(0, 0, self.width(), self.height())
        bg_label.setPixmap(QPixmap(bg_path).scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        bg_label.lower()

        # Load font
        font_id = QFontDatabase.addApplicationFont(os.path.join(asset_path, "Orbitron-Regular.ttf"))
        orbitron = QFontDatabase.applicationFontFamilies(font_id)[0] if font_id != -1 else "Arial"

        # Forgot Box
        box = QWidget(self)
        box.setGeometry(250, 130, 300, 260)
        box.setStyleSheet("background-color: rgba(10,10,30,0.8); border-radius: 20px;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50)
        shadow.setColor(QColor(0, 200, 255, 160))
        shadow.setOffset(0, 0)
        box.setGraphicsEffect(shadow)

        title = QLabel("RECOVER PASSWORD", box)
        title.setGeometry(0, 20, 300, 30)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont(orbitron, 13))
        title.setStyleSheet("color: #00ffff;")

        self.username = QLineEdit(box)
        self.username.setPlaceholderText("Enter Galactic ID")
        self.username.setGeometry(30, 70, 240, 35)
        self.username.setStyleSheet(self.input_style())

        self.recover_btn = QPushButton("RETRIEVE", box)
        self.recover_btn.setGeometry(30, 120, 240, 40)
        self.recover_btn.setStyleSheet(self.button_style())
        self.recover_btn.clicked.connect(self.handle_recovery)

        self.back_btn = QPushButton("← BACK TO LOGIN", box)
        self.back_btn.setGeometry(30, 180, 240, 32)
        self.back_btn.setStyleSheet(self.button_style("#ffaa00"))
        self.back_btn.clicked.connect(self.switch_to_login)

    def input_style(self):
        return """
        QLineEdit {
            background-color: rgba(255, 255, 255, 0.1);
            color: #ffffff;
            border: 1px solid #00ffff;
            border-radius: 6px;
            padding-left: 10px;
        }
        QLineEdit:focus {
            border: 2px solid #00ffff;
            background-color: rgba(0, 50, 70, 0.3);
        }
        """

    def button_style(self, color="#00ffff"):
        return f"""
        QPushButton {{
            background-color: {color};
            color: black;
            font-weight: bold;
            border-radius: 12px;
            padding: 8px;
            border: 1px solid #0ff;
        }}
        QPushButton:hover {{
            background-color: #00dada;
            border: 1px solid #fff;
        }}
        """

    def handle_recovery(self):
        username = self.username.text().strip()
        if not username:
            QMessageBox.warning(self, "Input Needed", "Please enter your Galactic ID.")
            return

        path = os.path.join(os.path.dirname(__file__), "assets", "users.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                users = json.load(f)
        else:
            users = {}

        if username in users:
            password = users[username]["password"]
            QMessageBox.information(self, "Access Key Found", f"Your Access Key is:\n\n🔐 {password}")
        else:
            QMessageBox.warning(self, "Not Found", "Username not found in database.")
