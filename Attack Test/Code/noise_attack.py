## 高斯噪声

# 导入库
import cv2
import numpy as np
import os

# 修改工作目录
os.chdir(os.path.dirname(__file__))

# 读取图片
img = cv2.imread("../test_with_img_mark.png")
# 获取图片的高度，宽度和通道数
img_height, img_width, img_channels = img.shape
# 设置高斯分布的均值和方差
mean = 0
# 设置高斯分布的标准差
sigma = 10
# 根据均值和标准差生成符合高斯分布的噪声
gauss = np.random.normal(mean, sigma, (img_height, img_width, img_channels))
# 给图片添加高斯噪声
noisy_img = img + gauss
# 设置图片添加高斯噪声之后的像素值的范围
noisy_img = np.clip(noisy_img, a_min=0, a_max=255)
# 保存图片
cv2.imwrite("../noisy_img.png", noisy_img)
