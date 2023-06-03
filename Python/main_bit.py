# 导入库函数
from core.blind_watermark import WaterMark
import core.blind_watermark
import os

# # 更改工作目录到当前文件夹
# os.chdir(os.path.dirname(__file__))

# # print(os.getcwd())  # 获取当前工作目录路径

bwm1 = WaterMark(password_img=1, password_wm=1)
bwm1.read_img('D:/Learn/大学课程/数字图像处理/课程设计/Source/Pictures/test.png')
bwm1.read_wm([True, False, True, True, True, False], mode='bit')
bwm1.embed('D:/Learn/大学课程/数字图像处理/课程设计/Source//Pictures/testbit.png')


bwm1 = WaterMark(password_img=1, password_wm=1)
wm_extract = bwm1.extract('D:/Learn/大学课程/数字图像处理/课程设计/Source/Pictures/testbit.png', mode='bit', wm_shape=6)
print(wm_extract)
