# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2025.01.02
Author: ZhangYuetao
File Name: watermark_setting_main.py
Update: 2025.01.06
"""

from ui.watermark_setting import Ui_Dialog
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui, QtWidgets

import config


class SettingsDialog(QDialog, Ui_Dialog):
    """
    水印参数设置对话框类，用于配置水印的字体、位置、颜色、透明度等参数。

    Attributes:
        config (dict): 水印配置字典，从 TOML 文件中加载。
        org_place (str): 水印位置。
        org_x (int): 水印距离边缘的 x 像素值。
        org_y (int): 水印距离边缘的 y 像素值。
        color_red (int): 字体颜色的红色分量。
        color_green (int): 字体颜色的绿色分量。
        color_blue (int): 字体颜色的蓝色分量。
        font_face (str): 字体类型。
        font_scale (float): 字体缩放比例。
        thickness (int): 字体粗细。
        alpha (float): 水印不透明度，值范围 0（完全透明）到 1（完全不透明）。
        cnt_type (str): 统计方式。
    """

    def __init__(self, parent=None):
        """
        初始化水印参数设置对话框。

        :param parent: 父窗口对象，默认为 None。
        """
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("水印参数设置")
        self.setWindowIcon(QtGui.QIcon(config.ICO_FILE))

        self.config = config.load_config(config.WATERMARK_ATTR_FILE, config.WATERMARK_DEFAULT_CONFIG)

        org_parts = self.config['org'].split(',')
        self.org_place = org_parts[0].strip()  # 水印位置
        self.org_x = int(org_parts[1].strip())  # 水印距离边缘x像素值
        self.org_y = int(org_parts[2].strip())  # 水印距离边缘y像素值

        # 解析 color
        color_str = self.config['color'].strip('()')
        color_parts = color_str.split(',')
        self.color_red = int(color_parts[2].strip())
        self.color_green = int(color_parts[1].strip())
        self.color_blue = int(color_parts[0].strip())

        self.font_face = str(self.config['fontFace'])  # 字体类型
        self.font_scale = float(self.config['fontScale'])  # 字体缩放比例
        self.thickness = int(self.config['thickness'])   # 字体粗细
        self.alpha = float(self.config['alpha'])  # 水印不透明度，值范围0（完全透明）到1（完全不透明）
        self.cnt_type = str(self.config['num_way'])  # 统计方式

        self.font_face_comboBox.addItems(config.FONT_FACE_MAP.keys())
        self.org_place_comboBox.addItems(config.ORG_PLACE_MAP.keys())
        self.cnt_type_comboBox.addItems(config.CNT_TYPE_MAP.keys())

        self.buttonBox.accepted.connect(self.accept_settings)

        # 绑定事件处理函数
        self.thickness_lineEdit.textChanged.connect(self.validate_thickness)
        self.font_scale_doubleSpinBox.valueChanged.connect(self.validate_font_scale)
        self.red_lineEdit.textChanged.connect(self.validate_color_red)
        self.green_lineEdit.textChanged.connect(self.validate_color_green)
        self.blue_lineEdit.textChanged.connect(self.validate_color_blue)
        self.org_x_spinBox.valueChanged.connect(self.validate_org_x)
        self.org_y_spinBox.valueChanged.connect(self.validate_org_y)
        self.alpha_doubleSpinBox.valueChanged.connect(self.validate_alpha)

        self.init_show()

    def init_show(self):
        """
        初始化界面控件的显示状态。

        根据当前配置参数的值，设置各个控件的初始状态。
        """
        # 设置字体类型
        for text, value in config.FONT_FACE_MAP.items():
            if value == self.font_face:
                self.font_face_comboBox.setCurrentText(text)
                break

        # 设置水印位置
        for text, value in config.ORG_PLACE_MAP.items():
            if value == self.org_place:
                self.org_place_comboBox.setCurrentText(text)
                break

        # 设置统计方式
        for text, value in config.CNT_TYPE_MAP.items():
            if value == self.cnt_type:
                self.cnt_type_comboBox.setCurrentText(text)
                break

        self.thickness_lineEdit.setText(str(self.thickness))
        self.font_scale_doubleSpinBox.setValue(self.font_scale)
        self.red_lineEdit.setText(str(self.color_red))
        self.green_lineEdit.setText(str(self.color_green))
        self.blue_lineEdit.setText(str(self.color_blue))
        self.org_x_spinBox.setValue(self.org_x)
        self.org_y_spinBox.setValue(self.org_y)
        self.alpha_doubleSpinBox.setValue(self.alpha)

    def validate_thickness(self):
        """
        验证字体粗细是否符合格式要求。
        """
        try:
            thickness = int(self.thickness_lineEdit.text())
            if thickness <= 0:
                self.info_label.setText("错误：字体粗细必须大于0")
                self.submit_enabled(False)
            else:
                self.info_label.setText("")
                self.submit_enabled(True)
        except ValueError:
            self.info_label.setText("错误：字体粗细必须为正整数")
            self.submit_enabled(False)

    def validate_font_scale(self):
        """
        验证字体缩放比例是否符合格式要求。
        """
        font_scale = self.font_scale_doubleSpinBox.value()
        if font_scale <= 0:
            self.info_label.setText("错误：字体缩放比例必须为正浮点数")
            self.submit_enabled(False)
        else:
            self.info_label.setText("")
            self.submit_enabled(True)

    def validate_color_red(self):
        """
        验证红色分量是否符合格式要求。
        """
        self._validate_color_component(self.red_lineEdit, "红色")

    def validate_color_green(self):
        """
        验证绿色分量是否符合格式要求。
        """
        self._validate_color_component(self.green_lineEdit, "绿色")

    def validate_color_blue(self):
        """
        验证蓝色分量是否符合格式要求。
        """
        self._validate_color_component(self.blue_lineEdit, "蓝色")

    def _validate_color_component(self, line_edit, color_name):
        """
        通用方法：验证颜色分量是否符合格式要求。
        """
        try:
            value = int(line_edit.text())
            if value < 0 or value > 255:
                self.info_label.setText(f"错误：{color_name}分量必须在0到255之间")
                self.submit_enabled(False)
            else:
                self.info_label.setText("")
        except ValueError:
            self.info_label.setText(f"错误：{color_name}分量必须为整数")
            self.submit_enabled(False)

    def validate_org_x(self):
        """
        验证水印X偏移量是否符合格式要求。
        """
        org_x = self.org_x_spinBox.value()
        if org_x < 0:
            self.info_label.setText("错误：水印X偏移量必须为非负整数")
            self.submit_enabled(False)
        else:
            self.info_label.setText("")
            self.submit_enabled(True)

    def validate_org_y(self):
        """
        验证水印Y偏移量是否符合格式要求。
        """
        org_y = self.org_y_spinBox.value()
        if org_y < 0:
            self.info_label.setText("错误：水印Y偏移量必须为非负整数")
            self.submit_enabled(False)
        else:
            self.info_label.setText("")
            self.submit_enabled(True)

    def validate_alpha(self):
        """
        验证透明度是否符合格式要求。
        """
        alpha = self.alpha_doubleSpinBox.value()
        if alpha < 0 or alpha > 1:
            self.info_label.setText("错误：透明度必须在0到1之间")
            self.submit_enabled(False)
        else:
            self.info_label.setText("")
            self.submit_enabled(True)

    def submit_enabled(self, enable):
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(enable)

    def update_settings(self):
        """
        更新参数。
        """
        # 获取用户修改的值
        self.font_face = config.FONT_FACE_MAP[self.font_face_comboBox.currentText()]
        self.org_place = config.ORG_PLACE_MAP[self.org_place_comboBox.currentText()]
        self.cnt_type = config.CNT_TYPE_MAP[self.cnt_type_comboBox.currentText()]
        self.thickness = int(self.thickness_lineEdit.text())
        self.font_scale = self.font_scale_doubleSpinBox.value()
        self.color_red = int(self.red_lineEdit.text())
        self.color_green = int(self.green_lineEdit.text())
        self.color_blue = int(self.blue_lineEdit.text())
        self.org_x = self.org_x_spinBox.value()
        self.org_y = self.org_y_spinBox.value()
        self.alpha = self.alpha_doubleSpinBox.value()

    def save_settings_to_toml(self):
        """
        将用户修改的配置保存到 TOML 文件中。

        从界面控件中获取用户修改的值，更新配置字典，并保存到 TOML 文件。
        """
        self.update_settings()

        # 更新配置字典
        self.config['fontFace'] = self.font_face
        self.config['org'] = f"{self.org_place}, {self.org_x}, {self.org_y}"
        self.config['num_way'] = self.cnt_type
        self.config['thickness'] = self.thickness
        self.config['fontScale'] = self.font_scale
        self.config['color'] = f"({self.color_blue}, {self.color_green}, {self.color_red})"
        self.config['alpha'] = self.alpha

        # 保存到 TOML 文件
        config.save_config(config.WATERMARK_ATTR_FILE, self.config)

    def accept_settings(self):
        """
        保存用户修改的配置并关闭对话框。

        调用 `save_settings_to_toml` 方法保存配置，然后关闭对话框。
        """
        self.save_settings_to_toml()  # 保存配置
        self.accept()  # 关闭对话框
