# -*- coding: utf-8 -*-

"""
Project Name: data_processing
File Created: 2024.07.08
Author: ZhangYuetao
File Name: pic_dedup.py
last renew 2024.07.08
"""

import os
import shutil
from imagededup.methods.hashing import PHash


def find_images_in_folder(folder):
    """遍历文件夹及其子文件夹，找到所有图片文件"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
    image_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(os.path.join(root, file))
    return image_files


def copy_images_to_folder(image_files, destination_folder):
    """将图片文件复制到目标文件夹"""
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for image_file in image_files:
        shutil.copy(image_file, destination_folder)


def remove_duplicates(image_dir1, image_dir2, max_distance_threshold=10):
    """使用 PHash 算法移除相似的图片"""
    phasher = PHash()
    # 计算第一个图像目录中的所有图像的哈希值
    image_hashes1 = phasher.encode_images(image_dir=image_dir1, recursive=True)
    image_hashes1 = {os.path.join(image_dir1, k): v for k, v in image_hashes1.items()}

    # 计算第二个图像目录中的所有图像的哈希值（如果提供了第二个目录）
    image_hashes2 = {}
    if image_dir2:
        image_hashes2 = phasher.encode_images(image_dir=image_dir2, recursive=True)
        image_hashes2 = {os.path.join(image_dir2, k): v for k, v in image_hashes2.items()}

    # 合并两个目录的哈希值
    combined_hashes = {**image_hashes1, **image_hashes2}
    print(image_hashes1)
    print(image_hashes2)
    print(combined_hashes)

    # 查找相似图像
    duplicates = phasher.find_duplicates(encoding_map=combined_hashes, max_distance_threshold=max_distance_threshold)

    # 获取第一个目录中的所有唯一图像
    unique_images1 = set(image_hashes1.keys())
    unique_images2 = set(image_hashes2.keys())

    for key, value in duplicates.items():
        if value:  # 有相似项
            if key in unique_images1:
                for v in value:
                    if v in unique_images2 and key in unique_images1:
                        unique_images1.remove(key)
                    if v in unique_images1:
                        unique_images1.remove(v)
                
    return list(unique_images1)


def dedup(input_folder1, input_folder2, output_folder, max_distance_threshold=10):
    # 去重
    unique_images = remove_duplicates(input_folder1, input_folder2, max_distance_threshold)

    # 复制唯一图片到目标文件夹
    copy_images_to_folder([os.path.join(input_folder1, img) for img in unique_images], output_folder)


# 示例用法
input_folder1 = '/home/zyt/桌面/t11'
input_folder2 = None
output_folder = '/home/zyt/桌面/pic2'
max_distance_threshold = 10  # 设定最大距离阈值

dedup(input_folder1, input_folder2, output_folder, max_distance_threshold)

