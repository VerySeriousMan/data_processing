# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2024.12.30
Author: ZhangYuetao
File Name: file_utils.py
Update: 2025.02.21
"""

import os
import re
import shutil


def move_folder_contents(old_path, new_path):
    """
    移动文件夹中的所有内容到新路径

    :param old_path: 原文件夹路径
    :param new_path: 目标文件夹路径
    """
    for root, dirs, files in os.walk(old_path):
        for dir_name in dirs:
            old_dir = os.path.join(root, dir_name)
            new_dir = os.path.join(new_path, os.path.relpath(old_dir, old_path))
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)

        for file_name in files:
            old_file = os.path.join(root, file_name)
            new_file = os.path.join(new_path, os.path.relpath(old_file, old_path))
            shutil.copy2(old_file, new_file)

    shutil.rmtree(old_path)


def change_files(dir_path, old_setting_line, new_setting_line):
    """
    修改指定目录下文件的名称

    :param dir_path: 目标目录路径
    :param old_setting_line: 旧设置行
    :param new_setting_line: 新设置行
    """
    for root, _, files in os.walk(dir_path):
        for filename in files:
            new_filename = filename.replace(old_setting_line, new_setting_line)
            os.rename(os.path.join(root, filename), os.path.join(root, new_filename))


def change_settings(dir_path, old_setting_line, new_setting_line):
    """
    修改设置文件名及其内容

    :param dir_path: 目标目录路径
    :param old_setting_line: 旧设置行
    :param new_setting_line: 新设置行
    :return: 返回修改后的新目录路径或空。
    """
    change_files(dir_path, old_setting_line, new_setting_line)

    for dir_name in os.listdir(dir_path):
        if old_setting_line in dir_name:
            new_dir_name = dir_name.replace(old_setting_line, new_setting_line)
            new_path = os.path.join(dir_path, new_dir_name)
            old_path = os.path.join(dir_path, dir_name)

            if os.path.exists(new_path):
                move_folder_contents(old_path, new_path)
            else:
                os.rename(old_path, new_path)

    new_dir_path = change_current_dir_id(dir_path, old_setting_line, new_setting_line)

    return new_dir_path


def change_current_dir_id(dir_path, old_id, new_id):
    """
    修改当前目录的名称，将目录名中的旧ID替换为新ID。

    :param dir_path: 当前目录路径，表示需要修改的文件夹路径。
    :param old_id: 旧ID，表示需要被替换的字符串。
    :param new_id: 新ID，表示替换后的字符串。
    :return: 如果新ID是数字且替换成功，返回新目录路径；否则返回None。
    """
    if new_id.isdigit():
        dir_name = os.path.basename(dir_path)
        if old_id in dir_name:
            new_dir_name = dir_name.replace(old_id, new_id)
            new_dir_path = os.path.join(os.path.dirname(dir_path), new_dir_name)

            if os.path.exists(new_dir_path):
                move_folder_contents(dir_path, new_dir_path)
            else:
                os.rename(dir_path, new_dir_path)

            return new_dir_path

    return None


def change_IDcard(dir_path):
    """
    修改身份证文件夹名并移动内容

    :param dir_path: 目标目录路径
    """
    for dir_name in os.listdir(dir_path):
        if dir_name[-1] == 'x':
            new_dir_name = dir_name[:-1] + 'X'
            change_files(os.path.join(dir_path, dir_name), dir_name, new_dir_name)

            new_path = os.path.join(dir_path, new_dir_name)
            old_path = os.path.join(dir_path, dir_name)

            if os.path.exists(new_path):
                move_folder_contents(old_path, new_path)
            else:
                os.rename(old_path, new_path)


def create_dir_name(root_path, filename, start_origen=False):
    """
    创建新的目录名称，避免重复

    :param root_path: 根目录路径
    :param filename: 基础文件名
    :param start_origen: 从不跟后缀开始命名
    :return: 新创建的目录路径
    """
    if not os.path.exists(root_path):
        os.makedirs(root_path)

    if start_origen:
        dir_name = os.path.join(root_path, f'{filename}')
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
            return dir_name

    i = 1
    while os.path.exists(os.path.join(root_path, f'{filename}_{i}')):
        i += 1
    os.mkdir(os.path.join(root_path, f'{filename}_{i}'))
    return os.path.join(root_path, f'{filename}_{i}')


def remove_patterns(file, res):
    """
    根据忽略的正则表达式移除文件名中的模式

    :param file: 文件名
    :param res: 正则表达式列表
    :return: 清理后的文件名
    """
    for pattern in res:
        file = re.sub(pattern, '', file)
    return file
