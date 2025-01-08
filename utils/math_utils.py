# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2024.12.31
Author: ZhangYuetao
File Name: math_utils.py
Update: 2025.01.02
"""
import random
import numpy as np

from collections import defaultdict

import utils.validation_utils


# 自定义距离函数
def custom_distance(x, y, distance_type="euclidean"):
    """
    计算两个点之间的距离，支持欧氏距离、汉明距离

    :param x: 点 x（一个标量或数组）
    :param y: 点 y（一个标量或数组或哈希值字符串）
    :param distance_type: 距离类型（'euclidean', 'hamming'）
    :return: 距离值
    """
    if distance_type == "euclidean":
        return np.linalg.norm(x - y)  # 欧氏距离：直线距离
    elif distance_type == "hamming":
        if utils.validation_utils.is_all_of_type(str, x, y):
            bin_x = bin(int(x, 16))[2:].zfill(64)
            bin_y = bin(int(y, 16))[2:].zfill(64)
            return sum(el1 != el2 for el1, el2 in zip(bin_x, bin_y))
        else:
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
        distances = np.array(
            [min([custom_distance(x, center, distance_type=distance_type) for center in centers]) for x in data])
        # 根据 D(x)^2 选择新的簇中心
        probabilities = distances ** 2 / np.sum(distances ** 2)

        # 使用原始数据点的索引选择新中心
        new_center_index = np.random.choice(range(len(data)), p=probabilities)
        new_center = data[new_center_index]
        centers.append(new_center)

    return centers


# 自定义优化K-means++ 聚类算法
def kmeans_plus_custom(data, k, max_iters=1000, distance_type="euclidean"):
    """
    自定义优化K-means++ 聚类算法

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
        # print(iteration)
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
                    centers = [center + 0.1 * data_std * np.random.uniform(-1, 1, size=center.shape) for center in
                               centers]
                else:  # 找到了更低的loss，更新并重置
                    might_best_loss = total_loss  # 更新might_best_loss
                    # 随机移动
                    centers = [center + 0.1 * data_std * np.random.uniform(-1, 1, size=center.shape) for center in
                               centers]
        else:
            centers = new_centers  # 更新簇中心
        previous_loss = total_loss  # 更新损失值

    return clusters, centers


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
