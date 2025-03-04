# -*- coding: utf-8 -*-
#
# Auto created by: auto_generate_init.py
#
"""
Project Name: data_processing
File Created: 2025.01.03
Author: ZhangYuetao
File Name: __init__.py
Update: 2025.01.24
"""

# 导入 file_utils 模块中的函数
from .file_utils import (
    change_IDcard,
    change_current_dir_id,
    change_files,
    change_settings,
    create_dir_name,
    move_folder_contents,
    remove_patterns,
)

# 导入 math_utils 模块中的函数
from .math_utils import (
    custom_distance,
    initialize_centers_kmeans_plus,
    kmeans_plus_custom,
    normalize_data,
)

# 导入 text_utils 模块中的函数
from .text_utils import (
    create_txt,
    save_line_to_txt,
)

# 导入 validation_utils 模块中的函数
from .validation_utils import (
    get_current_software_path,
    is_all_of_type,
    is_file_complete,
    is_have_chinese,
    is_image,
)

# 定义包的公共接口
__all__ = [
    # file_utils
    'change_IDcard',
    'change_current_dir_id',
    'change_files',
    'change_settings',
    'create_dir_name',
    'move_folder_contents',
    'remove_patterns',

    # math_utils
    'custom_distance',
    'initialize_centers_kmeans_plus',
    'kmeans_plus_custom',
    'normalize_data',

    # text_utils
    'create_txt',
    'save_line_to_txt',

    # validation_utils
    'get_current_software_path',
    'is_all_of_type',
    'is_file_complete',
    'is_have_chinese',
    'is_image',

]
