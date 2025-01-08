# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2024.07.10
Author: ZhangYuetao
File Name: rework_main.py
Update: 2025.01.08
"""

import os
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5 import QtGui

from ui.rework import Ui_Form
import core.data_check
import utils
import config


class ReworkWindow(QWidget, Ui_Form):
    """
    错误数据修改窗口类，用于批量或单个修改错误文件名。

    Attributes:
        txt_path (str): 错误文件路径的文本文件路径。
        project_name (str): 项目名称，用于文件名校验。
        wrong_lines (list): 存储错误文件路径的列表。
        process_type (str): 处理类型，'batch' 表示批量处理，'single' 表示单个处理。
    """

    def __init__(self, parent=None, txt_path=None, project_name=None):
        """
        初始化错误数据修改窗口。

        :param parent: 父窗口对象，默认为 None。
        :param txt_path: 错误文件路径的文本文件路径，默认为 None。
        :param project_name: 项目名称，默认为 None。
        """
        super(ReworkWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("错误数据修改")
        self.setWindowIcon(QtGui.QIcon(config.ICO_FILE))

        self.txt_path = txt_path
        self.project_name = project_name
        self.wrong_lines = []
        self.process_type = 'batch'

        # 连接信号与槽
        self.return_home_button.clicked.connect(self.return_main_window)
        self.batch_checkBox.clicked.connect(self.batch_box_clicked)
        self.single_checkBox.clicked.connect(self.single_box_clicked)
        self.open_txt_pushButton.clicked.connect(self.open_txt)
        self.change_button.clicked.connect(self.change_file)
        self.jump_button.clicked.connect(self.jump_file)

        self.batch_checkBox.setChecked(True)
        self.have_txt_path()

    def have_txt_path(self):
        """
        检查是否已加载错误文件路径的文本文件，并更新UI状态。
        """
        had = bool(self.txt_path)
        self.change_button.setEnabled(had)
        self.jump_button.setEnabled(had)
        if had:
            self.txt_path_label.setText(self.txt_path)
            self.get_wrong_lines()
            self.show_current_filename()
            self.count_nums()
        else:
            self.info_label.setText("请导入错误地址txt")

    def open_txt(self):
        """
        打开错误文件路径的文本文件，并加载错误文件路径。
        """
        if self.txt_path:
            utils.save_line_to_txt(self.wrong_lines, self.txt_path)
        file_path = QFileDialog.getOpenFileName(self)[0]
        if file_path:
            if not file_path.endswith(".txt"):
                self.info_label.setText("格式错误，请导入txt")
            else:
                self.txt_path = file_path
                self.have_txt_path()

    def get_wrong_lines(self):
        """
        从文本文件中读取错误文件路径，并存储到 `wrong_lines` 列表中。
        """
        self.wrong_lines = []
        try:
            with open(self.txt_path, 'r', encoding='utf-8') as files:
                for line in files:
                    self.wrong_lines.append(line.strip())  # 移除换行符
        except Exception as e:
            self.info_label.setText(f"读取文件时出错: {e}")

    def show_current_filename(self):
        """
        显示当前处理的文件名，并更新UI。
        """
        if self.wrong_lines:
            current_file_path = self.wrong_lines[0]
            current_filename = os.path.basename(current_file_path)
        else:
            current_filename = '---空---'
            current_file_path = '---空---'
            self.change_button.setEnabled(False)
            self.jump_button.setEnabled(False)
        self.old_filename_label.setText(current_file_path)
        self.change_filename_lineEdit.setText(current_filename)

    def count_nums(self):
        """
        统计剩余错误文件的数量，并更新UI。
        """
        nums = len(self.wrong_lines)
        self.num_label.setText(str(nums))  # 确保是字符串

    def batch_box_clicked(self):
        """
        处理 'batch' 复选框的点击事件，更新处理类型。
        """
        if self.batch_checkBox.isChecked():
            self.process_type = 'batch'
            self.single_checkBox.setChecked(False)
        else:
            self.process_type = 'single'
            self.single_checkBox.setChecked(True)

    def single_box_clicked(self):
        """
        处理 'single' 复选框的点击事件，更新处理类型。
        """
        if self.single_checkBox.isChecked():
            self.process_type = 'single'
            self.batch_checkBox.setChecked(False)
        else:
            self.process_type = 'batch'
            self.batch_checkBox.setChecked(True)

    def change_file(self):
        """
        处理修改文件名的操作，根据处理类型批量或单个修改文件名。
        """
        new_filename = self.change_filename_lineEdit.text()
        if core.is_wrong_filename(new_filename, self.project_name):
            self.info_label.setText('新的文件名不符合要求，请重新修改')
            return

        old_file = self.old_filename_label.text()
        try:
            if self.process_type == 'single':
                new_file = os.path.join(os.path.dirname(old_file), new_filename)
                os.rename(old_file, new_file)
                self.wrong_lines.remove(old_file)
            else:
                batch_files = core.get_batch_files(old_file, self.wrong_lines, self.project_name)
                for batch_file in batch_files:
                    new_file = os.path.join(os.path.dirname(batch_file), new_filename)
                    os.rename(batch_file, new_file)
                    self.wrong_lines.remove(batch_file)

            self.show_current_filename()
            self.count_nums()
            self.info_label.setText('修改完成，请修改下一张')
        except Exception as e:
            self.info_label.setText(f"重命名文件时出错: {e}")

    def jump_file(self):
        """
        处理跳过文件的操作，根据处理类型批量或单个跳过文件。
        """
        old_file = self.old_filename_label.text()
        try:
            if self.process_type == 'single':
                self.wrong_lines.remove(old_file)
            else:
                batch_files = core.get_batch_files(old_file, self.wrong_lines, self.project_name)
                for batch_file in batch_files:
                    self.wrong_lines.remove(batch_file)

            self.show_current_filename()
            self.count_nums()
            self.info_label.setText('已跳过')
        except Exception as e:
            self.info_label.setText(f"跳过文件时出错: {e}")

    def return_main_window(self):
        """
        处理返回主窗口的操作，保存剩余的错误文件路径并关闭窗口。
        """
        try:
            utils.save_line_to_txt(self.wrong_lines, self.txt_path)
        except Exception as e:
            self.info_label.setText(f"保存文件时出错: {e}")
        self.close()

    def closeEvent(self, event):
        """
        在窗口关闭事件发生时保存数据。

        :param event: 关闭事件对象。
        """
        try:
            utils.save_line_to_txt(self.wrong_lines, self.txt_path)
        except Exception as e:
            self.info_label.setText(f"保存文件时出错: {e}")
        event.accept()  # 接受关闭事件，允许窗口关闭
