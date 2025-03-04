# -*- coding: utf-8 -*-
"""
Project Name: Shortcut_keys
File Created: 2024.07.04
Author: ZhangYuetao
File Name: config.py
Update: 2025.03.04
"""
import json
import os
import toml


animation_frames = [
    "[◰   ]",
    "[ ◳  ]",
    "[  ◲ ]",
    "[   ◱]",
    "[  ◲ ]",
    "[ ◳  ]",
]

TEST_ID_FILE = r'settings/testID.txt'
TRAIN_ID_FILE = r'settings/trainID.txt'

WATERMARK_ATTR_FILE = r'settings/watermark_attr.toml'
SETTING_FILE = r'settings/setting.toml'
SECRET_FILE = r'settings/.secret.toml'
SOFTWARE_INFOS_FILE = r'settings/software_infos.toml'

BATCH_IGNORE_FILE = r'settings/batch_ignore.json'
ATTRIBUTE_NAME_FILE = r'settings/attribute_name.json'
ID_INFO_FILE = r'settings/id_info.json'

ICO_FILE = r'settings/xey.ico'

SHARE_DIR = r'数据相关软件/数据处理软件'

# 定义默认参数值
SETTING_DEFAULT_CONFIG = {
    'visible': 'outside',
    'dedup_cover': 'false',
    'save_dedup_info': 'false',
    'watermark_cover': 'false',
    'space_enabled': 'false',
    'IDcard': 'true',
    'project_name': 'face_and_palm_live'
}


WATERMARK_DEFAULT_CONFIG = {
    'org': 'bottom_left, 10, 10',
    'fontFace': 'cv2.FONT_HERSHEY_SIMPLEX',
    'fontScale': '1',
    'color': '(255, 0, 0)',
    'thickness': '2',
    'lineType': 'cv2.LINE_AA',
    'alpha': '0.9',
    'num_way': 'all_nums'
}

FONT_FACE_MAP = {
        '无衬线': 'cv2.FONT_HERSHEY_SIMPLEX',
        '小号无衬线': 'cv2.FONT_HERSHEY_PLAIN',
        '复杂无衬线': 'cv2.FONT_HERSHEY_DUPLEX',
        '衬线': 'cv2.FONT_HERSHEY_COMPLEX',
        '复杂衬线': 'cv2.FONT_HERSHEY_TRIPLEX',
        '小号衬线': 'cv2.FONT_HERSHEY_COMPLEX_SMALL',
        '手写风格': 'cv2.FONT_HERSHEY_SCRIPT_SIMPLEX',
        '复杂手写风': 'cv2.FONT_HERSHEY_SCRIPT_COMPLEX',
    }

CNT_TYPE_MAP = {
    '全部计数': 'all_nums',
    '分文件夹计数': 'each_nums',
    '不计数': 'no_nums',
}

ORG_PLACE_MAP = {
    '左上方': 'top_left',
    '右上方': 'top_right',
    '左下方': 'bottom_left',
    '右下方': 'bottom_right',
    '下方正中间': 'bottom_middle',
    '上方正中间': 'top_middle',
    '右方正中间': 'right_middle',
    '左方正中间': 'left_middle',
}


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


def save_config(file_path, config_dict):
    """
    将配置字典保存到 TOML 文件中

    :param file_path: TOML 文件路径
    :param config_dict: 配置字典
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        toml.dump(config_dict, f)


def load_id_txt(file_type):
    """
    从给定的文本文件中读取ID

    :param file_type: 文本文件类型（'test' 或 'train'）
    :return: 读取的ID列表
    :raises ValueError: 如果文件类型无效
    :raises FileNotFoundError: 如果文件不存在
    :raises IOError: 如果文件读取失败
    """
    # 文件类型与路径的映射
    file_type_to_path = {
        'test': TEST_ID_FILE,
        'train': TRAIN_ID_FILE,
    }

    # 检查文件类型是否有效
    if file_type not in file_type_to_path:
        raise ValueError(f"无效的文件类型: {file_type}。支持的类型为 'test' 或 'train'。")

    # 获取文件路径
    file_path = file_type_to_path[file_type]

    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"未找到文件: {file_path}")

    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file]
    except IOError as e:
        raise IOError(f"读取文件失败: {file_path}。错误信息: {str(e)}")


def load_json(json_path):
    """
    加载 JSON 文件并返回其内容

    :param json_path: JSON 文件的路径
    :return: JSON 文件的内容（字典或列表），如果加载失败则返回 None
    """
    try:
        # 尝试打开并读取 JSON 文件
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"错误：文件未找到 - {json_path}")
    except json.JSONDecodeError:
        print(f"错误：文件格式无效（非标准 JSON） - {json_path}")
    except PermissionError:
        print(f"错误：没有权限读取文件 - {json_path}")
    except Exception as e:
        print(f"错误：加载 JSON 文件时发生未知错误 - {e}")
    return None


def load_ignore_re(project_name):
    """
    获取该项目需要忽略的正则表达式

    :param project_name: 项目名称
    :return: 需要忽略的正则表达式列表
    """
    try:
        # 尝试打开并读取文件
        with open(BATCH_IGNORE_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"文件未找到: {BATCH_IGNORE_FILE}")
        return []
    except json.JSONDecodeError:
        print(f"文件格式错误: {BATCH_IGNORE_FILE}")
        return []
    except Exception as e:
        print(f"读取文件时发生未知错误: {e}")
        return []

    # 获取项目配置并返回正则表达式列表
    project_config = data.get(project_name, {})
    return list(project_config.keys())


def load_credentials(config_path=SECRET_FILE):
    """
    从配置文件中加载服务器连接凭证。

    :param config_path: 配置文件的路径。
    :return: 包含服务器IP、共享名称、用户名和密码的元组。
    """
    with open(config_path, 'r') as config_file:
        config_info = toml.load(config_file)
        credentials = config_info.get("credentials", {})
        return (
            credentials.get("server_ip"),
            credentials.get("share_name"),
            credentials.get("username"),
            credentials.get("password"),
        )
