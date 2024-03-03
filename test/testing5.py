'''
Descripttion: 根据查找要求筛选文件到指定文件夹
version: 3.0
Author: luxin
Date: 2024-03-03 11:02:55
LastEditTime: 2024-03-03 21:17:26
'''

import os
import shutil
from collections import defaultdict

def count_matching_files(source_dir, target_strings):
    matching_file_count = 0
    
    for root, _, files in os.walk(source_dir):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                file_name_without_extension = os.path.splitext(file_name)[0]
                if all(target_string in file_name_without_extension for target_string in target_strings):
                    matching_file_count += 1
    
    print(f"Number of files matching all target strings: {matching_file_count}")

def find_and_copy_files(source_dir, destination_dir, target_strings):
    
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    # dictionary - store filenames, filepath 
    file_dict = defaultdict(list)
    
    # iterate all files
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                file_name = os.path.splitext(file)[0]
                if all(target_string in file_name for target_string in target_strings):
                    if file_name in file_dict:
                        print(f"Removing duplicate file: {file_name}")
                        for path in file_dict[file_name]:
                            print(f"Removing: {path}")
                            os.remove(path)
                        file_dict[file_name].clear()
                    file_dict[file_name].append(file_path)
    
    for file_paths in file_dict.values():
        for file_path in file_paths:
            shutil.copy(file_path, destination_dir)

def main():
    src_folder = 'C:\\Users\\luxin\\Desktop\\src'
    dst_folder = 'C:\\Users\\luxin\\Desktop\\dst'
    target_strings = ['uw']
    
    if os.path.exists(src_folder):
        print(f"The path {src_folder} exists")
        count_matching_files(src_folder, target_strings)
    else:
        raise FileNotFoundError(f"The path {src_folder} does not exist.")
    
    find_and_copy_files(src_folder, dst_folder, target_strings)
    
if __name__ == '__main__':
    main()