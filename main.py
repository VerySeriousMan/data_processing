# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2023.12.18
Author: ZhangYuetao
File Name: main.py
Update: 2025.02.21
"""

import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
import qt_material


if __name__ == '__main__':
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # 自适应适配不同分辨率
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    from ui.main.main_window import MainWindow  # 延迟导入，解决opencv与pyqt线程冲突问题

    window_title = "数据预处理软件V2.2.1"
    myWin = MainWindow(window_title)
    qt_material.apply_stylesheet(app, theme='default')
    myWin.show()
    sys.exit(app.exec_())
