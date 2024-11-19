# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2024.09.27
Author: ZhangYuetao
File Name: watermark.py
Update: 2024.10.09
"""

import os
import numpy as np

import cv2

import config

DEFAULT_CONFIG = {
    'org': 'bottom_left, 10, 10',
    'fontFace': 'cv2.FONT_HERSHEY_SIMPLEX',
    'fontScale': '1',
    'color': '(255, 0, 0)',
    'thickness': '2',
    'lineType': 'cv2.LINE_AA',
    'alpha': '0.9',
    'num_way': 'all_nums'
}


def get_position(org, offset_x, offset_y, width, height):
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
    else:
        # 默认返回左下角
        return offset_x, height - offset_y


def add_watermark(filepath, extra_text):
    """
    在指定文件夹中的图像上添加水印
    :param filepath: 包含图像的文件夹路径
    :param extra_text: 附加的水印文本
    """
    # 加载水印配置
    txt_config = config.load_config(r'settings/watermark_attr.toml', DEFAULT_CONFIG)

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

                height, width = img.shape[:2]

                # 创建与原图相同大小的透明图层
                overlay = np.zeros_like(img, dtype=np.uint8)

                # 获取水印位置
                org = get_position(position_type, offset_x, offset_y, width, height)

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

                # 在透明图层上添加文本
                cv2.putText(overlay, text=text, org=org, fontFace=fontFace,
                            fontScale=fontScale, color=color, thickness=thickness, lineType=lineType)

                # 将水印合并到原图
                img_with_watermark = cv2.addWeighted(overlay, alpha, img, 1, 0)

                # 保存结果
                success = cv2.imwrite(p_path, img_with_watermark)
                if not success:
                    print(f"保存失败: {p_path}")

                if num_way != 'no_nums':
                    add_num += 1  # 仅在需要时递增


if __name__ == "__main__":
    add_watermark('/home/zyt/桌面/t1', 'test')
