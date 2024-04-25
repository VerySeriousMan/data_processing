# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data_processing.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(631, 374)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.open_dir_button = QtWidgets.QPushButton(self.centralwidget)
        self.open_dir_button.setGeometry(QtCore.QRect(10, 10, 131, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_dir_button.sizePolicy().hasHeightForWidth())
        self.open_dir_button.setSizePolicy(sizePolicy)
        self.open_dir_button.setObjectName("open_dir_button")
        self.classify_button = QtWidgets.QPushButton(self.centralwidget)
        self.classify_button.setGeometry(QtCore.QRect(10, 60, 131, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.classify_button.sizePolicy().hasHeightForWidth())
        self.classify_button.setSizePolicy(sizePolicy)
        self.classify_button.setObjectName("classify_button")
        self.file_path_lable = QtWidgets.QLabel(self.centralwidget)
        self.file_path_lable.setGeometry(QtCore.QRect(150, 10, 1001, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_path_lable.sizePolicy().hasHeightForWidth())
        self.file_path_lable.setSizePolicy(sizePolicy)
        self.file_path_lable.setText("")
        self.file_path_lable.setObjectName("file_path_lable")
        self.classify_lable = QtWidgets.QLabel(self.centralwidget)
        self.classify_lable.setGeometry(QtCore.QRect(150, 60, 131, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.classify_lable.sizePolicy().hasHeightForWidth())
        self.classify_lable.setSizePolicy(sizePolicy)
        self.classify_lable.setText("")
        self.classify_lable.setObjectName("classify_lable")
        self.front_line = QtWidgets.QLineEdit(self.centralwidget)
        self.front_line.setGeometry(QtCore.QRect(340, 60, 61, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.front_line.sizePolicy().hasHeightForWidth())
        self.front_line.setSizePolicy(sizePolicy)
        self.front_line.setObjectName("front_line")
        self.back_line = QtWidgets.QLineEdit(self.centralwidget)
        self.back_line.setGeometry(QtCore.QRect(480, 60, 61, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.back_line.sizePolicy().hasHeightForWidth())
        self.back_line.setSizePolicy(sizePolicy)
        self.back_line.setObjectName("back_line")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(290, 60, 51, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(430, 60, 51, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.change_id_button = QtWidgets.QPushButton(self.centralwidget)
        self.change_id_button.setGeometry(QtCore.QRect(10, 110, 131, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.change_id_button.sizePolicy().hasHeightForWidth())
        self.change_id_button.setSizePolicy(sizePolicy)
        self.change_id_button.setObjectName("change_id_button")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(440, 110, 51, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(260, 110, 51, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.new_id_line = QtWidgets.QLineEdit(self.centralwidget)
        self.new_id_line.setGeometry(QtCore.QRect(490, 110, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.new_id_line.sizePolicy().hasHeightForWidth())
        self.new_id_line.setSizePolicy(sizePolicy)
        self.new_id_line.setObjectName("new_id_line")
        self.old_id_line = QtWidgets.QLineEdit(self.centralwidget)
        self.old_id_line.setGeometry(QtCore.QRect(310, 110, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.old_id_line.sizePolicy().hasHeightForWidth())
        self.old_id_line.setSizePolicy(sizePolicy)
        self.old_id_line.setObjectName("old_id_line")
        self.change_lable = QtWidgets.QLabel(self.centralwidget)
        self.change_lable.setGeometry(QtCore.QRect(150, 110, 101, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.change_lable.sizePolicy().hasHeightForWidth())
        self.change_lable.setSizePolicy(sizePolicy)
        self.change_lable.setText("")
        self.change_lable.setObjectName("change_lable")
        self.change_setting_button = QtWidgets.QPushButton(self.centralwidget)
        self.change_setting_button.setGeometry(QtCore.QRect(10, 230, 131, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.change_setting_button.sizePolicy().hasHeightForWidth())
        self.change_setting_button.setSizePolicy(sizePolicy)
        self.change_setting_button.setObjectName("change_setting_button")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(440, 230, 61, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(260, 230, 61, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.old_setting_line = QtWidgets.QLineEdit(self.centralwidget)
        self.old_setting_line.setGeometry(QtCore.QRect(320, 230, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.old_setting_line.sizePolicy().hasHeightForWidth())
        self.old_setting_line.setSizePolicy(sizePolicy)
        self.old_setting_line.setObjectName("old_setting_line")
        self.new_setting_line = QtWidgets.QLineEdit(self.centralwidget)
        self.new_setting_line.setGeometry(QtCore.QRect(500, 230, 111, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.new_setting_line.sizePolicy().hasHeightForWidth())
        self.new_setting_line.setSizePolicy(sizePolicy)
        self.new_setting_line.setObjectName("new_setting_line")
        self.change_setting_lable = QtWidgets.QLabel(self.centralwidget)
        self.change_setting_lable.setGeometry(QtCore.QRect(150, 230, 101, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.change_setting_lable.sizePolicy().hasHeightForWidth())
        self.change_setting_lable.setSizePolicy(sizePolicy)
        self.change_setting_lable.setText("")
        self.change_setting_lable.setObjectName("change_setting_lable")
        self.open_small_dir_button = QtWidgets.QPushButton(self.centralwidget)
        self.open_small_dir_button.setGeometry(QtCore.QRect(10, 180, 131, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_small_dir_button.sizePolicy().hasHeightForWidth())
        self.open_small_dir_button.setSizePolicy(sizePolicy)
        self.open_small_dir_button.setObjectName("open_small_dir_button")
        self.file_small_path_lable = QtWidgets.QLabel(self.centralwidget)
        self.file_small_path_lable.setGeometry(QtCore.QRect(160, 190, 1031, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_small_path_lable.sizePolicy().hasHeightForWidth())
        self.file_small_path_lable.setSizePolicy(sizePolicy)
        self.file_small_path_lable.setText("")
        self.file_small_path_lable.setObjectName("file_small_path_lable")
        self.creat_txt_button = QtWidgets.QPushButton(self.centralwidget)
        self.creat_txt_button.setGeometry(QtCore.QRect(10, 280, 131, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.creat_txt_button.sizePolicy().hasHeightForWidth())
        self.creat_txt_button.setSizePolicy(sizePolicy)
        self.creat_txt_button.setObjectName("creat_txt_button")
        self.txt_lable = QtWidgets.QLabel(self.centralwidget)
        self.txt_lable.setGeometry(QtCore.QRect(130, 280, 121, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_lable.sizePolicy().hasHeightForWidth())
        self.txt_lable.setSizePolicy(sizePolicy)
        self.txt_lable.setText("")
        self.txt_lable.setObjectName("txt_lable")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 160, 641, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setLineWidth(1)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 631, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.change_setting_button.pressed.connect(self.change_setting_lable.clear) # type: ignore
        self.change_id_button.pressed.connect(self.change_lable.clear) # type: ignore
        self.classify_button.pressed.connect(self.classify_lable.clear) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.open_dir_button.setText(_translate("MainWindow", "选择文件夹"))
        self.classify_button.setText(_translate("MainWindow", "划分集合"))
        self.label.setText(_translate("MainWindow", "前留"))
        self.label_2.setText(_translate("MainWindow", "后留"))
        self.change_id_button.setText(_translate("MainWindow", "修改ID"))
        self.label_3.setText(_translate("MainWindow", "新ID"))
        self.label_4.setText(_translate("MainWindow", "原ID"))
        self.change_setting_button.setText(_translate("MainWindow", "修改属性"))
        self.label_5.setText(_translate("MainWindow", "新属性"))
        self.label_6.setText(_translate("MainWindow", "原属性"))
        self.open_small_dir_button.setText(_translate("MainWindow", "选择文件夹"))
        self.creat_txt_button.setText(_translate("MainWindow", "生成txt"))
