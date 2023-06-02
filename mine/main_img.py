from core.blind_watermark import WaterMark
import core.blind_watermark as blind_watermark
import os

# os.chdir(os.path.dirname(__file__))

bwm1 = WaterMark(password_wm=1, password_img=1)
# read original image
bwm1.read_img('D:/Learn/Pictures_test/test4.jpg')
# read watermark
bwm1.read_wm('D:/Learn/Pictures_test/QRcode_50.png')
# embed
bwm1.embed('D:/Learn/Pictures_test/test_with_img_mark.jpg')

print('Done!')

bwm1 = WaterMark(password_wm=1, password_img=1)
# notice that wm_shape is necessary
bwm1.extract(filename='D:/Learn/Pictures_test/test_with_img_mark.jpg', wm_shape=(50, 50), out_wm_name='D:/Learn/Pictures_test/test_with_img_mark_result.jpg', )

print('Done!')