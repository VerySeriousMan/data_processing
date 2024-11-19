# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2024.07.03
Author: ZhangYuetao
File Name: utils.py
Update: 2024.10.09
"""

import json
import os
import re
import shutil


def pre_id(file_path):
    """
    从给定的文本文件中读取ID
    :param file_path: 文本文件路径
    :return: 读取的ID列表
    """
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as file:
        txtID = [line.strip() for line in file]
    return txtID


def classify_id(dir_path, front_line, back_line):
    """
    根据ID将文件分类到测试和训练文件夹
    :param dir_path: 包含待分类文件的目录路径
    :param front_line: ID的前缀索引
    :param back_line: ID的后缀索引
    """
    for filename in os.listdir(dir_path):
        filepath = os.path.join(dir_path, filename)
        fileid = get_id(filename, front_line, back_line)
        test_path = os.path.join(dir_path + '_test', filename)
        train_path = os.path.join(dir_path + '_train', filename)
        test_id = pre_id(r'settings/testID.txt')
        train_id = pre_id(r'settings/trainID.txt')

        if fileid in test_id:
            shutil.move(filepath, test_path)
        elif fileid in train_id:
            shutil.move(filepath, train_path)


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


def change_IDcard(dir_path):
    """
    修改身份证文件夹名并移动内容
    :param dir_path: 目标目录路径
    """
    for dirname in os.listdir(dir_path):
        if dirname[-1] == 'x':
            new_dirname = dirname[:-1] + 'X'
            change_files(os.path.join(dir_path, dirname), dirname, new_dirname)

            new_path = os.path.join(dir_path, new_dirname)
            old_path = os.path.join(dir_path, dirname)

            if os.path.exists(new_path):
                move_folder_contents(old_path, new_path)
            else:
                os.rename(old_path, new_path)


def change_settings(dir_path, old_setting_line, new_setting_line):
    """
    修改设置文件名及其内容
    :param dir_path: 目标目录路径
    :param old_setting_line: 旧设置行
    :param new_setting_line: 新设置行
    """
    change_files(dir_path, old_setting_line, new_setting_line)

    for dirname in os.listdir(dir_path):
        if old_setting_line in dirname:
            new_dirname = dirname.replace(old_setting_line, new_setting_line)
            new_path = os.path.join(dir_path, new_dirname)
            old_path = os.path.join(dir_path, dirname)

            if os.path.exists(new_path):
                move_folder_contents(old_path, new_path)
            else:
                os.rename(old_path, new_path)


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


def creat_txt(dir_path, output_path):
    """
    创建包含目录下所有图像路径的文本文件
    :param dir_path: 要处理的目录路径
    :param output_path: 输出文件夹路径
    """
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    txt_name = dir_path.split('/')[-1] + '.txt'
    txt_path = os.path.join(output_path, txt_name)
    image_paths = []
    for root, _, files in os.walk(dir_path):
        image_paths.extend(os.path.join(root, file) for file in files)

    with open(txt_path, mode='w', encoding='utf-8') as txt:
        for path in image_paths:
            txt.writelines(path + '\n')


def get_id(filename: str, front_line, back_line):
    """
    从文件名中提取ID
    :param filename: 文件名
    :param front_line: ID的前缀索引
    :param back_line: ID的后缀索引
    :return: 提取的ID
    """
    front_line = int(front_line or 0)
    back_line = int(back_line or 0)

    if back_line == 0:
        return filename[front_line:]
    else:
        return filename[front_line:-back_line]


def create_dir_name(root_path, filename):
    """
    创建新的目录名称，避免重复
    :param root_path: 根目录路径
    :param filename: 基础文件名
    :return: 新创建的目录路径
    """
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    i = 1
    while os.path.exists(os.path.join(root_path, f'{filename}_{i}')):
        i += 1
    os.mkdir(os.path.join(root_path, f'{filename}_{i}'))
    return os.path.join(root_path, f'{filename}_{i}')


def get_wrong_paths_txt(root_path, output_path, project_name):
    """
    获取不符合要求的文件路径并保存到文本文件
    :param root_path: 要检查的根目录路径
    :param output_path: 输出文件夹路径
    :param project_name: 项目名称
    :return: 存储不合规路径的文件路径
    """
    wrong_paths = []
    for root, _, files in os.walk(root_path):
        for file in files:
            if is_wrong_filename(file, project_name):
                wrong_paths.append(os.path.join(root, file))

    if len(wrong_paths) > 0:
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        i = 1
        while os.path.exists(os.path.join(output_path, f'wrong_paths_{i}.txt')):
            i += 1
        wrong_file_path = os.path.join(output_path, f'wrong_paths_{i}.txt')
        with open(wrong_file_path, 'w', encoding='utf-8') as txt:
            for path in wrong_paths:
                txt.write(path + '\n')
        return wrong_file_path
    else:
        return None


def is_wrong_filename(filename, project_name):
    """
    判断文件名是否符合要求
    :param filename: 文件名
    :param project_name: 项目名称
    :return: 是否为不合规文件名
    """
    if re.search(r'[\u4e00-\u9fff]', filename) is not None:  # 判断是否含有中文
        return True
    with open('settings/attribute_name.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    project_config = data.get(project_name)
    if not project_config:
        return False

    check_value = project_config['check_value']
    check_range = project_config['check_range']
    check_length = project_config['check_length']

    start, end = map(int, check_length.split('-'))
    attributes = filename.split('_')
    if len(attributes) < end:
        return True
    attributes_to_check = attributes[start:end]

    for attribute in attributes_to_check:
        if attribute not in check_value and not any(r in attribute for r in check_range):
            return True

    return False


def get_ignore_re(project_name):
    """
    获取该项目需要忽略的正则表达式
    :param project_name: 项目名称
    :return: 需要忽略的正则表达式列表
    """
    with open('settings/batch_ignore.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    project_config = data.get(project_name)
    res = []

    if project_config:
        for regex in project_config.keys():
            res.append(regex)

    return res


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


def get_batch_files(file, wrong_lines, project_name):
    """
    获取与文件名相似的不合规文件列表
    :param file: 文件名
    :param wrong_lines: 不合规文件行列表
    :param project_name: 项目名称
    :return: 不合规文件列表
    """
    res = get_ignore_re(project_name)
    batch_files = []
    file_cleaned = remove_patterns(file, res)
    for line in wrong_lines:
        if file_cleaned == remove_patterns(line, res):
            batch_files.append(line)
    return batch_files


def save_line_to_txt(lines, save_path):
    """
    将指定行保存到文本文件
    :param lines: 行列表
    :param save_path: 保存路径
    """
    with open(save_path, 'w', encoding='utf-8') as txt:
        for line in lines:
            txt.write(line + '\n')
