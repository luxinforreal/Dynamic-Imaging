'''
Descripttion: Test SPI Intensity and DGI
version: 2.3.1
Author: luxin
Date: 2024-02-29 10:55:25
LastEditTime: 2024-02-29 15:20:04
'''
import os
import cv2
import glob
import numpy as np
from scipy import io
import matplotlib.pyplot as plt
from natsort import natsorted, ns

# --- DGI算法检验 ---
# handle "*.txt" file
def process_files_in_folder(folder_path) -> list:
    flat_numbers_list = []
    files = glob.glob(os.path.join(folder_path, '*.txt'))
    print(len(files))

    for file_path in files:
        with open(file_path, 'r') as file:
            lines_list = file.readlines()

        numbers_list = [[float(value) for value in line.strip().split(',')] for line in lines_list]
        flat_numbers_list.extend([num for sublist in numbers_list for num in sublist])
    
    return flat_numbers_list

# load Speckle Pattern
def load_images_as_array(directory: str, size: int) -> np.ndarray:
    """
    加载指定目录下前size个.png格式的图片,并将它们转换为灰度图像后存储在numpy数组中.

    :param directory: 图片所在的目录路径.
    :param size: 要加载的图片数量.
    :return: 一个形状为(size, height, width)的numpy数组,其中height和width是图片的高和宽.
    """
    os.chdir(directory)
    filelist = [f for f in os.listdir(directory) if f.endswith('.png')]
    filelist = natsorted(filelist)
    filelist = filelist[:size]

    # 读取图像
    img_data = []
    for i in range(size):
        img = cv2.imread(filelist[i], cv2.IMREAD_GRAYSCALE)
        img_data.append(img)
    img_data = np.asarray(img_data)
    
    # 反转图像
    flipped_image = []
    for i in range(size):
        img_data[i] = np.flip(img_data[i], axis=1)
        flipped_image.append(img_data[i])

    # 将二维图像数组展平为一维数组列表
    arr = [img.flatten() for img in img_data]
    arr = np.asarray(arr)

    return img_data

# DGI Algorith
def DGI(data: list, img_data: np.ndarray, size: int) -> None:
    data = flat_numbers_list
    bucket = data
    ghost = np.zeros((800, 1280))
    bucket_sum = 0
    sum_field = ghost + 0.00001
    corr_sum = ghost
    number_sum = 0
    ghost_sum = ghost
    number_sum = 0
    plt.ion()
        
    for i in range(np.size(data)):
        image = img_data[i]
        img = image.astype('float64')
        sum_field = sum_field + img
        number = np.sum(img)
        number_sum = number + number_sum
        mean_number = number_sum/(i + 1) 
    
        print(i)

        # Differential GI
        mean_field = sum_field/(i + 1)
        bucketDebug = bucket[i]
        # bucketDebug = bucketDebug[0]
        bucket_sum = bucket_sum+bucketDebug
        mean_bucket = bucket_sum/(i + 1)
        ghost_sum =ghost_sum + (((img/mean_field) - 1)*(bucketDebug - (mean_bucket*number/mean_number)))
        # isnan = np.isnan(ghost_sum)
        # print(True in isnan)
    
        ghost_final = ghost_sum/(i + 1)

        if i == size:
            break
    plt.imshow(ghost_final)
    
# --- main ---
def main():
    directory = "D:/Speckle pattern/030bmp/030bmp/"
    size = 1500
    
    img_data = load_images_as_array(directory, size)
    flat_numbers_list = process_files_in_folder(directory)
    
    if len(flat_numbers_list) == size:
        DGI(flat_numbers_list, img_data, size)
    else:
        print ("Unmatched number of images !!!")
        
if __name__ == "__main__":
    main()
