'''
Descripttion: 根据查找要求筛选文件到指定文件夹
version: 2.0
Author: luxin
Date: 2024-03-03 11:02:55
LastEditTime: 2024-03-03 11:45:51
'''

import os
import shutil

import os
import shutil
from collections import defaultdict

def move_files_with_specific_strings(src_folder, dst_folder, specific_strings, temp_folder=None):
    """
    将源文件夹中包含任何特定字符串的.npy文件复制并移动到目标文件夹,处理目标文件夹中可能存在的同名文件。

    参数：
    src_folder (str): 源文件夹路径
    dst_folder (str): 目标文件夹路径
    specific_strings (list[str]): 特定字符串列表
    temp_folder (str, optional): 临时文件夹路径,如果不提供则在内存中创建临时文件,默认为None
    
    返回值：
    dict: 键为原目标文件名，值为重命名后的目标文件路径字典
    """
    if temp_folder is None:
        temp_folder = os.path.join(os.getcwd(), '_temp')
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    renamed_files = defaultdict(int)

    # 遍历源文件夹中的所有文件
    for filename in os.listdir(src_folder):
        if filename.endswith('.txt'):
            if any(string in filename for string in specific_strings):
                src_file = os.path.join(src_folder, filename)
                temp_file = os.path.join(temp_folder, filename)

                shutil.copy(src_file, temp_file)
                
                base_name, ext = os.path.splitext(filename)
                while os.path.exists(os.path.join(dst_folder, filename)):
                    renamed_files[base_name] += 1
                    filename = f"{base_name}_{renamed_files[base_name]}{ext}"

                dst_file = os.path.join(dst_folder, filename)

                shutil.move(temp_file, dst_file)
                print(f"Copied and moved file {os.path.basename(temp_file)} to {os.path.basename(dst_file)}")

    # 清理临时文件夹（如果不需要保留临时文件）
    # for file in os.listdir(temp_folder):
    #     os.remove(os.path.join(temp_folder, file))
    # os.rmdir(temp_folder)

    return dict(renamed_files)


def main():
    src_folder = "C:\Users\luxin\Desktop\src"
    dst_folder = "C:\Users\luxin\Desktop\dst"
    string_dist = ['wp1', 'r200', 'uw']
    renamed_files_dict = move_files_with_specific_strings(src_folder, dst_folder, string_dist)
    for original_name, new_name in renamed_files_dict.items():
        print(f"Original name: {original_name}, Renamed to: {new_name}")

if __name__ == '__main__':
    main()