# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2023.12.18
Author: ZhangYuetao
File Name: main.py
Update: 2024.11.19
"""

import os.path
import shutil
import subprocess
import sys
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from data_processing import *
import qt_material

import utils
import config
from pic_dedup import dedup
from rework_main import ReworkWindow
from data_classify import image_classify, image_classify_by_name
import server_connect


class MyClass(QMainWindow, Ui_MainWindow):
    # 定义默认参数值
    DEFAULT_CONFIG = {
        'visible': 'outside',
        'dedup_cover': 'false',
        'space_enabled': 'false',
        'IDcard': 'true',
        'project_name': 'face_and_palm_live'
    }

    def __init__(self, parent=None):
        super(MyClass, self).__init__(parent)

        self.setupUi(self)
        self.setWindowTitle("数据预处理软件V1.7")
        self.setWindowIcon(QtGui.QIcon("xey.ico"))

        self.dir_path = None
        self.compare_dir_path = None
        self.rework_window = None
        self.wrong_txt_path = None
        self.current_software_path = self.get_file_path()
        self.current_software_version = server_connect.get_current_software_version(self.current_software_path)

        self.open_dir_button.clicked.connect(self.open_dir)
        self.open_compare_dir_button.clicked.connect(self.open_compare_dir)
        self.classify_button.clicked.connect(self.classify)
        self.change_setting_button.clicked.connect(self.change_settings)
        self.create_txt_button.clicked.connect(self.get_txt)
        self.pic_dedup_button.clicked.connect(self.dedup_images)
        self.data_check_button.clicked.connect(self.data_check)
        self.compare_checkBox.clicked.connect(self.check_compare_checkbox)
        self.change_wrong_attribute_button.clicked.connect(self.open_rework_window)
        self.add_watermark_button.clicked.connect(self.add_watermarks)
        self.pre_classify_button.clicked.connect(self.pre_classify)
        self.software_update_action.triggered.connect(self.update_software)

        self.process_tabWidget.setEnabled(False)
        self.save_type_checkBox.setChecked(True)

        self.back_line.textChanged.connect(self.data_classify_info_label.clear)
        self.front_line.textChanged.connect(self.data_classify_info_label.clear)
        self.old_setting_line.textChanged.connect(self.attribute_change_info_label.clear)
        self.new_setting_line.textChanged.connect(self.attribute_change_info_label.clear)
        self.process_tabWidget.currentChanged.connect(self.info_label_clear)

        self.config_data = config.load_config(r'settings/setting.toml', self.DEFAULT_CONFIG)
        self.file_path_lable.setText('请先点击’选择文件夹’按钮选择需要处理的文件夹')
        self.pre_classify_comboBox.addItems(['按创建时间', '按修改时间', '按图片相似度', '按文件名'])
        self.auto_update()
        self.init_update()

        if self.config_data['visible'] != 'sunnyaiot':
            # 获取选项卡的索引
            dedup_index = self.process_tabWidget.indexOf(self.dedup_tab)
            classify_index = self.process_tabWidget.indexOf(self.data_classify_tab)
            watermark_index = self.process_tabWidget.indexOf(self.watermark_tab)
            image_pre_classify = self.process_tabWidget.indexOf(self.image_pre_classify_tab)
            count_index = self.process_tabWidget.indexOf(self.create_count_tab)

            # 按照索引从大到小排序
            indices = sorted([dedup_index, classify_index, watermark_index, image_pre_classify, count_index],
                             reverse=True)

            # 移除选项卡
            for index in indices:
                self.process_tabWidget.removeTab(index)
        else:
            watermark_index = self.process_tabWidget.indexOf(self.watermark_tab)
            self.process_tabWidget.removeTab(watermark_index)

    def init_update(self):
        dir_path = os.path.dirname(self.current_software_path)
        dir_name = os.path.basename(dir_path)
        if dir_name == 'temp':
            old_dir_path = os.path.dirname(dir_path)
            for file in os.listdir(old_dir_path):
                if file.endswith('.exe'):
                    old_software = os.path.join(old_dir_path, file)
                    os.remove(old_software)
            shutil.copy2(self.current_software_path, old_dir_path)
            new_file_path = os.path.join(old_dir_path, os.path.basename(self.current_software_path))
            if os.path.exists(new_file_path) and server_connect.is_file_complete(new_file_path):
                msg_box = QMessageBox(self)  # 创建一个新的 QMessageBox 对象
                reply = msg_box.question(self, '更新完成', '软件更新完成，需要立即重启吗？',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                msg_box.raise_()  # 确保弹窗显示在最上层

                if reply == QMessageBox.Yes:
                    subprocess.Popen(new_file_path)
                    time.sleep(1)
                    sys.exit("程序已退出")
                else:
                    sys.exit("程序已退出")
        else:
            is_updated = 0
            for file in os.listdir(dir_path):
                if file == 'temp':
                    is_updated = 1
                    shutil.rmtree(file)
            if is_updated == 1:
                try:
                    text = server_connect.get_update_log('数据预处理软件')
                    QMessageBox.information(self, '更新成功', f'更新成功！\n{text}')
                except Exception as e:
                    QMessageBox.critical(self, '更新成功', f'日志加载失败: {str(e)}')

    @staticmethod
    def get_file_path():
        # 检查是否是打包后的程序
        if getattr(sys, 'frozen', False):
            # PyInstaller 打包后的路径
            current_path = os.path.abspath(sys.argv[0])
        else:
            # 非打包情况下的路径
            current_path = os.path.abspath(__file__)
        return current_path

    def auto_update(self):
        dir_path = os.path.dirname(self.current_software_path)
        dir_name = os.path.basename(dir_path)
        if dir_name != 'temp':
            if server_connect.check_version(self.current_software_version) == 1:
                self.update_software()

    def update_software(self):
        update_way = server_connect.check_version(self.current_software_version)
        if update_way == -1:
            # 网络未连接，弹出提示框
            QMessageBox.warning(self, '更新提示', '网络未连接，暂时无法更新')
        elif update_way == 0:
            # 当前已为最新版本，弹出提示框
            QMessageBox.information(self, '更新提示', '当前已为最新版本')
        else:
            # 弹出提示框，询问是否立即更新
            msg_box = QMessageBox(self)  # 创建一个新的 QMessageBox 对象
            reply = msg_box.question(self, '更新提示', '发现新版本，开始更新吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            msg_box.raise_()  # 确保弹窗显示在最上层

            if reply == QMessageBox.Yes:
                try:
                    server_connect.update_software(os.path.dirname(self.current_software_path), '数据预处理软件')
                    text = server_connect.get_update_log('数据预处理软件')
                    QMessageBox.information(self, '更新成功', f'更新成功！\n{text}')
                except Exception as e:
                    QMessageBox.critical(self, '更新失败', f'更新失败: {str(e)}')
            else:
                pass

    def open_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self)
        if dir_path:
            self.dir_path = dir_path
            self.file_path_lable.setText(f'已打开{self.dir_path}')
            self.process_tabWidget.setEnabled(True)
            self.reset_compare()
            if self.config_data['space_enabled'] == 'true':
                utils.change_settings(self.dir_path, ' ', '')
            if self.config_data['IDcard'] == 'true':
                utils.change_IDcard(self.dir_path)

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
        utils.classify_id(self.dir_path, self.front_line.text(), self.back_line.text())

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
        utils.change_settings(self.dir_path, self.old_setting_line.text(), self.new_setting_line.text())
        self.attribute_change_info_label.setText('修改完成')

    def get_txt(self):
        utils.creat_txt(self.dir_path, '数据地址文档')
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
        similar_percent = int(self.distance_line.text()) if self.distance_line.text() else 100
        dedup_cover = self.config_data['dedup_cover']
        if dedup_cover == 'false':
            output_path = utils.create_dir_name('去重后图像', 'dedup_images')
        else:
            output_path = ''
        if self.compare_checkBox.isChecked():
            if not self.compare_dir_path:
                self.info_label.setText('未导入对比文件夹')
                return
        error_list = dedup(self.dir_path, self.compare_dir_path, output_path, similar_percent, dedup_cover)
        self.dedup_info_label.setText('去重完毕')

        if error_list:
            error_message = '\n'.join(error_list)
            self.dedup_info_label.setText(f'去重完毕，存在以下错误:\n{error_message}')

    def data_check(self):
        if self.config_data['space_enabled'] == 'true':
            utils.change_settings(self.dir_path, ' ', '')
        if self.config_data['IDcard'] == 'true':
            utils.change_IDcard(self.dir_path)
        self.wrong_txt_path = utils.get_wrong_paths_txt(self.dir_path, '问题数据', self.config_data['project_name'])
        if not self.wrong_txt_path:
            self.wrong_data_processing_info_label.setText('检查完毕,无错误数据')
        else:
            self.wrong_data_processing_info_label.setText('检查完毕')

    def add_watermarks(self):
        extra_info = self.extra_info_line.text()
        add_watermark(self.dir_path, extra_info)
        self.watermark_info_label.setText('水印添加完成')

    def pre_classify(self):
        classify_type = self.pre_classify_comboBox.currentText()
        classify_nums = int(self.pre_classify_nums_spinBox.text())
        if self.save_type_checkBox.isChecked():
            save_type = 'original'
        else:
            save_type = 'merge'

        try:
            if classify_type == '按文件名':
                image_classify_by_name(self.dir_path, classify_nums, save_type)
                self.image_pre_classify_info_label.setText('预分类完成')
            else:
                if classify_nums == 0:
                    self.image_pre_classify_info_label.setText('分类数不能为0')
                else:
                    image_classify(self.dir_path, classify_nums, classify_type, save_type)
                    self.image_pre_classify_info_label.setText('预分类完成')
        except Exception as e:
            self.image_pre_classify_info_label.setText(str(e))

    def info_label_clear(self):
        self.open_compare_dir_info_label.clear()
        self.dedup_info_label.clear()
        self.data_classify_info_label.clear()
        self.create_count_info_label.clear()
        self.attribute_change_info_label.clear()
        self.wrong_data_processing_info_label.clear()
        self.watermark_info_label.clear()
        self.image_pre_classify_info_label.clear()

    def open_rework_window(self):
        self.rework_window = ReworkWindow(txt_path=self.wrong_txt_path, project_name=self.config_data['project_name'])
        self.rework_window.show()

    def closeEvent(self, event):
        if self.rework_window:
            self.rework_window.close()
        event.accept()


if __name__ == '__main__':
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # 自适应适配不同分辨率
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    from watermark import add_watermark  # 延迟导入，解决opencv与pyqt线程冲突问题

    myWin = MyClass()
    qt_material.apply_stylesheet(app, theme='default')
    myWin.show()
    sys.exit(app.exec_())
