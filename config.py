# -*- coding: utf-8 -*-
"""
Project Name: Shortcut_keys
File Created: 2024.07.04
Author: ZhangYuetao
File Name: config.py
last renew 2024.09.27
"""

import os
import toml


def load_config(filepath, default):
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
