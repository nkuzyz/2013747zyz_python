# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menu.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QSound
from Game.GUI.FingerGame import Ui_FingerGame
from Game.GUI.PersonDraw import Ui_PersonDraw
from Game.GUI.PushUp import Ui_PushUp


class Ui_Form(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui_push_up = None
        self.ui_person_draw = None
        self.ui_finger_game = None
        self.sound = QSound('../Resources/click.wav', self)
        self.setupUi(self)
        self.slot_init()  # 初始化槽函数


    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.button_person_draw = QtWidgets.QPushButton(Form)
        self.button_person_draw.setGeometry(QtCore.QRect(150, 100, 100, 30))
        self.button_person_draw.setObjectName("button_person_draw")
        self.button_finger_game = QtWidgets.QPushButton(Form)
        self.button_finger_game.setGeometry(QtCore.QRect(150, 50, 100, 30))
        self.button_finger_game.setObjectName("button_finger_game")
        self.button_push_up = QtWidgets.QPushButton(Form)
        self.button_push_up.setGeometry(QtCore.QRect(150, 150, 100, 30))
        self.button_push_up.setObjectName("button_push_up")
        self.button_close = QtWidgets.QPushButton(Form)
        self.button_close.setGeometry(QtCore.QRect(160, 210, 81, 22))
        self.button_close.setObjectName("button_close")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.button_person_draw.setText(_translate("Form", "骨架检测"))
        self.button_finger_game.setText(_translate("Form", "手指乒乓"))
        self.button_push_up.setText(_translate("Form", "俯卧撑计数"))
        self.button_close.setText(_translate("Form", "退出程序"))

    def slot_init(self):
        self.button_finger_game.clicked.connect(self.start_finger_game)
        self.button_finger_game.clicked.connect(self.sound.play)
        self.button_person_draw.clicked.connect(self.start_person_draw)
        self.button_person_draw.clicked.connect(self.sound.play)
        self.button_push_up.clicked.connect(self.start_push_up)
        self.button_push_up.clicked.connect(self.sound.play)
        self.button_close.clicked.connect(self.close_menu)
        self.button_close.clicked.connect(self.sound.play)

    def start_finger_game(self):
        # Ui_Form.close(self)
        self.ui_finger_game = Ui_FingerGame()
        self.ui_finger_game.show()

    def start_person_draw(self):
        # Ui_Form.close(self)
        self.ui_person_draw = Ui_PersonDraw()
        self.ui_person_draw.show()
        
    def start_push_up(self):
        # Ui_Form.close(self)
        self.ui_push_up = Ui_PushUp()
        self.ui_push_up.show()
    
    def close_menu(self):
        Ui_Form.close(self)
        
