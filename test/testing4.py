'''
Descripttion: 转换图片格式 *.png -> *.bmp
version: 1.0
Author: luxin
Date: 2024-02-29 16:48:34
LastEditTime: 2024-02-29 17:33:54
description:
    convert_png_to_bmp_old(source_dir: str, target_dir: str):需要手动修改路径
    convert_png_to_bmp(source_dir: str, target_dir: str):参数拼接
'''

import cv2
import os

# single convert 
def convert_png_to_bmp(source_dir: str, target_dir: str):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for root, dirs, files in os.walk(source_dir):
        for file_name in files:
            if file_name.endswith(".png"):
                png_file_path = os.path.join(root, file_name)
                
                base_name = os.path.splitext(file_name)[0]
                bmp_file_path = os.path.join(target_dir, base_name + ".bmp")
                img = cv2.imread(png_file_path, cv2.IMREAD_UNCHANGED)

                if img is not None:
                    cv2.imwrite(bmp_file_path, img)
                    print(f"成功将 {png_file_path} 转换为 {bmp_file_path}")
                else:
                    print(f"未能读取 {png_file_path}")
source_path = "D:\\speckle pattern\\064"
target_path = "D:\\speckle pattern\\bmp\\064"
convert_png_to_bmp(source_path, target_path)

# update convert 
# def convert_png_to_bmp(base_source_dir: str, additional_source_path: str, base_target_dir: str, additional_target_path: str):
#     source_dir = os.path.join(base_source_dir, additional_source_path)
#     target_dir = os.path.join(base_target_dir, additional_target_path)

#     if not os.path.exists(target_dir):
#         os.makedirs(target_dir)

#     for root, dirs, files in os.walk(source_dir):
#         for file_name in files:
#             if file_name.endswith(".png"):
#                 png_file_path = os.path.join(root, file_name)
#                 base_name = os.path.splitext(file_name)[0]
#                 bmp_file_path = os.path.join(target_dir, base_name + ".bmp")
#                 img = cv2.imread(png_file_path, cv2.IMREAD_UNCHANGED)
#                 if img is not None:
#                     cv2.imwrite(bmp_file_path, img)
#                     print(f"成功将 {png_file_path} 转换为 {bmp_file_path}")
#                 else:
#                     print(f"未能读取 {png_file_path}")

    
