# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2024.12.30
Author: ZhangYuetao
File Name: text_utils.py
Update: 2025.01.03
"""

import os


def create_txt(dir_path, output_path):
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


def save_line_to_txt(lines, save_path):
    """
    将指定行保存到文本文件

    :param lines: 行列表
    :param save_path: 保存路径
    """
    with open(save_path, 'w', encoding='utf-8') as txt:
        for line in lines:
            txt.write(line + '\n')
