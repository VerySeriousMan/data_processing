# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2024.07.03
Author: ZhangYuetao
File Name: utils.py
last renew: 2024.07.16
"""
import json
import os
import re
import shutil


def pre_id(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as file:
        txtID = [line.strip() for line in file]
    return txtID


def classify_id(dir_path, front_line, back_line):
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
    for root, _, files in os.walk(dir_path):
        for filename in files:
            new_filename = filename.replace(old_setting_line, new_setting_line)
            os.rename(os.path.join(root, filename), os.path.join(root, new_filename))


def creat_txt(dir_path, output_path):
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
    front_line = int(front_line or 0)
    back_line = int(back_line or 0)

    if back_line == 0:
        return filename[front_line:]
    else:
        return filename[front_line:-back_line]


def create_dir_name(root_path, filename):
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    i = 1
    while os.path.exists(os.path.join(root_path, f'{filename}_{i}')):
        i += 1
    os.mkdir(os.path.join(root_path, f'{filename}_{i}'))
    return os.path.join(root_path, f'{filename}_{i}')


def get_wrong_paths_txt(root_path, output_path, project_name):
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

    # 检查每个属性是否满足条件
    for attribute in attributes_to_check:
        if attribute not in check_value and not any(r in attribute for r in check_range):
            return True

    return False


def get_ignore_re(project_name):
    with open('settings/batch_ignore.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    project_config = data.get(project_name)
    res = []

    if project_config:
        for regex in project_config.keys():
            res.append(regex)

    return res


def remove_patterns(file, res):
    for pattern in res:
        file = re.sub(pattern, '', file)
    return file


def get_batch_files(file, wrong_lines, project_name):
    res = get_ignore_re(project_name)
    batch_files = []
    file_cleaned = remove_patterns(file, res)
    for line in wrong_lines:
        if file_cleaned == remove_patterns(line, res):
            batch_files.append(line)
    return batch_files


def save_line_to_txt(lines, save_path):
    with open(save_path, 'w', encoding='utf-8') as txt:
        for line in lines:
            txt.write(line + '\n')
