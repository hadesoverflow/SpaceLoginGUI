# register_gui.py
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QFontDatabase, QFont, QColor
from PyQt5.QtCore import Qt
import json, os

class RegisterWindow(QWidget):
    def __init__(self, switch_to_login):
        super().__init__()
        self.switch_to_login = switch_to_login
        self.initUI()

    def initUI(self):
        self.setFixedSize(800, 520)
        self.setWindowTitle("Register")

        base_path = os.path.dirname(os.path.abspath(__file__))
        asset_path = os.path.join(base_path, "assets")
        bg_path = os.path.join(asset_path, "space_background.jpg")

        # Background
        bg_label = QLabel(self)
        bg_label.setGeometry(0, 0, self.width(), self.height())
        bg_label.setPixmap(QPixmap(bg_path).scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        bg_label.lower()

        font_id = QFontDatabase.addApplicationFont(os.path.join(asset_path, "Orbitron-Regular.ttf"))
        orbitron = QFontDatabase.applicationFontFamilies(font_id)[0] if font_id != -1 else "Arial"

        # Register box
        self.box = QWidget(self)
        self.box.setGeometry(250, 110, 300, 360)
        self.box.setStyleSheet("background-color: rgba(10, 10, 30, 0.9); border-radius: 20px;")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(60)
        shadow.setColor(QColor(0, 255, 255, 200))
        shadow.setOffset(0, 0)
        self.box.setGraphicsEffect(shadow)

        title = QLabel("CREATE ACCOUNT", self.box)
        title.setGeometry(0, 20, 300, 40)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont(orbitron, 15, QFont.Bold))
        title.setStyleSheet("color: #00ffff;")

        self.username = QLineEdit(self.box)
        self.username.setPlaceholderText("🧑‍🚀 New Galactic ID")
        self.username.setGeometry(30, 80, 240, 38)
        self.username.setStyleSheet(self.input_style())

        self.password = QLineEdit(self.box)
        self.password.setPlaceholderText("🔒 Access Key")
        self.password.setGeometry(30, 130, 240, 38)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet(self.input_style())

        self.confirm = QLineEdit(self.box)
        self.confirm.setPlaceholderText("🔒 Confirm Key")
        self.confirm.setGeometry(30, 180, 240, 38)
        self.confirm.setEchoMode(QLineEdit.Password)
        self.confirm.setStyleSheet(self.input_style())

        register_btn = QPushButton("🚀 Create Account", self.box)
        register_btn.setGeometry(30, 230, 240, 44)
        register_btn.setStyleSheet(self.button_style("#33ccff", "white"))
        register_btn.clicked.connect(self.handle_register)

        back_btn = QPushButton("← Back to Login", self.box)
        back_btn.setGeometry(30, 285, 240, 30)
        back_btn.setStyleSheet(self.button_style("#ffaa00", "black"))
        back_btn.clicked.connect(self.switch_to_login)

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

    def handle_register(self):
        user = self.username.text().strip()
        pwd = self.password.text().strip()
        confirm = self.confirm.text().strip()

        if not user or not pwd or not confirm:
            QMessageBox.warning(self, "Missing Info", "All fields are required.")
            return

        if pwd != confirm:
            QMessageBox.warning(self, "Mismatch", "Access Keys do not match.")
            return

        path = os.path.join(os.path.dirname(__file__), "assets", "users.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                users = json.load(f)
        else:
            users = {}

        if user in users:
            QMessageBox.warning(self, "Exists", "This Galactic ID already exists.")
            return

        users[user] = {"password": pwd}
        with open(path, "w") as f:
            json.dump(users, f, indent=4)

        QMessageBox.information(self, "Success", "Account created! Ready to launch.")
        self.switch_to_login()
