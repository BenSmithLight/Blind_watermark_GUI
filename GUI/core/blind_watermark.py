import warnings

import numpy as np
import cv2

from core.bwm_core import WaterMarkCore


class WaterMark:

    def __init__(self,
                 password_wm=1,
                 password_img=1,
                 block_shape=(4, 4),
                 mode='common',
                 processes=None):

        # 初始化水印处理函数
        self.bwm_core = WaterMarkCore(password_img=password_img,
                                      mode=mode,
                                      processes=processes)

        self.password_wm = password_wm

        self.wm_bit = None
        self.wm_size = 0

    def read_img(self, filename=None, img=None):
        # 如果没有传入图像，则使用opencv读取图像
        if img is None:
            # img = cv2.imread(filename, flags=cv2.IMREAD_UNCHANGED)
            img = cv2.imdecode(np.fromfile(filename, dtype=np.uint8), -1)
            # cv2.IMREAD_UNCHANGED表示不进行颜色空间转换，否则图像将变为BGR空间，非RGB
            assert img is not None, "文件读取失败，请检查文件路径"

        # 将图片传入水印处理函数
        self.bwm_core.read_img_arr(img=img)

    def read_wm(self, wm_content, mode='img'):
        # 输入检查
        assert mode in ('img', 'str', 'bit'), "输入模式错误，应该为img/str/bit"

        if mode == 'img':
            # wm = cv2.imread(filename=wm_content, flags=cv2.IMREAD_GRAYSCALE)
            wm = cv2.imdecode(np.fromfile(wm_content, dtype=np.uint8), 0)
            # 获取图像大小
            wm_shape = wm.shape

            assert wm is not None, 'file "{filename}" not read'.format(
                filename=wm_content)

            # 读入图片格式的水印，并转为一维 bit 格式，抛弃灰度级别
            self.wm_bit = wm.flatten() > 128

        elif mode == 'str':
            byte = bin(int(wm_content.encode('utf-8').hex(),
                           base=16))[2:]  # 将输入的水印转换为二进制字符串
            self.wm_bit = (np.array(list(byte)) == '1')  # 将二进制字符串转换为 bit 格式
        else:
            self.wm_bit = np.array(wm_content)

        self.wm_size = self.wm_bit.size  # 记录水印长度

        # 水印加密:
        np.random.RandomState(self.password_wm).shuffle(
            self.wm_bit)  # 通过password_wm作为随机数种子对水印进行乱序

        self.bwm_core.read_wm(self.wm_bit)

        # 如果变量wm_shape存在，则返回该变量
        try:
            return wm_shape
        except:
            pass

    def embed(self, filename=None, compression_ratio=None):
        '''
        :param filename: string
            Save the image file as filename
        :param compression_ratio: int or None
            If compression_ratio = None, do not compression,
            If compression_ratio is integer between 0 and 100, the smaller, the output file is smaller.
        :return:
        '''
        # 调用函数执行水印嵌入
        embed_img = self.bwm_core.embed()

        if (embed_img == 'error'):
            return 'error'


        # 如果提供了文件名，则保存图像，否则直接返回图像
        if filename is not None:
            # 如果不设置图像压缩，则直接输出图像
            if compression_ratio is None:
                # cv2.imwrite(filename=filename, img=embed_img)
                cv2.imencode('.png', embed_img)[1].tofile(filename)
            # 如果设置了图像压缩，则按照图像类型进行压缩
            elif filename.endswith('.jpg'):
                cv2.imwrite(
                    filename=filename,
                    img=embed_img,
                    params=[cv2.IMWRITE_JPEG_QUALITY, compression_ratio])
            elif filename.endswith('.png'):
                cv2.imwrite(
                    filename=filename,
                    img=embed_img,
                    params=[cv2.IMWRITE_PNG_COMPRESSION, compression_ratio])
            # 如果是其他类型的图像，则直接输出
            else:
                # cv2.imwrite(filename=filename, img=embed_img)
                cv2.imencode('.png', embed_img)[1].tofile(filename)
        return embed_img

    def extract_decrypt(self, wm_avg):
        wm_index = np.arange(self.wm_size)
        # 通过password_wm作为随机数种子对水印进行乱序
        np.random.RandomState(self.password_wm).shuffle(wm_index)
        wm_avg[wm_index] = wm_avg.copy()
        return wm_avg

    def extract(self,
                filename=None,
                embed_img=None,
                wm_shape=None,
                out_wm_name=None,
                mode='img'):
        # 检查水印长度是否提供
        assert wm_shape is not None, 'wm_shape needed'

        if filename is not None:
            # embed_img = cv2.imread(filename, flags=cv2.IMREAD_COLOR)
            embed_img = cv2.imdecode(np.fromfile(filename, dtype=np.uint8), -1)
            assert embed_img is not None, "{filename} not read".format(
                filename=filename)

        self.wm_size = np.array(wm_shape).prod()  # 记录水印长度

        if mode in ('str', 'bit'):
            wm_avg = self.bwm_core.extract_with_kmeans(img=embed_img,
                                                       wm_shape=wm_shape)
        else:
            wm_avg = self.bwm_core.extract(img=embed_img, wm_shape=wm_shape)

        # 解密：
        wm = self.extract_decrypt(wm_avg=wm_avg)

        # 转化为指定格式：
        if mode == 'img':
            wm = 255 * wm.reshape(wm_shape[0], wm_shape[1])
            # cv2.imwrite(out_wm_name, wm)
            cv2.imencode('.png', wm)[1].tofile(out_wm_name)
        elif mode == 'str':
            try:
                byte = ''.join(str((i >= 0.5) * 1) for i in wm)
                wm = bytes.fromhex(hex(int(byte,
                                        base=2))[2:]).decode('utf-8',
                                                                errors='replace')
            except:
                wm = '解析错误，请检查密码和水印长度'

        return wm
