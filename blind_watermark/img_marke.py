from blind_watermark import WaterMark
import blind_watermark
import os

os.chdir(os.path.dirname(__file__))
blind_watermark.bw_notes.close()

bwm1 = WaterMark(password_wm=1, password_img=1)
# read original image
bwm1.read_img('../Pictures/test.png')
# read watermark
bwm1.read_wm('../Pictures/QRcode_small.png')
# embed
bwm1.embed('../Pictures/test_with_imgmark.png')

bwm1 = WaterMark(password_wm=1, password_img=1)
# notice that wm_shape is necessary
bwm1.extract(filename='../Pictures/test_with_imgmark.png', wm_shape=(50, 50), out_wm_name='../Pictures/imgmark.png', )
