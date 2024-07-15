# -*- coding: utf-8 -*-

"""
Project Name: data_processing
File Created: 2024.07.08
Author: ZhangYuetao
File Name: pic_dedup.py
last renew 2024.07.12
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


def copy_images_to_folder(image_files, source_folder, destination_folder):
    """将图片文件复制到目标文件夹，保留原文件夹结构"""
    for image_file in image_files:
        # 获取相对于源文件夹的相对路径
        relative_path = os.path.relpath(image_file, source_folder)
        # 构建目标文件夹中的完整路径
        destination_path = os.path.join(destination_folder, relative_path)
        # 确保目标路径的文件夹存在
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        # 复制文件到目标路径
        shutil.copy(image_file, destination_path)


def remove_duplicates(image_dir1, image_dir2, max_distance_threshold, dedup_cover='false'):
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

    # 查找相似图像
    duplicates = phasher.find_duplicates(encoding_map=combined_hashes, max_distance_threshold=max_distance_threshold)

    # 获取第一个目录中的所有唯一图像
    unique_images1 = set(image_hashes1.keys())
    unique_images2 = set(image_hashes2.keys())

    if dedup_cover == 'false':
        for key, value in duplicates.items():
            if value:  # 有相似项
                if key in unique_images1:
                    for v in value:
                        if v in unique_images2 and key in unique_images1:
                            unique_images1.remove(key)
                        if v in unique_images1:
                            unique_images1.remove(v)
    else:
        for key, value in duplicates.items():
            if value:  # 有相似项
                if key in unique_images1:
                    for v in value:
                        if v in unique_images2 and key in unique_images1:
                            unique_images1.remove(key)
                            os.remove(key)
                        if v in unique_images1:
                            unique_images1.remove(v)
                            os.remove(v)
                
    return list(unique_images1)


def custom_round(x):
    return int(x + 0.5) if x > 0 else int(x - 0.5)


def dedup(input_folder1, input_folder2, output_folder, similar_percent, dedup_cover='false'):
    max_distance_threshold = custom_round(64 - 0.64 * similar_percent)
    # 去重
    unique_images = remove_duplicates(input_folder1, input_folder2, max_distance_threshold, dedup_cover)

    if dedup_cover == 'false':
        # 复制唯一图片到目标文件夹，保留原文件夹结构
        copy_images_to_folder(unique_images, input_folder1, output_folder)
