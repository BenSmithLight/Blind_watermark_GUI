## 椒盐噪声

# 导入库
import cv2
import numpy as np
import os

# 修改工作目录
os.chdir(os.path.dirname(__file__))

# 读取图片
img = cv2.imread("../test_with_img_mark.png")
# 设置添加椒盐噪声的数目比例
s_vs_p = 0.5
# 设置添加噪声图像像素的数目
amount = 0.04
noisy_img = np.copy(img)
# 添加salt噪声
num_salt = np.ceil(amount * img.size * s_vs_p)
# 设置添加噪声的坐标位置
coords = [np.random.randint(0, i - 1, int(num_salt)) for i in img.shape]
noisy_img[coords[0], coords[1], :] = [255, 255, 255]
# 添加pepper噪声
num_pepper = np.ceil(amount * img.size * (1. - s_vs_p))
# 设置添加噪声的坐标位置
coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in img.shape]
noisy_img[coords[0], coords[1], :] = [0, 0, 0]
# 保存图片
cv2.imwrite("../noisy_img2.png", noisy_img)

