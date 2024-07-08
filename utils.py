# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2024.07.03
Author: ZhangYuetao
File Name: utils.py
last renew: 2024.07.04
"""

import os
import shutil


def pre_id(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        txtID = [line.strip() for line in file]
    return txtID


def move_folder_contents(old_path, new_path):
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


def change_xjd(dir_path):
    for filename in os.listdir(dir_path):
        if filename.lower().startswith('xjd') and 'x' in filename[3:]:
            change_files(os.path.join(dir_path, filename), filename[3:], filename[3:].replace('x', 'X'))

            new_filename = filename.replace(filename[3:], filename[3:].replace('x', 'X'))
            new_path = os.path.join(dir_path, new_filename)
            old_path = os.path.join(dir_path, filename)

            if os.path.exists(new_path):
                move_folder_contents(old_path, new_path)
            else:
                os.rename(old_path, new_path)


def change_settings(dir_path, old_setting_line, new_setting_line):
    change_files(dir_path, old_setting_line, new_setting_line)

    for filename in os.listdir(dir_path):
        if old_setting_line in filename:
            new_filename = filename.replace(old_setting_line, new_setting_line)
            new_path = os.path.join(dir_path, new_filename)
            old_path = os.path.join(dir_path, filename)

            if os.path.exists(new_path):
                move_folder_contents(old_path, new_path)
            else:
                os.rename(old_path, new_path)


def change_files(dir_path, old_setting_line, new_setting_line):
    for dirs, _, filenames in os.walk(dir_path):
        for filename in filenames:
            new_filename = filename.replace(old_setting_line, new_setting_line)
            os.rename(os.path.join(dirs, filename), os.path.join(dirs, new_filename))


def creat_txt(dir_path):
    txt_path = dir_path + '.txt'
    image_paths = []
    for root, _, files in os.walk(dir_path):
        image_paths.extend(os.path.join(root, file) for file in files)

    with open(txt_path, mode='w', encoding='utf-8') as txt:
        txt.writelines(path.replace('\\', '/') + '\n' for path in image_paths)


def get_id(filename: str, front_line, back_line):
    front_line = int(front_line or 0)
    back_line = int(back_line or 0)

    if back_line == 0:
        return filename[front_line:]
    else:
        return filename[front_line:-back_line]
