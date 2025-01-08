# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2024.12.30
Author: ZhangYuetao
File Name: validation_utils.py
Update: 2025.01.08
"""

import re
import os
import sys
import time

from PIL import Image


def is_have_chinese(filename):
    """
    判断文件名是否含有中文。

    :param filename: 输入的文件名。
    :return: 如果含有中文返回 True，否则返回 False。
    """
    if re.search(r'[\u4e00-\u9fff]', filename) is not None:  # 判断是否含有中文
        return True
    else:
        return False


def get_current_software_path():
    """
    获取当前软件的可执行文件路径。

    :return: 当前软件的可执行文件路径。
    """
    # 检查是否是打包后的程序
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后的路径
        return os.path.abspath(sys.argv[0])
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'main.py')


def is_file_complete(file_path, timeout=60):
    """
    检查文件是否完全复制完成。

    :param file_path: 文件路径。
    :param timeout: 最大等待时间（秒）。
    :return: 如果文件复制完成则返回 True，否则返回 False。
    """
    if not os.path.exists(file_path):
        return False

    initial_size = os.path.getsize(file_path)
    time.sleep(1)  # 等待1秒钟，给文件写入一些时间
    final_size = os.path.getsize(file_path)

    # 如果文件大小没有变化，认为文件已复制完成
    if initial_size == final_size:
        return True

    # 如果文件大小仍在变化，则继续等待
    start_time = time.time()
    while time.time() - start_time < timeout:
        time.sleep(1)
        new_size = os.path.getsize(file_path)
        if new_size == final_size:
            return True
        final_size = new_size

    # 超过最大等待时间后认为文件未复制完成
    return False


# 判断文件是否为图片文件
def is_image(file_path, speed="normal"):
    """
    判断文件是否为图片文件

    :param file_path: 文件路径
    :param speed: 检测模式，'fast' 或 'normal'（默认）
    :return: True 如果是图片文件，否则 False
    """
    if speed == 'fast':
        return file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff'))

    else:
        try:
            with Image.open(file_path) as img:
                img.verify()  # 验证图片文件是否损坏
            return True
        except:
            return False


def is_all_of_type(target_type, *args):
    """
    检测所有数据是否都属于指定类型

    :param target_type: 目标类型（如 str, int, list 等）
    :param args: 不定数量的待检测数据
    :return: 如果所有数据都属于目标类型，返回 True；否则返回 False
    """
    return all(isinstance(arg, target_type) for arg in args)
