import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QSound

# from MainUI import Ui_MainWindow
from Game.GUI.Menu import Ui_Form

class LoginWIn(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = None
        self.initUI()



    def initUI(self):

        self.setWindowTitle('趣味工具箱')
        # 设置窗口位置居中
        self.resize(300, 200)
        self.setFixedSize(300, 200)
        self.move(QApplication.desktop().width() / 2 - self.width() / 2, 400)


        # 添加菜单帮助栏
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        act_help = QAction('帮助', self)  # 属于当前窗体
        act_help.triggered.connect(self.Help)
        menubar.addAction(act_help)

        act_other = QAction('其他', self)  # 属于当前窗体
        act_other.triggered.connect(self.other)
        menubar.addAction(act_other)

        self.statusBar().showMessage('2013747张怡桢')
        myframe = QFrame(self)

        userlb = QLabel('用户名:', myframe)
        passwordlb = QLabel('密  码:', myframe)
        passwordlb.move(0, 35)

        self.userline = QLineEdit(myframe)
        self.passwordline = QLineEdit(myframe)
        self.userline.move(55, 0)
        self.passwordline.move(55, 30)
        # 隐藏密码 设置密码模式
        self.passwordline.setEchoMode(QLineEdit.Password)
        # 登录按钮
        btnlogin = QPushButton('登录', myframe)
        btnquit = QPushButton('退出', myframe)
        btnlogin.move(0, 80)
        btnquit.move(110, 80)
        # 链接到槽实现登录
        sound = QSound('../Resources/click.wav', self)
        btnlogin.clicked.connect(self.myBtnClick)
        btnlogin.clicked.connect(sound.play)
        btnquit.clicked.connect(self.myBtnClick)
        btnquit.clicked.connect(sound.play)

        # 设置位置
        myframe.move(50, 50)
        myframe.resize(300, 300)
        # 隐藏放大缩小,只显示关闭按钮
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.show()

    def myBtnClick(self):
        # 获取源
        source = self.sender()
        account_dict = {'2013747': '123'}
        if source.text() == '登录':
            user = self.userline.text()
            password = self.passwordline.text()
            user_keys = list(account_dict.keys())
            if user not in user_keys:
                reply1 = QMessageBox.information(self, '登录出错', '用户不存在', QMessageBox.Yes | QMessageBox.No,
                                                 QMessageBox.Yes)

            elif password == account_dict[user]:
                LoginWIn.close(self)
                self.ui = Ui_Form()
                self.ui.show()
            else:
                reply2 = QMessageBox.information(self, '登录出错', '密码错误', QMessageBox.Yes | QMessageBox.No,
                                                 QMessageBox.Yes)
        elif source.text() == '退出':
            QApplication.instance().exit()

    # 定义帮助函数
    def Help(self):
        msgbox = QMessageBox(QMessageBox.Information, '帮助', '初始用户：2013747 \n 初始密码：123', QMessageBox.Ok, self)
        # 显示提示窗口
        msgbox.show()

    def other(self):
        msgbox = QMessageBox(QMessageBox.Information, '其他', '制作者姓名：张怡桢 \n 制作者学号：2013747', QMessageBox.Ok, self)
        # 显示提示窗口
        msgbox.show()

#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     desk = QApplication.desktop()
#     menu = LoginWIn()
#     sys.exit(app.exec_())
