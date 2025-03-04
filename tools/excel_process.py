# -*- coding: utf-8 -*-
"""
Project Name: data_processing
File Created: 2025.01.24
Author: ZhangYuetao
File Name: excel_process.py
Update: 2025.01.24
"""

import pandas as pd
import json

# 读取Excel文件
excel_file = r'C:\Users\zngzhangyuet\Desktop\id_info.xlsx'  # 替换为你的Excel文件路径
sheets_dict = pd.read_excel(excel_file, sheet_name=None)  # 读取所有Sheet

# 创建一个空字典来存储所有Sheet的数据
data_dict = {}

# 遍历每个Sheet
for sheet_name, df in sheets_dict.items():
    # 遍历当前Sheet的DataFrame
    for index, row in df.iterrows():
        employee_id = row[0]  # 第一列：工号
        if employee_id and not pd.isna(employee_id):
            employee_id = str(int(employee_id))
        birth_year = str(row[2])  # 第三列：出生年
        if birth_year == "0" or birth_year == "x":
            birth_year = "X"
        height = str(row[3])  # 第四列：身高
        if height == "0" or height == "x":
            height = "X"

        # 如果工号已经存在，跳过或覆盖（根据需求选择）
        if employee_id in data_dict:
            print(f"警告：工号 {employee_id} 在Sheet '{sheet_name}' 中重复，已覆盖之前的数据。")

        # 将数据存入字典
        data_dict[employee_id] = {'birth_year': birth_year, 'height': height}

# 将字典写入JSON文件
json_file = r'settings/id_info.json'  # 替换为你想要保存的JSON文件路径
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(data_dict, f, ensure_ascii=False, indent=4)

print(f"JSON文件已成功创建并保存到 {json_file}")
