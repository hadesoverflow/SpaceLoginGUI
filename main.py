# main.py
import sys
from PyQt5.QtWidgets import QApplication

from login_gui import LoginWindow
from register_gui import RegisterWindow
from forgot_gui import ForgotPasswordWindow
from dashboard_gui import DashboardWindow

app = QApplication(sys.argv)

# Khởi tạo các cửa sổ và logic chuyển đổi
def to_register():
    login.hide()
    register.show()

def to_login():
    register.hide()
    forgot.hide()
    dashboard.hide()
    login.show()

def to_dashboard(username):
    login.hide()
    dashboard.set_username(username)
    dashboard.show()

def to_forgot():
    login.hide()
    forgot.show()

# Tạo instance các cửa sổ
login = LoginWindow(
    switch_to_register=to_register,
    switch_to_dashboard=to_dashboard,
    switch_to_forgot=to_forgot
)
register = RegisterWindow(switch_to_login=to_login)
forgot = ForgotPasswordWindow(switch_to_login=to_login)
dashboard = DashboardWindow()

login.show()
sys.exit(app.exec_())
