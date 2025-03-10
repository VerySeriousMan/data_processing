# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2024.07.08
Author: ZhangYuetao
File Name: dedup.py
Update: 2025.03.04
"""
import hashlib
import os
import shutil

from PIL import Image
import imagehash
import zyt_validation_utils

import utils


def find_duplicates(encoding_map, max_distance_threshold):
    """
    查找重复的图像

    :param encoding_map: 图像的哈希值映射
    :param max_distance_threshold: 最大允许的汉明距离
    :return: 重复图像的字典
    """
    duplicates = {}
    hashes = list(encoding_map.values())
    keys = list(encoding_map.keys())

    for i in range(len(hashes)):
        for j in range(i + 1, len(hashes)):
            # 汉明距离
            distance = utils.custom_distance(hashes[i], hashes[j], 'hamming')
            if distance <= max_distance_threshold:
                if keys[i] not in duplicates:
                    duplicates[keys[i]] = []
                duplicates[keys[i]].append(keys[j])

    return duplicates


def calculate_phash_for_images(directory):
    """
    计算指定目录下所有图像的感知哈希值

    :param directory: 要处理的图像目录
    :return: 包含图像路径和其对应哈希值的字典，以及错误列表
    """
    phash_dict = {}
    error_list = []

    # 遍历文件夹及子文件夹
    for root, _, files in os.walk(directory):
        for file_name in files:
            if zyt_validation_utils.is_image(file_name, 'fast', raise_error=False):
                image_path = os.path.join(root, file_name)
                try:
                    image = Image.open(image_path)
                    phash_value = imagehash.phash(image)
                    phash_dict[image_path] = str(phash_value)
                except Exception as e:
                    error_list.append(f"无法处理图像 {image_path}: {e}")

    return phash_dict, error_list


def calculate_md5_for_images(directory, chunk_size=8192):
    """
    计算指定目录下所有图像文件的 MD5 哈希值

    :param directory: 要处理的图像目录
    :param chunk_size: 分块读取文件时的块大小（字节），默认为 8192
    :return: 包含图像路径和其对应 MD5 哈希值的字典，以及错误列表
    """
    md5_dict = {}
    error_list = []

    # 遍历文件夹及子文件夹
    for root, _, files in os.walk(directory):
        for file_name in files:
            if zyt_validation_utils.is_image(file_name, 'fast', raise_error=False):
                image_path = os.path.join(root, file_name)
                try:
                    md5 = hashlib.md5()
                    with open(image_path, "rb") as f:
                        # 分块读取文件内容（避免大文件内存溢出）
                        while chunk := f.read(chunk_size):
                            md5.update(chunk)
                    md5_hash = md5.hexdigest()
                    md5_dict[image_path] = md5_hash
                except Exception as e:
                    error_list.append(f"无法计算文件 {image_path} 的 MD5: {str(e)}")

    return md5_dict, error_list


def copy_images_to_folder(image_files, source_folder, destination_folder):
    """
    将图片文件复制到目标文件夹，保留原文件夹结构

    :param image_files: 要复制的图像文件列表
    :param source_folder: 源文件夹路径
    :param destination_folder: 目标文件夹路径
    """
    for image_file in image_files:
        relative_path = os.path.relpath(image_file, source_folder)
        destination_path = os.path.join(destination_folder, relative_path)
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        shutil.copy(image_file, destination_path)


def remove_duplicates(image_dir1, image_dir2, max_distance_threshold, dedup_cover='false'):
    """
    使用 PHash 算法移除相似的图片

    :param image_dir1: 第一个图像目录
    :param image_dir2: 第二个图像目录（可选）
    :param max_distance_threshold: 最大允许的汉明距离
    :param dedup_cover: 是否覆盖删除相似图像
    :return: 唯一图像列表、删除图像列表和错误列表
    """
    if max_distance_threshold == 0:
        image_hashes1, errors1 = calculate_md5_for_images(image_dir1)
    else:
        image_hashes1, errors1 = calculate_phash_for_images(image_dir1)

    image_hashes2 = {}
    errors2 = []
    if image_dir2:
        if max_distance_threshold == 0:
            image_hashes2, errors2 = calculate_md5_for_images(image_dir2)
        else:
            image_hashes2, errors2 = calculate_phash_for_images(image_dir2)

    combined_hashes = {**image_hashes1, **image_hashes2}
    duplicates = find_duplicates(combined_hashes, max_distance_threshold)

    unique_images1 = set(image_hashes1.keys())
    unique_images2 = set(image_hashes2.keys())
    deleted_images = []

    if dedup_cover == 'false':
        for key, value in duplicates.items():
            if value:
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
            if value:
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


def save_delete_images_txt(deleted_images, output_folder):
    """
    将删除的图像路径保存到文本文件

    :param deleted_images: 被删除的图像路径列表
    :param output_folder: 输出文件夹路径
    """
    if not zyt_validation_utils.is_empty(deleted_images):
        txt_path = os.path.join(output_folder, 'deleted_images_path.txt')
        with open(txt_path, 'a', encoding='utf-8') as txt:
            for file in deleted_images:
                txt.write(file + '\n')


def dedup(input_folder1, input_folder2, output_folder, similar_percent,
          dedup_cover='false', save_dedup_info='false', every_folder=False):
    """
    去重处理

    :param input_folder1: 第一个输入文件夹路径
    :param input_folder2: 第二个输入文件夹路径（可选）
    :param output_folder: 输出文件夹路径
    :param similar_percent: 相似度百分比
    :param dedup_cover: 是否覆盖删除相似图像
    :param save_dedup_info: 是否保存去重信息txt
    :param every_folder: 是否各子文件夹独立
    :return: 错误列表
    """

    def _custom_round(x):
        """自定义四舍五入函数"""
        return int(x + 0.5) if x > 0 else int(x - 0.5)

    max_distance_threshold = _custom_round(64 - 0.64 * similar_percent)

    error_lists = []

    if not every_folder:
        unique_images, deleted_images, error_lists = remove_duplicates(input_folder1, input_folder2, max_distance_threshold, dedup_cover)

        if dedup_cover == 'false':
            copy_images_to_folder(unique_images, input_folder1, output_folder)

        if save_dedup_info != 'false':
            save_delete_images_txt(deleted_images, output_folder)

    else:
        for root, dirs, _ in os.walk(input_folder1):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)

                if not zyt_validation_utils.dir_check.is_have_subdirectories(dir_path):
                    unique_images, deleted_images, error_list = remove_duplicates(dir_path, input_folder2, max_distance_threshold, dedup_cover)

                    if dedup_cover == 'false':
                        output_dir = os.path.join(output_folder, os.path.relpath(dir_path, input_folder1))
                        copy_images_to_folder(unique_images, dir_path, output_dir)

                    if save_dedup_info != 'false':
                        save_delete_images_txt(deleted_images, output_folder)

                    error_lists.extend(error_list)

    return error_lists
