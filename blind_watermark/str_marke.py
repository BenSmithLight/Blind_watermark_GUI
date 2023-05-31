from blind_watermark import WaterMark
import blind_watermark
import os

os.chdir(os.path.dirname(__file__))
blind_watermark.bw_notes.close()

bwm1 = WaterMark(password_img=1, password_wm=1)
bwm1.read_img('../Pictures/test.png')
wm = '2201020228 朱竞阳'
bwm1.read_wm(wm, mode='str')
bwm1.embed('../Pictures/test_with_mark.png')
len_wm = len(bwm1.wm_bit)
print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))

bwm1 = WaterMark(password_img=1, password_wm=1)
wm_extract = bwm1.extract('../Pictures/test_with_mark.png', wm_shape=len_wm, mode='str')
print(wm_extract)