# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2023.12.18
Author: ZhangYuetao
File Name: main.py
last renew 2024.07.15
"""

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import qt_material

from data_processing import *
from utils import creat_txt, change_settings, classify_id, change_xjd, create_dir_name, get_wrong_paths_txt
import config
from pic_dedup import dedup
from rework_main import ReworkWindow


class MyClass(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyClass, self).__init__(parent)

        self.setupUi(self)
        self.setWindowTitle("数据预处理软件V1.4(beta)")
        self.setWindowIcon(QtGui.QIcon("xey.ico"))

        self.dir_path = None
        self.compare_dir_path = None
        self.rework_window = None
        self.wrong_txt_path = None

        self.open_dir_button.clicked.connect(self.open_dir)
        self.open_compare_dir_button.clicked.connect(self.open_compare_dir)
        self.classify_button.clicked.connect(self.classify)
        self.change_setting_button.clicked.connect(self.change_settings)
        self.create_txt_button.clicked.connect(self.get_txt)
        self.pic_dedup_button.clicked.connect(self.dedup_images)
        self.data_check_button.clicked.connect(self.data_check)
        self.compare_checkBox.clicked.connect(self.check_compare_checkbox)
        self.change_wrong_attribute_button.clicked.connect(self.open_rework_window)

        self.process_tabWidget.setEnabled(False)

        self.back_line.textChanged.connect(self.data_classify_info_label.clear)
        self.front_line.textChanged.connect(self.data_classify_info_label.clear)
        self.old_setting_line.textChanged.connect(self.attribute_change_info_label.clear)
        self.new_setting_line.textChanged.connect(self.attribute_change_info_label.clear)

        self.config_data = config.load_config()

        if self.config_data['visible'] != 'sunnyaiot':
            self.dedup_tab.hide()
            self.data_classify_tab.hide()
            self.create_count_tab.hide()

    def open_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self)
        if dir_path:
            self.dir_path = dir_path
            self.file_path_lable.setText(self.dir_path)
            self.process_tabWidget.setEnabled(True)
            self.reset_compare()
            if self.config_data['space_enabled'] == 'true':
                change_settings(self.dir_path, ' ', '')
            if self.config_data['IDcard'] == 'true':
                change_xjd(self.dir_path)

    def open_compare_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self)
        if dir_path:
            self.compare_dir_path = dir_path
            self.open_compare_dir_info_label.setText(f"已选择文件夹:{dir_path.split('/')[-1]}")

    def classify(self):
        def is_valid_input(text):
            return text.isdigit() or not text

        if not (is_valid_input(self.front_line.text()) and is_valid_input(self.back_line.text())):
            self.info_label.setText('输入错误，请输入数字或为空')
            return
        classify_id(self.dir_path, self.front_line.text(), self.back_line.text())

        self.process_tabWidget.setEnabled(False)
        self.file_path_lable.setText('分类完成，请打开新的文件夹')
        self.reset_compare()
        self.data_classify_info_label.setText('分类完成')

    def change_settings(self):
        self.old_setting_line.text().replace(' ', '')
        self.new_setting_line.text().replace(' ', '')
        if not self.old_setting_line.text() or not self.new_setting_line.text():
            self.attribute_change_info_label.setText('属性不能为空')
            return
        change_settings(self.dir_path, self.old_setting_line.text(), self.new_setting_line.text())
        self.attribute_change_info_label.setText('修改完成')

    def get_txt(self):
        creat_txt(self.dir_path, '数据地址文档')
        filename = self.dir_path.split('/')[-1] + '.txt'
        self.create_count_info_label.setText(f'已生成{filename}')

    def check_compare_checkbox(self):
        if self.compare_checkBox.isChecked():
            self.open_compare_dir_button.setEnabled(True)
            self.open_compare_dir_info_label.setText('请选择作为对比的文件夹')
        else:
            self.reset_compare()

    def reset_compare(self):
        self.compare_dir_path = None
        self.compare_checkBox.setChecked(False)
        self.open_compare_dir_button.setEnabled(False)
        self.open_compare_dir_info_label.clear()

    def dedup_images(self):
        max_distance_threshold = self.distance_line.text() if self.distance_line.text() else 0
        output_path = create_dir_name('去重后图像', 'dedup_images')
        dedup_cover = self.config_data['dedup_cover']
        if self.compare_checkBox.isChecked():
            if not self.compare_dir_path:
                self.info_label.setText('未导入对比文件夹')
                return
        dedup(self.dir_path, self.compare_dir_path, output_path, max_distance_threshold, dedup_cover)
        self.dedup_info_label.setText('去重完毕')

    def data_check(self):
        if self.config_data['space_enabled'] == 'true':
            change_settings(self.dir_path, ' ', '')
        if self.config_data['IDcard'] == 'true':
            change_xjd(self.dir_path)
        self.wrong_txt_path = get_wrong_paths_txt(self.dir_path, '问题数据', self.config_data['project_name'])
        if not self.wrong_txt_path:
            self.wrong_data_processing_info_label.setText('检查完毕,无错误数据')
        else:
            self.wrong_data_processing_info_label.setText('检查完毕')

    def open_rework_window(self):
        self.rework_window = ReworkWindow(txt_path=self.wrong_txt_path, project_name=self.config_data['project_name'])
        self.rework_window.show()

    def closeEvent(self, event):
        if self.rework_window:
            self.rework_window.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyClass()
    qt_material.apply_stylesheet(app, theme='default')
    myWin.show()
    sys.exit(app.exec_())
