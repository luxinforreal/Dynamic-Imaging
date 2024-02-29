'''
Descripttion: 快速检测文件夹中的光强数据是否为1500次采集
version: 1.0.0
Author: luxin
Date: 2024-02-29 10:55:25
LastEditTime: 2024-02-29 16:40:22
'''
import os
import glob

# --- DGI算法检验 ---
# handle "*.txt" file
def check_line_count_in_txts(folder_path) -> None:
    non_conforming_files = []

    # 获取指定文件夹下所有.txt文件的完整路径
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))

    for file_path in txt_files:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) != 1500:
                print(f"文件 {file_path} 不包含1500行数据,实际行数为 {len(lines)}。")
                non_conforming_files.append(file_path)

    if not non_conforming_files:
        print("所有.txt文件均包含1500行数据。")
    
# --- main ---
def main():
    folder_path = 'your_folder_path'  # 替换为你要检测的文件夹路径
    check_line_count_in_txts(folder_path)
          
if __name__ == "__main__":
    main()
