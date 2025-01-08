# -*- coding: utf-8 -*-
#
# Auto created by: auto_generate_init.py
#
"""
Project Name: data_processing
File Created: 2025.01.03
Author: ZhangYuetao
File Name: __init__.py
Update: 2025.01.08
"""

# 导入 data_check 模块中的函数
from .data_check import (
    get_batch_files,
    get_wrong_paths_txt,
    is_wrong_filename,
)

# 导入 dedup 模块中的函数
from .dedup import (
    calculate_phash_for_images,
    copy_images_to_folder,
    dedup,
    find_duplicates,
    remove_duplicates,
    save_delete_images_txt,
)

# 导入 pre_classify 模块中的函数
from .pre_classify import (
    classify_id,
    get_classify_line_name,
    get_image_similarity,
    image_classify,
    image_classify_by_name,
)

# 导入 watermark 模块中的函数
from .watermark import (
    add_watermark,
    add_watermark_to_image,
    get_mark_position,
)

# 定义包的公共接口
__all__ = [
    # data_check
    'get_batch_files',
    'get_wrong_paths_txt',
    'is_wrong_filename',

    # dedup
    'calculate_phash_for_images',
    'copy_images_to_folder',
    'dedup',
    'find_duplicates',
    'remove_duplicates',
    'save_delete_images_txt',

    # pre_classify
    'classify_id',
    'get_classify_line_name',
    'get_image_similarity',
    'image_classify',
    'image_classify_by_name',

    # watermark
    'add_watermark',
    'add_watermark_to_image',
    'get_mark_position',

]
