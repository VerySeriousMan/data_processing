# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2023.12.18
Author: ZhangYuetao
File Name: main.py
Update: 2024.12.31
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.data_processing import *
import qt_material


if __name__ == '__main__':
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # 自适应适配不同分辨率
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    from ui.main.main_window import MainWindow  # 延迟导入，解决opencv与pyqt线程冲突问题

    myWin = MainWindow()
    qt_material.apply_stylesheet(app, theme='default')
    myWin.show()
    sys.exit(app.exec_())
