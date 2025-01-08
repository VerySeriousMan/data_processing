# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2024.12.24
Author: ZhangYuetao
File Name: work_thread.py
Update: 2025.01.08
"""
import os

from PyQt5.QtCore import QThread, pyqtSignal

import core
import utils


class WorkingThread(QThread):
    """
    工作线程类，用于在后台执行各种任务，避免阻塞主线程。

    Signals:
        status_signal (str): 用于向UI发送任务状态的信号。
        wrong_txt_signal (str): 用于传递错误数据文件路径的信号。
    """
    status_signal = pyqtSignal(str)  # 用于更新UI的信号
    wrong_txt_signal = pyqtSignal(str)  # 用于传递wrong_txt_path的信号

    def __init__(self, task_type, dir_path, *args):
        """
        初始化工作线程。

        :param task_type: 任务类型（如 'classify', 'dedup', 'add_watermark' 等）。
        :param dir_path: 目标文件夹路径。
        :param args: 根据任务类型传递的额外参数。
        """
        super().__init__()
        self.task_type = task_type
        self.dir_path = dir_path
        self.args = args

    def run(self):
        """
        线程运行的主方法，根据任务类型执行相应的任务。
        """
        try:
            if self.task_type == 'classify':
                self._classify()
            elif self.task_type == 'change_settings':
                self._change_settings()
            elif self.task_type == 'get_txt':
                self._get_txt()
            elif self.task_type == 'dedup':
                self._dedup()
            elif self.task_type == 'data_check':
                self._data_check()
            elif self.task_type == 'add_watermark':
                self._add_watermark()
            elif self.task_type == 'pre_classify':
                self._pre_classify()
            else:
                raise ValueError(f"Unknown task type: {self.task_type}")

        except Exception as e:
            self.status_signal.emit(f'{self.task_type} 失败：{str(e)}')

    def _classify(self):
        """
        执行分类任务。
        """
        try:
            front_line, back_line = self.args
            core.classify_id(self.dir_path, front_line, back_line)
            self.status_signal.emit('分类完成，请打开新的文件夹')
        except FileNotFoundError as e:
            self.status_signal.emit(f'分类失败：{str(e)}')
        except ValueError as e:
            self.status_signal.emit(f'分类失败：{str(e)}')
        except Exception as e:
            self.status_signal.emit(f'分类失败：未知错误 - {str(e)}')

    def _change_settings(self):
        """
        执行修改设置任务。
        """
        old_setting_line, new_setting_line = self.args
        utils.change_settings(self.dir_path, old_setting_line, new_setting_line)
        self.status_signal.emit('修改完成')

    def _get_txt(self):
        """
        执行生成文本文件任务。
        """
        utils.create_txt(self.dir_path, '数据地址文档')
        filename = self.dir_path.split('/')[-1] + '.txt'
        txt_path = os.path.join('数据地址文档', filename)
        self.status_signal.emit(f'已生成地址：{txt_path}')

    def _dedup(self):
        """
        执行去重任务。
        """
        compare_dir_path, output_path, similar_percent, dedup_cover = self.args
        error_list = core.dedup(self.dir_path, compare_dir_path, output_path, similar_percent, dedup_cover)

        if error_list:
            error_message = '\n'.join(error_list)
            self.status_signal.emit(f'去重完毕，存在以下错误:\n{error_message}')
        else:
            self.status_signal.emit(f'去重完毕')

    def _data_check(self):
        """
        执行数据检查任务。
        """
        project_name, space_enabled, IDcard = self.args
        if space_enabled == 'true':
            utils.change_settings(self.dir_path, ' ', '')
        if IDcard == 'true':
            utils.change_IDcard(self.dir_path)

        wrong_txt_path = core.get_wrong_paths_txt(self.dir_path, '问题数据', project_name)
        if not wrong_txt_path:
            self.status_signal.emit('检查完毕,无错误数据')
        else:
            self.status_signal.emit('检查完毕')
        self.wrong_txt_signal.emit(wrong_txt_path)

    def _add_watermark(self):
        """
        执行添加水印任务。
        """
        extra_info, output_path = self.args
        core.add_watermark(self.dir_path, extra_info, output_path)
        self.status_signal.emit('水印添加完成')

    def _pre_classify(self):
        """
        执行预分类任务。
        """
        classify_nums, classify_type, save_type = self.args
        if classify_type == '按文件名':
            core.image_classify_by_name(self.dir_path, classify_nums, save_type)
        else:
            core.image_classify(self.dir_path, classify_nums, classify_type, save_type)
        self.status_signal.emit('预分类完成')
