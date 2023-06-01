# 导入库函数
from core.blind_watermark import WaterMark
import core.blind_watermark
import os

# 更改工作目录到当前文件夹
os.chdir(os.path.dirname(__file__))

# print(os.getcwd())  # 获取当前工作目录路径

# 向图像添加水印
bwm = WaterMark(password_img=1, password_wm=1)
# 读取载体图像
# bwm.read_img('../Pictures/test2.jpg')
bwm.read_img('D:/Learn/大学课程/数字图像处理/课程设计/Source/GUI/UI/design/Pictures/test.png')
# 设置水印内容
wm = '2201020228 朱竞阳'
# 读取水印
bwm.read_wm(wm, mode='str')
# 输出叠加水印的图片
bwm.embed('D:/Learn/大学课程/数字图像处理/课程设计/Source/GUI/UI/design/Pictures/teststr.png')
# 获取水印长度
len_wm = len(bwm.wm_bit)
print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))

# 从图像中提取水印
bwm = WaterMark(password_img=1, password_wm=1)
wm_extract = bwm.extract('../Pictures/test_with_str_mark.png', wm_shape=len_wm, mode='str')
print(wm_extract)