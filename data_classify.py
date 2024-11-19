# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2024.09.30
Author: ZhangYuetao
File Name: data_classify.py
Update: 2024.10.17
"""

import os
import shutil
import random

import imagehash
import numpy as np
from PIL import Image
from collections import defaultdict


# 自定义距离函数
def custom_distance(x, y, distance_type="euclidean"):
    """
    计算两个点之间的距离，支持欧氏距离、汉明距离
    :param x: 点 x（一个标量或数组）
    :param y: 点 y（一个标量或数组）
    :param distance_type: 距离类型（'euclidean', 'hamming'）
    :return: 距离值
    """
    if distance_type == "euclidean":
        return np.linalg.norm(x - y)  # 欧氏距离：直线距离
    elif distance_type == "hamming":
        return np.sum(x != y)  # 汉明距离：不相同的元素个数
    else:
        raise TypeError(f"未知的距离类型: {distance_type}")


def initialize_centers_kmeans_plus(data, k, distance_type):
    """
    K-means++ 初始化簇中心
    :param distance_type: 距离类型
    :param data: 要聚类的数据（一个数组或列表）
    :param k: 聚类的簇数
    :return: 初始化的簇中心
    """
    # 随机选择第一个簇中心
    centers = [random.choice(data)]

    for _ in range(1, k):
        distances = np.array([min([custom_distance(x, center, distance_type=distance_type) for center in centers]) for x in data])
        # 根据 D(x)^2 选择新的簇中心
        probabilities = distances ** 2 / np.sum(distances ** 2)

        # 使用原始数据点的索引选择新中心
        new_center_index = np.random.choice(range(len(data)), p=probabilities)
        new_center = data[new_center_index]
        centers.append(new_center)

    return centers


def kmeans_plus_custom(data, k, max_iters=1000, distance_type="euclidean"):
    """
    K-means++ 聚类算法
    :param data: 要聚类的数据（一个数组或列表）
    :param k: 聚类的簇数
    :param max_iters: 最大迭代次数
    :param distance_type: 距离度量类型（默认为欧氏距离）
    :return: 聚类后的簇和簇中心
    """
    # 使用 K-means++ 初始化簇中心
    centers = initialize_centers_kmeans_plus(data, k, distance_type)
    clusters = None
    previous_loss = float('inf')  # 初始设置为无穷大
    might_best_loss = None
    # 计算数据的全局标准差
    data_std = np.std(data, axis=0)

    for iteration in range(max_iters):
        print(iteration)
        clusters = defaultdict(list)  # 保存每个簇的成员
        new_centers = []  # 保存新的簇中心
        total_loss = 0  # 初始化当前损失

        # 分配每个数据点到最近的簇中心
        for idx, point in enumerate(data):
            distances = [custom_distance(point, center, distance_type) for center in centers]
            closest_center_idx = np.argmin(distances)  # 找到最近的簇中心
            clusters[closest_center_idx].append(idx)  # 使用原始索引
            total_loss += distances[closest_center_idx]  # 累加距离

        if distance_type == "euclidean":
            # 重新计算每个簇的新中心（平均值）
            for idx in range(k):
                if clusters[idx]:
                    new_center = np.mean([data[i] for i in clusters[idx]], axis=0)
                    new_centers.append(new_center)
                else:
                    # 如果某个簇没有分配到数据点，则随机选择一个数据点作为新中心
                    new_centers.append(data[np.random.choice(len(data))])
        else:
            # 重新计算每个簇的新中心（众数）
            for idx in range(k):
                if clusters[idx]:
                    # 获取当前簇内的所有特征
                    cluster_features = [data[i] for i in clusters[idx]]
                    # 转换为 NumPy 数组以便处理
                    cluster_array = np.array(cluster_features)

                    # 计算每一维度的众数
                    new_center = []
                    for dimension in range(cluster_array.shape[1]):
                        # 获取该维度的所有值
                        values = cluster_array[:, dimension]
                        # 计算众数
                        most_common = np.unique(values, return_counts=True)
                        new_center.append(most_common[0][np.argmax(most_common[1])])  # 取众数
                    new_centers.append(np.array(new_center))  # 将众数组成的新中心添加到列表中
                else:
                    # 如果没有数据点，则随机选择一个新中心
                    new_centers.append(data[np.random.choice(len(data))])

        # 检查损失是否发生变化，如果没有变化则停止迭代
        if total_loss == previous_loss:
            if might_best_loss is None:
                might_best_loss = total_loss
                # 随机移动当前中心
                centers = [center + 0.1 * data_std * np.random.uniform(-1, 1, size=center.shape) for center in centers]
            else:
                if total_loss == might_best_loss:
                    break
                elif total_loss > might_best_loss:
                    # 随机移动
                    centers = [center + 0.1 * data_std * np.random.uniform(-1, 1, size=center.shape) for center in centers]
                else:  # 找到了更低的loss，更新并重置
                    might_best_loss = total_loss  # 更新might_best_loss
                    # 随机移动
                    centers = [center + 0.1 * data_std * np.random.uniform(-1, 1, size=center.shape) for center in centers]
        else:
            centers = new_centers  # 更新簇中心
        previous_loss = total_loss  # 更新损失值

    return clusters, centers


# 判断文件是否为图片文件
def is_image(file_path):
    """
    判断文件是否为图片文件
    :param file_path: 文件路径
    :return: True 如果是图片文件，否则 False
    """
    try:
        with Image.open(file_path) as img:
            img.verify()  # 验证图片文件是否损坏
        return True
    except:
        return False


# 按文件创建时间分类
def get_creation_time(file_path):
    # print(file_path)
    # print(os.path.getctime(file_path))
    # print(os.path.getmtime(file_path))
    # print('-------------------------------------------')
    return os.path.getctime(file_path)


# 按文件修改时间分类
def get_modify_time(file_path):
    return os.path.getmtime(file_path)


# 按图片相似度分类，使用哈希值来代表图片的内容
def get_image_similarity(file_path):
    img = Image.open(file_path)
    hash_value = imagehash.phash(img)
    # 将哈希值转换为整数后转换为二进制字符串，并填充到64位
    binary_str = bin(int(str(hash_value), 16))[2:].zfill(64)
    return np.array([int(bit) for bit in binary_str])  # 返回64位二进制的整数数组


# 归一化函数
def normalize_data(data):
    """
    对输入数据进行Min-Max归一化处理
    :param data: 输入数据（NumPy数组）
    :return: 归一化后的数据
    """
    data_min = np.min(data, axis=0)
    data_max = np.max(data, axis=0)
    return (data - data_min) / (data_max - data_min)  # Min-Max归一化


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
            if is_image(file_path):
                if classify_by == "按创建时间":
                    feature = np.array([get_creation_time(file_path)])  # 按创建时间分类，特征为时间戳
                elif classify_by == "按修改时间":
                    feature = np.array([get_modify_time(file_path)])  # 按修改时间分类，特征为时间戳
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
    clusters, centers = kmeans_plus_custom(file_features_array, nums, distance_type=distance_type)

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
            if is_image(file_path):
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


if __name__ == "__main__":
    image_classify("/home/zyt/桌面/test5", 2, '按图片相似度', save_type='original')
    # image_classify_by_name("/home/zyt/桌面/test2", 1)
