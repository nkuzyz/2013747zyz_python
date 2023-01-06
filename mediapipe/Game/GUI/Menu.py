import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

#主界面
class MenuDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        #三个按钮实现三个功能
    def initUI(self):
        self.setWindowTitle("视频马赛克系统")
        self.setFixedSize(400, 300)# 宽×高

        # 设置图片显示区域
        self.label = QLabel(self)
        self.label.setFixedSize(80, 80)
        self.label.move(50, 50)
        # 设置背景颜色
        self.label.setStyleSheet("QLabel{background:white;}")

        #jpg = QtGui.QPixmap('./camera.jpg').scaled(self.label.width(), self.label.height())
        #self.label.setPixmap(jpg)


        # # 设置按钮——导入视频
        # btnvideo = QPushButton(self)
        # btnvideo.setText('视频打码处理')
        # btnvideo.move(200, 80)
        # #btnvideo.clicked.connect(self.openvideo)
        #
        #
        # # 设置按钮——打开摄像头
        # btncamera = QPushButton(self)
        # btncamera.setText("打开摄像头")
        # btncamera.move(200, 180)
        # #btncamera.clicked.connect(self.opencamera)
