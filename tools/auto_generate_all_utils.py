# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2023.12.30
Author: ZhangYuetao
File Name: auto_generate_all_utils.py
Update: 2025.01.02
"""

import inspect
from importlib import import_module
from datetime import datetime
import sys
import os
import glob
import re


def get_project_name(utils_files):
    """
    从 _utils.py 文件中获取项目名称。

    :param utils_files: _utils.py 文件路径列表
    :return: 项目名称
    """
    for file_path in utils_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r"Project Name: (.*)", content)
            if match:
                return match.group(1).strip()
    return os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 如果未找到，则使用项目根目录的名称


def generate_init_file(utils_dir, project_name, file_created_date):
    """
    生成 __init__.py 文件。

    :param utils_dir: utils 目录路径
    :param project_name: 项目名称
    :param file_created_date: 文件创建日期
    """
    # 获取当前日期
    today = datetime.now().strftime("%Y.%m.%d")

    # 删除旧的 __init__.py 文件（如果存在），并读取其 File Created 日期
    init_file_path = os.path.join(utils_dir, "__init__.py")
    if os.path.exists(init_file_path):
        # 读取旧文件的 File Created 日期
        with open(init_file_path, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r"File Created: (\d{4}\.\d{2}\.\d{2})", content)
            if match:
                file_created_date = match.group(1)
        # 删除旧文件
        os.remove(init_file_path)
        print("旧的 __init__.py 文件已删除！")

    # 获取 utils 目录下所有以 _utils.py 结尾的文件
    utils_files = glob.glob(os.path.join(utils_dir, "*_utils.py"))

    # 提取模块名（去掉 .py 后缀）
    modules = {os.path.basename(f)[:-3]: f"{os.path.basename(f)[:-3]} 模块中的函数" for f in utils_files}

    # 生成导入部分和 __all__ 列表
    init_content = f'''# -*- coding: utf-8 -*-
#
# Auto created by: auto_generate_all_utils.py
#
"""
Project Name: {project_name}
File Created: {file_created_date}
Author: ZhangYuetao
File Name: __init__.py
Update: {today}
"""

'''

    # 生成导入部分
    for module_name, comment in modules.items():
        module = import_module(f'utils.{module_name}')  # 使用完整路径导入模块
        # 只保留定义在当前模块中的函数
        functions = [
            name for name, obj in inspect.getmembers(module)
            if inspect.isfunction(obj) and inspect.getmodule(obj) == module
        ]
        if functions:  # 如果当前模块有函数，才生成导入部分
            init_content += f"# 导入 {comment}\n"
            init_content += f"from .{module_name} import (\n"
            for func in functions:
                init_content += f"    {func},\n"
            init_content += ")\n\n"

    # 生成 __all__ 列表
    init_content += "# 定义包的公共接口\n"
    init_content += "__all__ = [\n"
    for module_name, comment in modules.items():
        module = import_module(f'utils.{module_name}')  # 使用完整路径导入模块
        # 只保留定义在当前模块中的函数
        functions = [
            name for name, obj in inspect.getmembers(module)
            if inspect.isfunction(obj) and inspect.getmodule(obj) == module
        ]
        if functions:  # 如果当前模块有函数，才生成 __all__ 部分
            init_content += f"    # {module_name}\n"
            for func in functions:
                init_content += f"    '{func}',\n"
        init_content += "\n"
    init_content += "]\n"

    # 将生成的内容写入 __init__.py
    with open(init_file_path, "w", encoding="utf-8") as f:
        f.write(init_content)

    print("新的 __init__.py 文件已生成！")


def main():
    """
    主函数，用于命令行调用。
    """
    # 获取当前日期
    today = datetime.now().strftime("%Y.%m.%d")

    # 将项目根目录添加到 Python 路径
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(project_root)

    # 获取 utils 目录路径
    utils_dir = os.path.join(project_root, "utils")

    # 获取项目名称
    utils_files = glob.glob(os.path.join(utils_dir, "*_utils.py"))
    project_name = get_project_name(utils_files)

    # 生成 __init__.py 文件
    generate_init_file(utils_dir, project_name, today)


if __name__ == "__main__":
    main()
