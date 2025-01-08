# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2024.09.30
Author: ZhangYuetao
File Name: pre_classify.py
Update: 2025.01.08
"""

import os
import shutil

import imagehash
import numpy as np

from PIL import Image

import config
import utils


# 获取哈希值，用于相似度分类
def get_image_similarity(file_path):
    """
    计算图像的哈希值，并将其转换为 64 位二进制数组。

    :param file_path: 图像文件路径
    :return: 64 位二进制的整数数组
    """
    img = Image.open(file_path)
    hash_value = imagehash.phash(img)
    # 将哈希值转换为整数后转换为二进制字符串，并填充到64位
    binary_str = bin(int(str(hash_value), 16))[2:].zfill(64)
    return np.array([int(bit) for bit in binary_str])  # 返回64位二进制的整数数组


# 主分类函数，使用自定义距离的 K-means++ 算法进行分类
def image_classify(dir_path, nums, classify_by, save_type='original'):
    """
    对文件夹中的图片文件按指定的分类依据进行聚类分类，并按聚类结果将文件移动到不同的文件夹

    :param dir_path: 要分类的文件夹路径
    :param nums: 聚类的簇数
    :param save_type: 保存类型，选择是否保存原格式
    :param classify_by: 分类依据
    """
    dir_path = str(dir_path)
    if not os.path.exists(dir_path):
        raise FileNotFoundError("文件夹不存在")

    file_features = []  # 保存文件特征（如创建时间、文件名哈希值、图片相似度等）
    file_paths = []  # 保存文件路径

    # 遍历文件夹，收集图片文件的特征（根据指定分类依据）
    for root, _, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            if utils.is_image(file_path):
                if classify_by == "按创建时间":
                    feature = np.array([os.path.getctime(file_path)])  # 按创建时间分类，特征为时间戳
                elif classify_by == "按修改时间":
                    feature = np.array([os.path.getmtime(file_path)])  # 按修改时间分类，特征为时间戳
                elif classify_by == "按图片相似度":
                    feature = np.array(list(get_image_similarity(file_path)))  # 按图片相似度分类，特征为哈希值的字符
                else:
                    raise TypeError(f"未知的分类依据: {classify_by}")

                file_features.append(feature)  # 将特征封装为列表，适应后续算法
                file_paths.append(file_path)  # 保存文件路径

    if not file_features:
        raise FileNotFoundError("没有找到有效的图片文件")

    # 将文件特征转换为 NumPy 数组，以便用于聚类
    file_features_array = np.array(file_features)

    # # 进行数据归一化处理
    # normalized_features = normalize_data(file_features_array)

    # 选择合适的距离度量
    if classify_by == "按创建时间" or classify_by == "按修改时间":
        distance_type = "euclidean"
    else:
        distance_type = "hamming"

    # 调用手动实现的 K-means 算法进行聚类
    clusters, centers = utils.kmeans_plus_custom(file_features_array, nums, distance_type=distance_type)

    # 根据聚类结果将文件移动到相应的分类文件夹，同时保持原路径结构
    for cluster_idx, file_idx_list in clusters.items():
        # 创建分类文件夹，按簇的编号命名
        classify_folder = f"{os.path.basename(dir_path)}_classify_{cluster_idx}"
        classify_path = os.path.join(dir_path, classify_folder)

        if not os.path.exists(classify_path):
            os.makedirs(classify_path)

        if save_type == 'original':
            # 将属于该簇的文件移动到相应的文件夹中，同时保持原文件夹的相对路径结构
            for file_idx in file_idx_list:  # 使用文件的原始索引
                if file_idx < len(file_paths):
                    file_path = file_paths[file_idx]

                    # 获取文件的相对路径，重现其文件夹结构
                    relative_path = os.path.relpath(file_path, dir_path)
                    target_path = os.path.join(classify_path, relative_path)

                    # 创建目标文件的父文件夹（如果不存在的话）
                    target_dir = os.path.dirname(target_path)
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)

                    # 复制文件到分类文件夹中保持原结构
                    shutil.copy(file_path, target_path)
                else:
                    raise IndexError(f"无效的索引: {file_idx}, 超出范围: {len(file_paths)}")
        else:
            # 将属于该簇的文件移动到相应的文件夹中
            for file_idx in file_idx_list:  # 使用文件的原始索引
                if file_idx < len(file_paths):
                    file_path = file_paths[file_idx]
                    shutil.copy(file_path, classify_path)  # 复制文件到分类文件夹
                else:
                    raise IndexError(f"无效的索引: {file_idx}, 超出范围: {len(file_paths)}")


def get_classify_line_name(filename, line_num):
    """
    获取对应下划线数下的属性值

    :param filename: 文件名
    :param line_num: 下划线数
    :return parts[line_num]: 下划线数对应的值
    """
    parts = filename.split("_")
    if line_num < len(parts):
        return parts[line_num]
    else:
        raise IndexError(f"{filename}下划线数量不足")


def image_classify_by_name(dir_path, line_num, save_type='original'):
    """
    文件夹按文件名中的某一个属性进行划分

    :param dir_path: 要分类的文件夹
    :param line_num: 下划线数
    :param save_type: 保存格式
    """
    # 存储分类结果
    classified_files = {}

    # 遍历目录及其子目录
    for root, _, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            if utils.is_image(file_path):
                classify_line_name = get_classify_line_name(file, line_num)
                if classify_line_name:
                    if classify_line_name not in classified_files:
                        classified_files[classify_line_name] = []
                    classified_files[classify_line_name].append(file_path)

    # 分类与保存数据
    for classify_line_name, file_paths in classified_files.items():
        classify_folder = f"{os.path.basename(dir_path)}_classify_{classify_line_name}"
        classify_path = os.path.join(dir_path, classify_folder)

        if not os.path.exists(classify_path):
            os.makedirs(classify_path)

        if save_type == 'original':
            for file_path in file_paths:
                # 获取文件的相对路径
                relative_path = os.path.relpath(file_path, dir_path)
                target_path = os.path.join(classify_path, relative_path)

                # 创建目标文件的父文件夹（如果不存在的话）
                target_dir = os.path.dirname(target_path)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)

                # 复制文件到分类文件夹中保持原结构
                shutil.copy(file_path, target_path)
        else:
            for file_path in file_paths:
                shutil.copy(file_path, classify_path)


def classify_id(dir_path, front_line, back_line):
    """
    根据ID将文件分类到测试和训练文件夹

    :param dir_path: 包含待分类文件的目录路径
    :param front_line: ID的前缀索引
    :param back_line: ID的后缀索引
    :raises FileNotFoundError: 如果目录不存在
    :raises ValueError: 如果无法读取测试或训练ID文件
    """
    # 检查目录是否存在
    if not os.path.exists(dir_path):
        raise FileNotFoundError(f"目录不存在: {dir_path}")

    # 读取测试和训练ID
    try:
        test_id = config.load_id_txt('test')
        train_id = config.load_id_txt('train')
    except (ValueError, FileNotFoundError, IOError) as e:
        raise ValueError(f"无法读取测试或训练ID文件: {str(e)}")

    front_line = int(front_line or 0)
    back_line = int(back_line or 0)

    # 遍历目录中的文件并进行分类
    for filename in os.listdir(dir_path):
        filepath = os.path.join(dir_path, filename)

        if back_line == 0:
            fileid = filename[front_line:]
        else:
            fileid = filename[front_line:-back_line]

        test_path = os.path.join(dir_path + '_test', filename)
        train_path = os.path.join(dir_path + '_train', filename)

        # 将文件移动到对应的文件夹
        try:
            if fileid in test_id:
                shutil.move(filepath, test_path)
            elif fileid in train_id:
                shutil.move(filepath, train_path)
        except Exception as e:
            print(f"无法移动文件 {filename}: {str(e)}")


if __name__ == "__main__":
    image_classify("/home/zyt/桌面/test5", 2, '按图片相似度', save_type='original')
    # image_classify_by_name("/home/zyt/桌面/test2", 1)
