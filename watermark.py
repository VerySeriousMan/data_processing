# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2024.09.27
Author: ZhangYuetao
File Name: watermark.py
last renew: 2024.09.29
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
    for f_filename in os.listdir(filepath):
        path = os.path.join(filepath, f_filename)
        if not os.path.isdir(path):
            continue
        mark_text = f_filename

        if num_way == 'each_nums':
            add_num = 0

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

                img_with_watermark = cv2.addWeighted(overlay, alpha, img, 1, 0)

                # 保存结果
                success = cv2.imwrite(p_path, img_with_watermark)
                if not success:
                    print(f"保存失败: {p_path}")

                if num_way != 'no_nums':
                    add_num += 1  # 仅在需要时递增


if __name__ == "__main__":
    add_watermark('/home/zyt/桌面/t1', 'test')
