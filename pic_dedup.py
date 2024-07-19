# -*- coding: utf-8 -*-

"""
Project Name: data_processing
File Created: 2024.07.08
Author: ZhangYuetao
File Name: pic_dedup.py
last renew 2024.07.19
"""

import os
import shutil
from PIL import Image
import imagehash


class PHash:
    def find_duplicates(self, encoding_map, max_distance_threshold):
        duplicates = {}
        hashes = list(encoding_map.values())
        keys = list(encoding_map.keys())

        for i in range(len(hashes)):
            for j in range(i + 1, len(hashes)):
                # 计算汉明距离
                distance = self.hamming_distance(hashes[i], hashes[j])
                if distance <= max_distance_threshold:
                    if keys[i] not in duplicates:
                        duplicates[keys[i]] = []
                    duplicates[keys[i]].append(keys[j])

        return duplicates

    @staticmethod
    def hamming_distance(hash1, hash2):
        """计算汉明距离"""
        # 转换为64位二进制字符串
        bin1 = bin(int(hash1, 16))[2:].zfill(64)
        bin2 = bin(int(hash2, 16))[2:].zfill(64)

        return sum(el1 != el2 for el1, el2 in zip(bin1, bin2))


def calculate_phash_for_images(directory):
    phash_dict = {}
    error_list = []

    # 遍历文件夹及子文件夹
    for root, _, files in os.walk(directory):
        for file_name in files:
            # 过滤图像文件
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_path = os.path.join(root, file_name)
                try:
                    # 打开图像并计算 PHash
                    image = Image.open(image_path)
                    phash_value = imagehash.phash(image)
                    # 将结果添加到字典
                    phash_dict[image_path] = str(phash_value)
                except Exception as e:
                    error_list.append(f"无法处理图像 {image_path}: {e}")  # 添加错误信息到列表

    return phash_dict, error_list


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
    phasher = PHash()
    """使用 PHash 算法移除相似的图片"""
    # 计算第一个图像目录中的所有图像的哈希值
    image_hashes1, errors1 = calculate_phash_for_images(image_dir1)

    # 计算第二个图像目录中的所有图像的哈希值（如果提供了第二个目录）
    image_hashes2 = {}
    errors2 = []
    if image_dir2:
        image_hashes2, errors2 = calculate_phash_for_images(image_dir2)

    # 合并两个目录的哈希值
    combined_hashes = {**image_hashes1, **image_hashes2}

    # 查找相似图像
    duplicates = phasher.find_duplicates(encoding_map=combined_hashes, max_distance_threshold=max_distance_threshold)

    # 获取第一个目录中的所有唯一图像
    unique_images1 = set(image_hashes1.keys())
    unique_images2 = set(image_hashes2.keys())

    deleted_images = []

    if dedup_cover == 'false':
        for key, value in duplicates.items():
            if value:  # 有相似项
                if key in unique_images1:
                    for v in value:
                        if v in unique_images2 and key in unique_images1:
                            deleted_images.append(key)
                            unique_images1.remove(key)
                        if v in unique_images1:
                            deleted_images.append(v)
                            unique_images1.remove(v)
    else:
        for key, value in duplicates.items():
            if value:  # 有相似项
                if key in unique_images1:
                    for v in value:
                        if v in unique_images2 and key in unique_images1:
                            deleted_images.append(key)
                            unique_images1.remove(key)
                            os.remove(key)
                        if v in unique_images1:
                            deleted_images.append(v)
                            unique_images1.remove(v)
                            os.remove(v)

    return list(unique_images1), deleted_images, errors1 + errors2


def custom_round(x):
    return int(x + 0.5) if x > 0 else int(x - 0.5)


def save_delete_images_txt(deleted_images, output_folder):
    txt_path = output_folder + 'deleted_images_path.txt'
    with open(txt_path, 'w', encoding='utf-8') as txt:
        for file in deleted_images:
            txt.write(file + '\n')


def dedup(input_folder1, input_folder2, output_folder, similar_percent, dedup_cover='false'):
    max_distance_threshold = custom_round(64 - 0.64 * similar_percent)
    # 去重
    unique_images, deleted_images, error_list = remove_duplicates(input_folder1, input_folder2, max_distance_threshold, dedup_cover)

    if dedup_cover == 'false':
        # 复制唯一图片到目标文件夹，保留原文件夹结构
        copy_images_to_folder(unique_images, input_folder1, output_folder)

    save_delete_images_txt(deleted_images, output_folder)

    return error_list
