'''
Descripttion: testing acquired blocl algorithm
version: 1.0
Author: luxin
Date: 2023-06-26 16:42:46
LastEditTime: 2024-02-29 15:21:58
'''
# testing the acquire_block2 function 
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image

'''
    1. cv2.imread(image_path)
    2. PIL.imread(image_path) 
    3. keras.preprocessing.image.imread(image_path)
    4. Skimage.io.imread(image_path)
    5. matplotlib.pyplot.imread(image_path)
    6. matplotlib.image.imread(image_path)
'''
image_path = r"C:\\Users\\luxin\\Desktop\\Dynamic Imaging\\test\\image_testing.png"
img = Image.open(image_path)
img1 = np.array(img)
print(img1.shape)

# acqurie_block embedding in the image processing fucntion 
def acquire_block(numpy_image, a, b):
    new_image = []
    center = [1223, 1023]
    print("The Width of the Image is:%d  The Height of the Image is:%d"
          % (len(numpy_image[:, 1]), len(numpy_image[0])))
    sx = int(center[0] - a / 2)
    sy = int(center[1] - b / 2)
    # check the position
    # print("The start position x:%d The start position y:%d" % (sx, sy))
    new_image = numpy_image[sx:sx + a, sy: sy + b]
    print("The Width of the new Image is:%d  The Height of the nwe Image is:%d"
          % (len(new_image[:, 1]), len(new_image[0])))
    # print(new_image)
    # erase the led 
    xy = np.where(new_image >= 255)
    new_image[xy] = 0
    print(new_image.shape)
    img2 = Image.fromarray(new_image, 'L')
    img2.show()

def acquire_block2(numpy_image, a, b):
    new_image = []
    center = [1023, 1223]
    print("The Width of the Image is:%d  The Height of the Image is:%d"
          % (len(numpy_image[:, 1]), len(numpy_image[0])))
    print(numpy_image.shape)
    sx = int(center[0] - a/2)
    sy = int(center[1] - b/2)
    print(sx, sy)
    new_image = numpy_image[sx: sx + a, sy: sy + b]
    print("The Width of the new Image is:%d  The Height of the nwe Image is:%d"
          % (len(new_image[:, 1]), len(new_image[0])))
    print(new_image.shape)
    img = Image.fromarray(new_image, 'L')
    img.show()

# acquire_block(img1, 800, 1280)
# acquire_block2(img1, 800, 1280)

# -------------2024-01-10 Code Testing -----------
import cv2
import os

# 定义输入和输出图像尺寸
desired_width = 140
desired_height = 140

# 输入文件夹路径
# input_folder = "C:/Users/luxin/Desktop/20240109/pictures/20240110"

# # 遍历输入文件夹及其子文件夹
# for dirpath, dirnames, filenames in os.walk(input_folder):
#     for filename in filenames:
#         if filename.endswith('.png'):  # 检查是否为PNG文件
#             # 构建原始文件路径
#             original_file_path = os.path.join(dirpath, filename)
            
#             # 加载图片
#             img = cv2.imread(original_file_path)

#             # 将图片调整到指定大小
#             resized_img = cv2.resize(img, (desired_width, desired_height), interpolation=cv2.INTER_AREA)

#             # 构建保存新尺寸图片的路径（保持在原目录）
#             output_file_path = os.path.join(dirpath, f"{os.path.splitext(filename)[0]}_resized.png")

#             # 保存resize后的图片
#             cv2.imwrite(output_file_path, resized_img)

# print("所有PNG图片已成功resize并存储到各自所在目录下。")


# -------------2024-01-11 Code Testing -----------
# import os
# import numpy as np
# dim1, dim2, dim3 = 10, 1280, 800
# matrix_3d_random = np.random.rand(dim1, dim2, dim3)

# file_path = "./2024-ConbinedCode/datainfo"
# if not os.path.exists(file_path):
#     os.makedirs(file_path)
#     file_path = os.path.join(file_path, 'cropped_numpy_image_list_test.npy')
#     np.save(file_path, matrix_3d_random.shape)
# else:
#     print("The file does not exist")
import os
import numpy as np

dim1, dim2, dim3 = 10, 1280, 800
matrix_3d_random = np.random.rand(dim1, dim2, dim3)

folder_path = "./2024-ConbinedCode/datainfo"  # 更改为folder_path以明确表示这是目录路径
if not os.path.exists(folder_path):  # 检查目录是否存在而非文件
    os.makedirs(folder_path)  # 如果目录不存在，创建它

file_path = os.path.join(folder_path, 'cropped_numpy_image_list_test.npy')
np.save(file_path, matrix_3d_random.shape)
