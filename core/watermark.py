# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2024.09.27
Author: ZhangYuetao
File Name: watermark.py
Update: 2025.01.08
"""

import os
import numpy as np

import cv2

import config


def get_mark_position(org, offset_x, offset_y, width, height):
    """
    根据给定的位置参数计算水印位置

    :param org: 水印位置的类型
    :param offset_x: 水印相对于图像边缘的x偏移量
    :param offset_y: 水印相对于图像边缘的y偏移量
    :param width: 图像宽度
    :param height: 图像高度
    :return: 水印的坐标
    """
    if org == "top_left":
        return offset_x, offset_y
    elif org == "top_right":
        return width - offset_x, offset_y
    elif org == "bottom_left":
        return offset_x, height - offset_y
    elif org == "bottom_right":
        return width - offset_x, height - offset_y
    elif org == "bottom_middle":
        return width//2, height - offset_y
    elif org == "top_middle":
        return width//2, offset_y
    elif org == "right_middle":
        return width - offset_x, height//2
    elif org == "left_middle":
        return offset_x, height//2
    else:
        # 默认返回左下角
        return offset_x, height - offset_y


def add_watermark_to_image(img, text, position_type, offset_x, offset_y, fontFace, fontScale, color, thickness, lineType, alpha):
    """
    在单张图像上添加水印

    :param img: 输入图像
    :param text: 水印文本
    :param position_type: 水印位置类型
    :param offset_x: x偏移量
    :param offset_y: y偏移量
    :param fontFace: 字体类型
    :param fontScale: 字体大小
    :param color: 字体颜色
    :param thickness: 字体粗细
    :param lineType: 线条类型
    :param alpha: 水印不透明度
    :return: 添加水印后的图像
    """
    height, width = img.shape[:2]

    # 创建与原图相同大小的透明图层
    overlay = np.zeros_like(img, dtype=np.uint8)

    # 获取水印位置
    org = get_mark_position(position_type, offset_x, offset_y, width, height)

    # 在透明图层上添加文本
    cv2.putText(overlay, text=text, org=org, fontFace=fontFace,
                fontScale=fontScale, color=color, thickness=thickness, lineType=lineType)

    # 将水印合并到原图
    return cv2.addWeighted(overlay, alpha, img, 1, 0)


def add_watermark(filepath, extra_text, save_path):
    """
    在指定文件夹中的图像上添加水印

    :param filepath: 包含图像的文件夹路径
    :param extra_text: 附加的水印文本
    :param save_path: 保存地址
    """
    # 加载水印配置
    txt_config = config.load_config(config.WATERMARK_ATTR_FILE, config.WATERMARK_DEFAULT_CONFIG)

    org_str = txt_config['org']
    position_parts = org_str.split(',')
    position_type = position_parts[0].strip()
    offset_x = int(position_parts[1].strip())
    offset_y = int(position_parts[2].strip())

    fontFace = eval(txt_config['fontFace'])
    fontScale = float(txt_config['fontScale'])
    color = tuple(map(int, txt_config['color'].strip('()').split(',')))
    thickness = int(txt_config['thickness'])
    lineType = eval(txt_config['lineType'])
    alpha = float(txt_config['alpha'])  # 水印不透明度
    num_way = str(txt_config['num_way'])

    add_num = 0
    # 遍历每个子文件夹
    for first_dir in os.listdir(filepath):
        path = os.path.join(filepath, first_dir)
        if not os.path.isdir(path):
            continue
        mark_text = first_dir

        if num_way == 'each_nums':
            add_num = 0

        # 遍历每个图像文件
        for root, _, files in os.walk(path):
            for file in files:
                p_path = os.path.join(root, file)
                img = cv2.imread(p_path)
                if img is None:
                    print(f"无法读取图像: {p_path}")
                    continue

                # 生成水印文本
                if num_way == 'no_nums':
                    if extra_text:
                        text = f"{mark_text}_{extra_text}"
                    else:
                        text = f"{mark_text}"
                else:
                    if extra_text:
                        text = f"{mark_text}_{extra_text}_{add_num}"
                    else:
                        text = f"{mark_text}_{add_num}"

                # 将水印合并到原图
                img_with_watermark = add_watermark_to_image(img, text, position_type, offset_x, offset_y,
                                                            fontFace, fontScale, color, thickness, lineType, alpha)

                # 保存结果
                if save_path == '':
                    success = cv2.imwrite(p_path, img_with_watermark)

                    if not success:
                        print(f"保存失败: {p_path}")
                else:
                    base_p_path = os.path.relpath(root, filepath)
                    save_p_path = os.path.join(save_path, base_p_path, file)
                    os.makedirs(os.path.dirname(save_p_path), exist_ok=True)
                    success = cv2.imwrite(save_p_path, img_with_watermark)
                    if not success:
                        print(f"保存失败: {save_p_path}")

                if num_way != 'no_nums':
                    add_num += 1  # 仅在需要时递增


if __name__ == "__main__":
    add_watermark(r'C:\Users\zngzhangyuet\Desktop\123n\1063635\IRLeft', 'test', '')
