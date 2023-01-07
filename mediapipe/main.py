import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from Game.GUI.Login import LoginWIn

if __name__ == "__main__":
    app = QApplication(sys.argv)
    desk = QApplication.desktop()
    menu = LoginWIn()
    sys.exit(app.exec_())