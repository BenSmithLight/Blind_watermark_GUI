# 导入水印处理库
from core.blind_watermark import WaterMark
import core.blind_watermark
# 导入PyQt5库
from functools import partial
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidget, QStackedWidget, QGraphicsScene, QGraphicsPixmapItem
# 导入设计的UI
from design.Ui_main0928 import Ui_MainWindow
# 导入其他库
import warnings
import sys
import os

# 忽略警告
warnings.simplefilter("ignore", FutureWarning)

# 更改工作目录到当前文件夹
os.chdir(os.path.dirname(__file__))


# 定义主窗口类
class MyMainForm(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.start_x = None
        self.start_y = None
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 设置窗口标志：隐藏窗口边框

        # 设置label隐藏
        self.label_3.hide()
        self.label_4.hide()
        self.label_5.hide()
        self.label_7.hide()
        self.label_8.hide()

        # 设置文本颜色
        self.lineEdit_3.setStyleSheet("color: rgb(0, 0, 0);")
        self.lineEdit_7.setStyleSheet("color: rgb(0, 0, 0);")
        self.lineEdit_4.setStyleSheet("color: rgb(0, 0, 0);")
        self.lineEdit_6.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_8.setStyleSheet("color: rgb(255, 255, 255);")

        # 获取列表，并绑定点击事件
        list_obj = self.findChild(QListWidget, "listWidget")
        list_obj.itemClicked.connect(self.list_btn_function)

        # 添加选择文件的按钮
        self.pushButton_3.clicked.connect(partial(self.open_file,
                                                  1))  # 字符串文件选择
        self.pushButton_11.clicked.connect(partial(self.open_file,
                                                   2))  # 图片文件选择
        self.pushButton_12.clicked.connect(partial(self.open_file,
                                                   3))  # 水印文件选择
        self.pushButton_6.clicked.connect(partial(self.open_file, 4))  # 水印文件选择

        # 添加开始嵌入按钮
        self.pushButton.clicked.connect(partial(self.start_add, 'str'))
        self.pushButton_17.clicked.connect(partial(self.start_add, 'img'))
        self.pushButton_8.clicked.connect(partial(self.start_add, 'bit'))

        # 添加水印解析按钮
        self.pushButton_2.clicked.connect(partial(self.read_wm, 'str'))
        self.pushButton_4.clicked.connect(partial(self.read_wm, 'img'))
        self.pushButton_7.clicked.connect(partial(self.read_wm, 'bit'))

        # 添加关闭页面按钮
        self.pushButton_5.clicked.connect(self.close_app)

        # 添加水印密码和解析密码的确认按钮
        self.pushButton_16.clicked.connect(self.password_change)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            super(MyMainForm, self).mousePressEvent(event)
            self.start_x = event.x()
            self.start_y = event.y()

    def mouseReleaseEvent(self, event):
        self.start_x = None
        self.start_y = None

    def mouseMoveEvent(self, event):
        try:
            super(MyMainForm, self).mouseMoveEvent(event)
            dis_x = event.x() - self.start_x
            dis_y = event.y() - self.start_y
            self.move(self.x() + dis_x, self.y() + dis_y)
        except:
            pass

    def effect_shadow_style(self, widget):
        effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        effect_shadow.setOffset(0, 5)  # 偏移
        effect_shadow.setBlurRadius(12)  # 阴影半径
        effect_shadow.setColor(QtCore.Qt.gray)  # 阴影颜色
        widget.setGraphicsEffect(effect_shadow)

    # 定义更改密码的函数
    def password_change(self):
        global password_img  # 图片密码
        global password_wm  # 水印密码
        # 获取水印密码和解析密码
        if (self.lineEdit_6.text() != ''):
            try:
                password_wm = int(self.lineEdit_6.text())
            except:
                pass

    # 定义切换页面的函数
    def list_btn_function(self):
        item = self.listWidget.currentItem()

        # 根据选项切换页面
        if item.text() == "嵌入字符串":
            self.page_window.setCurrentIndex(0)
        elif item.text() == "嵌入图片":
            self.page_window.setCurrentIndex(1)
        elif item.text() == "嵌入比特流":
            self.page_window.setCurrentIndex(2)
        elif item.text() == "设置":
            self.page_window.setCurrentIndex(3)

    # 定义打开文件的函数
    def open_file(self, view=None):
        global file_name  # 待处理的图片
        global wm_img  # 水印图片

        if (view == None):
            return
        elif (view == 1):
            file_name = QtWidgets.QFileDialog.getOpenFileName(
                self, "选择文件", "./", "Image Files (*.png *.jpg *.bmp)")
            # 预览图片
            # 创建scene
            scene = QGraphicsScene()
            # 添加图片
            scene.addItem(QGraphicsPixmapItem(QtGui.QPixmap(file_name[0])))
            # 设置scene
            self.graphicsView.setScene(scene)
            # 缩放大图
            self.graphicsView.fitInView(scene.itemsBoundingRect(),
                                        QtCore.Qt.KeepAspectRatio)
        elif (view == 2):
            file_name = QtWidgets.QFileDialog.getOpenFileName(
                self, "选择文件", "./", "Image Files (*.png *.jpg *.bmp)")
            # 预览图片
            # 创建scene
            scene = QGraphicsScene()
            # 添加图片
            scene.addItem(QGraphicsPixmapItem(QtGui.QPixmap(file_name[0])))
            # 设置scene
            self.graphicsView_4.setScene(scene)
            # 缩放大图
            self.graphicsView_4.fitInView(scene.itemsBoundingRect(),
                                          QtCore.Qt.KeepAspectRatio)
        elif (view == 3):
            wm_img = QtWidgets.QFileDialog.getOpenFileName(
                self, "选择文件", "./", "Image Files (*.png *.jpg *.bmp)")
            # 预览图片
            # 创建scene
            scene = QGraphicsScene()
            # 添加图片
            scene.addItem(QGraphicsPixmapItem(QtGui.QPixmap(wm_img[0])))
            # 设置scene
            self.graphicsView_7.setScene(scene)
            # 缩放大图
            self.graphicsView_7.fitInView(scene.itemsBoundingRect(),
                                          QtCore.Qt.KeepAspectRatio)
        elif (view == 4):
            file_name = QtWidgets.QFileDialog.getOpenFileName(
                self, "选择文件", "./", "Image Files (*.png *.jpg *.bmp)")
            # 预览图片
            # 创建scene
            scene = QGraphicsScene()
            # 添加图片
            scene.addItem(QGraphicsPixmapItem(QtGui.QPixmap(file_name[0])))
            # 设置scene
            self.graphicsView_6.setScene(scene)
            # 缩放大图
            self.graphicsView_6.fitInView(scene.itemsBoundingRect(),
                                          QtCore.Qt.KeepAspectRatio)

    # 定义开始嵌入的函数
    def start_add(self, mod=None):
        # 显示运行状态
        self.label_8.show()
        QApplication.processEvents()  # 强制更新UI

        global wm_shape  # 水印图片的大小
        # 向图像添加水印
        bwm = WaterMark(password_img=password_img, password_wm=password_wm)

        # 检查文件输入，否则弹窗提醒
        try:
            if file_name[0] == '':
                QtWidgets.QMessageBox.warning(self, '警告', '请选择文件')
                return
        except:
            QtWidgets.QMessageBox.warning(self, '警告', '请选择文件')
            return

        # 参数检查部分
        if mod is None:
            return

        elif mod == 'str':
            # 检查输入，否则弹窗提醒
            if self.lineEdit_3.text() == '':
                QtWidgets.QMessageBox.warning(self, '警告', '请输入水印内容')
                return
            # 检查文件输入，否则弹窗提醒
            if file_name[0] == '':
                QtWidgets.QMessageBox.warning(self, '警告', '请选择文件')
                return

            # 获取嵌入的字符串
            wm = self.lineEdit_3.text()
            bwm.read_wm(wm_content=wm, mode='str')
            # 获取水印长度
            len_wm = len(bwm.wm_bit)
            # 输出水印长度
            self.lineEdit_3.setText('水印长度为： {len_wm}'.format(len_wm=len_wm))
            # 处理图片
            bwm.read_img(file_name[0])
            # 输出叠加水印的图片
            out_file = file_name[0][:-4] + '_with_str_mark' + file_name[0][-4:]
            bwm.embed(out_file)

            # 显示嵌入后的图片
            # 创建scene
            scene = QGraphicsScene()
            # 添加图片
            scene.addItem(QGraphicsPixmapItem(QtGui.QPixmap(out_file)))
            # 设置scene
            self.graphicsView_2.setScene(scene)
            # 缩放大图
            self.graphicsView_2.fitInView(scene.itemsBoundingRect(),
                                          QtCore.Qt.KeepAspectRatio)
            self.label_3.show()

        elif mod == 'img':
            # 检查文件输入，否则弹窗提醒
            if file_name[0] == '':
                QtWidgets.QMessageBox.warning(self, '警告', '请选择文件')
                return
            # 检查水印文件输入，否则弹窗提醒
            if wm_img[0] == '':
                QtWidgets.QMessageBox.warning(self, '警告', '请选择水印文件')
                return

            # 获取嵌入的图片
            wm = wm_img[0]
            wm_shape = bwm.read_wm(wm_content=wm, mode='img')
            # 输出水印大小
            self.lineEdit_7.setText('解析得水印大小为： {}'.format(wm_shape))
            # 处理图片
            bwm.read_img(file_name[0])
            # 输出叠加水印的图片
            out_file = file_name[0][:-4] + '_with_img_mark' + file_name[0][-4:]
            embed_img = bwm.embed(out_file)

            if (embed_img == 'error'):
                # 输出提示信息
                self.lineEdit_7.setText('水印图片过大，无法嵌入')
                self.label_8.hide()
                return

            # 显示嵌入后的图片
            # 创建scene
            scene = QGraphicsScene()
            # 添加图片
            scene.addItem(QGraphicsPixmapItem(QtGui.QPixmap(out_file)))
            # 设置scene
            self.graphicsView_3.setScene(scene)
            # 缩放大图
            self.graphicsView_3.fitInView(scene.itemsBoundingRect(),
                                          QtCore.Qt.KeepAspectRatio)
            self.label_5.show()
            self.label_4.hide()

        elif mod == 'bit':
            # 检查输入，否则弹窗提醒
            if self.lineEdit_4.text() == '':
                QtWidgets.QMessageBox.warning(self, '警告', '请输入水印内容')
                return
            # 检查文件输入，否则弹窗提醒
            if file_name[0] == '':
                QtWidgets.QMessageBox.warning(self, '警告', '请选择文件')
                return

            # 获取嵌入的字符串
            bit_data = self.lineEdit_4.text()
            # 将输入的10110等字符串转换为[True, False, True, True, True, False]等列表
            bit_data = [True if i == '1' else False for i in bit_data]
            wm = bit_data
            bwm.read_wm(wm_content=wm, mode='bit')
            # 获取水印长度
            len_wm = len(bwm.wm_bit)
            # 输出水印长度
            self.lineEdit_4.setText('水印长度为： {len_wm}'.format(len_wm=len_wm))
            # 处理图片
            bwm.read_img(file_name[0])
            # 输出叠加水印的图片
            out_file = file_name[0][:-4] + '_with_bit_mark' + file_name[0][-4:]
            bwm.embed(out_file)

            # 显示嵌入后的图片
            # 创建scene
            scene = QGraphicsScene()
            # 添加图片
            scene.addItem(QGraphicsPixmapItem(QtGui.QPixmap(out_file)))
            # 设置scene
            self.graphicsView_5.setScene(scene)
            # 缩放大图
            self.graphicsView_5.fitInView(scene.itemsBoundingRect(),
                                          QtCore.Qt.KeepAspectRatio)
            self.label_7.show()
        self.label_8.hide()

    # 定义水印解析的函数
    def read_wm(self, mod=None):
        # 显示运行状态
        self.label_8.show()
        QApplication.processEvents()  # 强制更新UI

        # 检查文件输入，否则弹窗提醒
        try:
            if file_name[0] == '':
                QtWidgets.QMessageBox.warning(self, '警告', '请选择文件')
                return
        except:
            QtWidgets.QMessageBox.warning(self, '警告', '请选择文件')
            return

        if mod is None:
            return
        elif mod == 'str':
            # 检查输入，否则弹窗提醒
            if self.lineEdit_3.text() == '':
                QtWidgets.QMessageBox.warning(self, '警告', '请输入水印长度')
                return
            # 检查输入的是否整数，否则弹窗提醒
            try:
                int(self.lineEdit_3.text())
            except:
                QtWidgets.QMessageBox.warning(self, '警告', '请输入整数')
                return
            # 检查文件的名字中是否包含mark，否则弹窗提醒
            if 'mark' not in file_name[0]:
                QtWidgets.QMessageBox.warning(self, '警告', '你可能选择了不带水印的图片')

            len_wm = int(self.lineEdit_3.text())
            bwm = WaterMark(password_img=password_img, password_wm=password_wm)
            wm_extract = bwm.extract(file_name[0], wm_shape=len_wm, mode='str')
            self.lineEdit_3.setText("水印内容为： {}".format(wm_extract))
        elif mod == 'img':
            # 检查文件的名字中是否包含mark，否则弹窗提醒
            if 'mark' not in file_name[0]:
                QtWidgets.QMessageBox.warning(self, '警告', '你可能选择了不带水印的图片')
            # 检查输入是否两个整数，否则弹窗提醒
            try:
                wm_shape = eval(self.lineEdit_7.text())
            except:
                QtWidgets.QMessageBox.warning(self, '警告',
                                              '请按提示输入尺寸。例如：(50, 50)')
                return
            # 定义解析出的水印输出的位置
            out_wm = file_name[0][:-4] + '_extracted_mark' + file_name[0][-4:]
            bwm = WaterMark(password_img=password_img, password_wm=password_wm)
            wm_extract = bwm.extract(file_name[0],
                                     wm_shape=wm_shape,
                                     out_wm_name=out_wm,
                                     mode='img')

            # 显示解析出的水印
            # 创建scene
            scene = QGraphicsScene()
            # 添加图片
            scene.addItem(QGraphicsPixmapItem(QtGui.QPixmap(out_wm)))
            # 设置scene
            self.graphicsView_12.setScene(scene)
            # 缩放大图
            self.graphicsView_12.fitInView(scene.itemsBoundingRect(),
                                           QtCore.Qt.KeepAspectRatio)
            self.label_5.hide()
            self.label_4.show()
        elif mod == 'bit':
            # 检查输入，否则弹窗提醒
            if self.lineEdit_4.text() == '':
                QtWidgets.QMessageBox.warning(self, '警告', '请输入水印长度')
                return
            # 检查输入的是否整数，否则弹窗提醒
            try:
                int(self.lineEdit_4.text())
            except:
                QtWidgets.QMessageBox.warning(self, '警告', '请输入整数')
                return
            # 检查文件的名字中是否包含mark，否则弹窗提醒
            if 'mark' not in file_name[0]:
                QtWidgets.QMessageBox.warning(self, '警告', '你可能选择了不带水印的图片')

            len_wm = int(self.lineEdit_4.text())
            bwm = WaterMark(password_img=password_img, password_wm=password_wm)
            wm_extract = bwm.extract(file_name[0], wm_shape=len_wm, mode='bit')
            # 输出结果转换为10101等字符串
            wm_extract = ''.join(
                ['1' if i == True else '0' for i in wm_extract])
            self.lineEdit_4.setText("水印内容为： {}".format(wm_extract))
            self.label_7.hide()
        self.label_8.hide()

    # 定义关闭页面的函数
    def close_app(self):
        QApplication.quit()


if __name__ == "__main__":
    # 初始化窗口
    app = QApplication(sys.argv)
    myWin = MyMainForm()

    # 设置水印密码和解析密码
    password_img = 1
    password_wm = 1

    # 运行窗口
    myWin.show()
    sys.exit(app.exec_())
