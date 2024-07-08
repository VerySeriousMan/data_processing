# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2023.12.18
Author: ZhangYuetao
File Name: main.py
last renew 2024.07.08
"""

import shutil
import sys
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import qt_material

from data_processing import *
from utils import pre_id, creat_txt, change_settings, get_id, change_xjd
import config


class MyClass(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyClass, self).__init__(parent)

        self.setupUi(self)
        self.setWindowTitle("数据预处理软件V1.4(beta)")
        self.setWindowIcon(QtGui.QIcon("xey.ico"))

        self.dir_path = None

        self.open_dir_button.clicked.connect(self.open_dir)
        self.classify_button.clicked.connect(self.classify)
        self.change_setting_button.clicked.connect(self.change_settings)
        self.creat_txt_button.clicked.connect(self.get_txt)

        self.classify_button.setEnabled(False)
        self.change_setting_button.setEnabled(False)
        self.creat_txt_button.setEnabled(False)

        self.back_line.textChanged.connect(self.info_label.clear)
        self.front_line.textChanged.connect(self.info_label.clear)
        self.old_setting_line.textChanged.connect(self.info_label.clear)
        self.new_setting_line.textChanged.connect(self.info_label.clear)

        self.config_data = config.load_config()

        if self.config_data['visible'] != 'sunnyaiot':
            self.classify_button.hide()
            self.label.hide()
            self.front_line.hide()
            self.label_2.hide()
            self.back_line.hide()
            self.creat_txt_button.hide()

    def open_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self)
        if dir_path:
            self.dir_path = dir_path
            self.file_path_lable.setText(self.dir_path)
            self.classify_button.setEnabled(True)
            self.change_setting_button.setEnabled(True)
            self.creat_txt_button.setEnabled(True)
            if self.config_data['space_enabled'] == 'true':
                change_settings(self.dir_path, ' ', '')
            if self.config_data['xjd'] == 'true':
                change_xjd(self.dir_path)

    def classify(self):
        def is_valid_input(text):
            return text.isdigit() or not text

        if not (is_valid_input(self.front_line.text()) and is_valid_input(self.back_line.text())):
            self.info_label.setText('输入错误，请输入数字或为空')
            return

        for filename in os.listdir(self.dir_path):
            filepath = os.path.join(self.dir_path, filename)
            fileid = get_id(filename, self.front_line.text(), self.back_line.text())
            test_path = os.path.join(self.dir_path + '_test', filename)
            train_path = os.path.join(self.dir_path + '_train', filename)
            test_id = pre_id(r'settings/testID.txt')
            train_id = pre_id(r'settings/trainID.txt')

            if fileid in test_id:
                shutil.move(filepath, test_path)
            elif fileid in train_id:
                shutil.move(filepath, train_path)
        self.info_label.setText('分类完成')

    def change_settings(self):
        self.old_setting_line.text().replace(' ', '')
        self.new_setting_line.text().replace(' ', '')
        if not self.old_setting_line.text() or not self.new_setting_line.text():
            self.info_label.setText('属性不能为空')
            return
        change_settings(self.dir_path, self.old_setting_line.text(), self.new_setting_line.text())
        self.info_label.setText('修改完成')

    def get_txt(self):
        creat_txt(self.dir_path)
        filename = self.dir_path.split('/')[-1] + '.txt'
        self.info_label.setText(f'已生成{filename}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyClass()
    qt_material.apply_stylesheet(app, theme='default')
    myWin.show()
    sys.exit(app.exec_())
