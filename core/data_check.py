# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2025.01.03
Author: ZhangYuetao
File Name: data_check.py
Update: 2025.01.03
"""

import os

import config
import utils


def is_wrong_filename(filename, project_name):
    """
    判断文件名是否符合要求

    :param filename: 文件名
    :param project_name: 项目名称
    :return: 是否为不合规文件名
    """
    if utils.is_have_chinese(filename):
        return True

    try:
        data = config.load_json(config.ATTRIBUTE_NAME_FILE)
    except:
        data = []

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


def get_batch_files(file, wrong_lines, project_name):
    """
    获取与文件名相似的不合规文件列表

    :param file: 文件名
    :param wrong_lines: 不合规文件行列表
    :param project_name: 项目名称
    :return: 不合规文件列表
    """
    res = config.load_ignore_re(project_name)
    batch_files = []
    file_cleaned = utils.remove_patterns(file, res)
    for line in wrong_lines:
        if file_cleaned == utils.remove_patterns(line, res):
            batch_files.append(line)
    return batch_files
