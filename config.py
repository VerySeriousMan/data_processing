# -*- coding: utf-8 -*-
"""
Project Name: Shortcut_keys
File Created: 2024.07.04
Author: ZhangYuetao
File Name: config.py
Update: 2024.10.09
"""

import os
import toml


def load_config(filepath, default):
    """
    加载配置文件，如果文件不存在或解析失败则使用默认配置
    :param filepath: TOML 文件路径
    :param default: 默认配置字典
    :return: 加载的配置字典
    """
    # 尝试读取现有的 TOML 文件
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                config = toml.load(f)
        else:
            config = default
    except (FileNotFoundError, toml.TomlDecodeError):
        config = default

    # 检查是否缺少必要的参数，如果缺少则更新为默认值
    for key, value in default.items():
        if key not in config:
            config[key] = value

    return config
