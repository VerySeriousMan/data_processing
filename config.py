# -*- coding: utf-8 -*-
"""
Project Name: Shortcut_keys
File Created: 2024.07.04
Author: ZhangYuetao
File Name: config.py
last renew 2024.07.04
"""

import os
import toml

# 定义默认参数值
DEFAULT_CONFIG = {
    'visible': 'outside',
    'space_enabled': 'false',
    'xjd': 'true'
}

CONFIG_FILE = r'settings/setting.toml'


def load_config():
    # 尝试读取现有的 TOML 文件
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = toml.load(f)
        else:
            config = DEFAULT_CONFIG
    except (FileNotFoundError, toml.TomlDecodeError):
        config = DEFAULT_CONFIG

    # 检查是否缺少必要的参数，如果缺少则更新为默认值
    for key, value in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = value

    return config


def save_config(config):
    # 将更新后的配置写入 TOML 文件
    with open(CONFIG_FILE, 'w') as f:
        toml.dump(config, f)
