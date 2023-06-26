# 导入库
import cv2
import numpy as np
import os

# 修改工作目录
os.chdir(os.path.dirname(__file__))

# 读取图片
img = cv2.imread("../test_with_img_mark.png")
# 设置高斯核的大小和标准差
kernel_size = (5, 5)
sigma = 1.5
# 使用cv2.GaussianBlur函数进行高斯滤波
blurred_img = cv2.GaussianBlur(img, kernel_size, sigma)
# 保存图片
cv2.imwrite("../blurred_img.png", blurred_img)
