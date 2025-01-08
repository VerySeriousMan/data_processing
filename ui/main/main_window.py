# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2023.12.18
Author: ZhangYuetao
File Name: main_window.py
Update: 2025.01.08
"""

from functools import partial
from collections import ChainMap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox

from ui.data_processing import *
import utils
import config
from ui.main.rework_main import ReworkWindow
from ui.main.feedback_main import FeedbackWindow
from ui.main.watermark_setting_main import SettingsDialog
from threads.work_thread import WorkingThread
from network.software_update import Updater
from network import server_connect


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    数据预处理软件的主窗口类，提供文件处理、分类、去重、水印添加等功能。

    Attributes:
        dir_path (str): 当前处理的文件夹路径。
        compare_dir_path (str): 对比文件夹路径。
        rework_window (ReworkWindow): 错误数据修改窗口对象。
        feedback_window (FeedbackWindow): 问题反馈窗口对象。
        wrong_txt_path (str): 错误数据文件路径。
        current_software_path (str): 当前软件的可执行文件路径。
        current_software_version (str): 当前软件的版本号。
        updater(Updater): 自动更新类。
        working_thread (WorkingThread): 工作线程对象。
        timer (QTimer): 用于动画效果的定时器。
        animation_index (int): 动画索引，用于显示动态效果。
    """

    def __init__(self, parent=None):
        """
        初始化主窗口。

        :param parent: 父窗口对象，默认为 None。
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("数据预处理软件V2.0")
        self.setWindowIcon(QtGui.QIcon(config.ICO_FILE))

        self.dir_path = None
        self.compare_dir_path = None
        self.rework_window = None
        self.feedback_window = None
        self.wrong_txt_path = None
        self.current_software_path = utils.get_current_software_path()
        self.current_software_version = server_connect.get_current_software_version(self.current_software_path)
        # 合并默认配置和用户配置，用户配置优先级更高
        self.config_data = ChainMap(config.load_config(config.SETTING_FILE, {}), config.SETTING_DEFAULT_CONFIG)
        # 初始化 AutoUpdater
        self.updater = Updater(self.current_software_path, self.current_software_version)
        self.timer = QTimer(self)
        self.animation_index = 0
        self.working_thread = None

        # 连接信号与槽
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
        self.watermark_param_pushButton.clicked.connect(self.open_watermark_setting_window)
        self.pre_classify_button.clicked.connect(self.pre_classify)
        self.software_update_action.triggered.connect(self.updater.update_software)
        self.problem_feedback_action.triggered.connect(self.feedback_problem)

        self.process_tabWidget.setEnabled(False)
        self.save_type_checkBox.setChecked(True)

        self.back_line.textChanged.connect(self.data_classify_info_label.clear)
        self.front_line.textChanged.connect(self.data_classify_info_label.clear)
        self.old_setting_line.textChanged.connect(self.attribute_change_info_label.clear)
        self.new_setting_line.textChanged.connect(self.attribute_change_info_label.clear)
        self.process_tabWidget.currentChanged.connect(self.info_label_clear)

        self.file_path_lable.setText('请先点击’选择文件夹’按钮选择需要处理的文件夹')
        self.pre_classify_comboBox.addItems(['按创建时间', '按修改时间', '按图片相似度', '按文件名'])

        self.updater.auto_update()
        self.updater.init_update()

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

    def feedback_problem(self):
        """
        处理问题反馈操作，检查网络连接并打开反馈窗口。
        """
        if server_connect.check_version(self.current_software_version) == -1:
            QMessageBox.warning(self, '网络未连接', '网络未连接，请连接内网后再试')
        else:
            self.open_feedback_window()

    def open_dir(self):
        """
        打开目标文件夹，并初始化相关设置。
        """
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
        """
        打开对比文件夹，并更新UI。
        """
        dir_path = QFileDialog.getExistingDirectory(self)
        if dir_path:
            self.compare_dir_path = dir_path
            self.open_compare_dir_info_label.setText(f"已选择文件夹:{dir_path.split('/')[-1]}")

    def classify(self):
        """
        执行分类任务，启动工作线程。
        """
        self.data_classify_info_label.setText('开始分类')

        def _is_valid_input(text):
            return text.isdigit() or not text

        if not (_is_valid_input(self.front_line.text()) and _is_valid_input(self.back_line.text())):
            self.data_classify_info_label.setText('输入错误，请输入数字或为空')
            return

        self.start_thread('分类中', 'classify', self.data_classify_info_label,
                          self.front_line.text(), self.back_line.text())

    def change_settings(self):
        """
        执行修改设置任务，启动工作线程。
        """
        self.attribute_change_info_label.setText('开始修改')
        self.old_setting_line.text().replace(' ', '')
        self.new_setting_line.text().replace(' ', '')

        if not self.old_setting_line.text():
            self.attribute_change_info_label.setText('原属性不能为空')
            return
        if not self.enable_null_checkBox.isChecked():
            if not self.new_setting_line.text():
                self.attribute_change_info_label.setText('新属性不能为空')
                return

        self.start_thread('修改中', 'change_settings', self.attribute_change_info_label,
                          self.old_setting_line.text(), self.new_setting_line.text())

    def get_txt(self):
        """
        执行生成文本文件任务，启动工作线程。
        """
        self.create_count_info_label.setText(f'开始生成地址')

        self.start_thread('地址生成中', 'get_txt', self.create_count_info_label)

    def check_compare_checkbox(self):
        """
        处理对比文件夹复选框的点击事件，更新UI。
        """
        if self.compare_checkBox.isChecked():
            self.open_compare_dir_button.setEnabled(True)
            self.open_compare_dir_info_label.setText('请选择作为对比的文件夹')
        else:
            self.reset_compare()

    def reset_compare(self):
        """
        重置对比文件夹路径及相关UI。
        """
        self.compare_dir_path = None
        self.compare_checkBox.setChecked(False)
        self.open_compare_dir_button.setEnabled(False)
        self.open_compare_dir_info_label.clear()

    def dedup_images(self):
        """
        执行去重任务，启动工作线程。
        """
        self.dedup_info_label.setText('开始去重')
        similar_percent = int(self.distance_line.text()) if self.distance_line.text() else 100
        dedup_cover = self.config_data['dedup_cover']

        if dedup_cover == 'false':
            output_path = utils.create_dir_name('去重后图像', 'dedup_images')
        else:
            output_path = ''
        if self.compare_checkBox.isChecked():
            if not self.compare_dir_path:
                self.dedup_info_label.setText('未导入对比文件夹')
                return

        self.start_thread('去重中', 'dedup', self.dedup_info_label,
                          self.compare_dir_path, output_path, similar_percent, dedup_cover)

    def data_check(self):
        """
        执行数据检查任务，启动工作线程。
        """
        self.wrong_data_processing_info_label.setText('开始检查')

        self.start_thread('数据检查中', 'data_check', self.wrong_data_processing_info_label,
                          self.config_data['project_name'], self.config_data['space_enabled'],
                          self.config_data['IDcard'])

    def _handle_wrong_txt_path(self, wrong_txt_path):
        """
        处理错误数据文件路径，更新UI。

        :param wrong_txt_path: 错误数据文件路径。
        """
        self.wrong_txt_path = wrong_txt_path

    def add_watermarks(self):
        """
        执行添加水印任务，启动工作线程。
        """
        self.watermark_info_label.setText('开始添加水印')
        extra_info = self.extra_info_line.text()

        watermark_cover = self.config_data['watermark_cover']

        if watermark_cover == 'false':
            output_path = utils.create_dir_name('added_watermark_images', 'watermark_images')
        else:
            output_path = ''

        self.start_thread('水印添加中', 'add_watermark', self.watermark_info_label, extra_info, output_path)

    def pre_classify(self):
        """
        执行预分类任务，启动工作线程。
        """
        self.image_pre_classify_info_label.setText('开始预分类')
        classify_type = self.pre_classify_comboBox.currentText()
        classify_nums = int(self.pre_classify_nums_spinBox.text())
        if self.save_type_checkBox.isChecked():
            save_type = 'original'
        else:
            save_type = 'merge'

        if classify_type != '按文件名' and classify_nums == 0:
            self.image_pre_classify_info_label.setText('分类数不能为0')
            return

        self.start_thread('预分类中', 'pre_classify', self.image_pre_classify_info_label,
                          classify_nums, classify_type, save_type)

    def info_label_clear(self):
        """
        清空所有信息标签的内容。
        """
        self.open_compare_dir_info_label.clear()
        self.dedup_info_label.clear()
        self.data_classify_info_label.clear()
        self.create_count_info_label.clear()
        self.attribute_change_info_label.clear()
        self.wrong_data_processing_info_label.clear()
        self.watermark_info_label.clear()
        self.image_pre_classify_info_label.clear()

    def check_thread(self):
        """
        检查是否有正在运行的线程。

        :return: 如果没有正在运行的线程，返回 True；否则返回 False。
        """
        if self.working_thread and self.working_thread.isRunning():
            QMessageBox.warning(self, '线程占用', '有任务正在运行中，请勿重复提交')
            return False
        return True

    def start_thread(self, animation_name, task_type, info_label, *args):
        """
        启动工作线程，执行指定任务。

        :param animation_name: 动画名称，用于显示动态效果。
        :param task_type: 任务类型。
        :param info_label: 信息标签，用于显示任务状态。
        :param args: 任务所需的额外参数。
        """
        # 检查是否有正在运行的线程
        if not self.check_thread():
            return

        self.start_animation(animation_name, info_label)
        self.working_thread = WorkingThread(task_type, self.dir_path, *args)

        # 使用 functools.partial 来传递额外参数
        self.working_thread.status_signal.connect(partial(self.update_info_label, info_label))
        self.working_thread.wrong_txt_signal.connect(self._handle_wrong_txt_path)
        self.working_thread.finished.connect(self.stop_animation)
        self.working_thread.finished.connect(self.cleanup_thread)  # 确保线程结束时资源被清理

        self.working_thread.start()

    def cleanup_thread(self):
        """
        清理工作线程资源，确保线程结束时资源被释放。
        """
        # 检查每个线程是否存在，如果存在则停止并置为 None
        if self.working_thread and self.working_thread.isRunning():
            self.working_thread.deleteLater()
        self.working_thread = None  # 置为 None

    def start_animation(self, info, info_label):
        """
        启动动画效果，显示动态信息。

        :param info: 动画信息。
        :param info_label: 信息标签，用于显示动画效果。
        """
        self.animation_index = 0
        self.timer.timeout.connect(partial(self.update_animation, info, info_label))
        self.timer.start(500)

    def stop_animation(self):
        """
        停止动画效果。
        """
        if hasattr(self, 'timer'):
            self.timer.stop()
            self.timer.timeout.disconnect()  # 断开所有连接到 timeout 信号的槽函数

    def update_animation(self, info, info_label):
        """
        更新动画效果，显示动态信息。

        :param info: 动画信息。
        :param info_label: 信息标签，用于显示动画效果。
        """
        animation_dots = '.' * self.animation_index
        info_label.setText(f'{info}{animation_dots}')
        self.animation_index = (self.animation_index + 1) % 4

    @staticmethod
    def update_info_label(info_label, text):
        """
        更新信息标签的内容。

        :param info_label: 信息标签。
        :param text: 要显示的文本。
        """
        info_label.setText(text)

    def open_watermark_setting_window(self):
        dialog = SettingsDialog(self)
        dialog.exec_()

    def open_rework_window(self):
        """
        打开错误数据修改窗口。
        """
        self.rework_window = ReworkWindow(txt_path=self.wrong_txt_path, project_name=self.config_data['project_name'])
        self.rework_window.show()

    def open_feedback_window(self):
        """
        打开问题反馈窗口。
        """
        self.feedback_window = FeedbackWindow()
        self.feedback_window.show()

    def closeEvent(self, event):
        """
        处理窗口关闭事件，确保所有资源被释放。

        :param event: 关闭事件对象。
        """
        if self.working_thread and self.working_thread.isRunning():
            self.working_thread.terminate()  # 终止线程
            self.working_thread.wait()  # 等待线程完全结束
        self.working_thread = None  # 置为 None

        if self.rework_window:
            self.rework_window.close()
        if self.feedback_window:
            self.feedback_window.close()
        event.accept()
