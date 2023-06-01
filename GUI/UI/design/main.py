# 导入库函数
from core.blind_watermark import WaterMark
import core.blind_watermark
import os
import sys

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidget, QStackedWidget, QGraphicsScene, QGraphicsPixmapItem

from Ui_main0928 import Ui_MainWindow

# 更改工作目录到当前文件夹
os.chdir(os.path.dirname(__file__))


class MyMainForm(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.start_x = None
        self.start_y = None
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 设置窗口标志：隐藏窗口边框

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()

    # 定义切换页面的函数
    def list_btn_function():
        item = myWin.listWidget.currentItem()

        # 根据选项切换页面
        if item.text() == "嵌入字符串":
            myWin.page_window.setCurrentIndex(0)
        elif item.text() == "嵌入图片":
            myWin.page_window.setCurrentIndex(1)
        elif item.text() == "嵌入比特流":
            myWin.page_window.setCurrentIndex(2)
        elif item.text() == "设置":
            myWin.page_window.setCurrentIndex(3)

    # 定义打开文件的函数
    def open_file():
        myWin.widget_3.hide()
        myWin.pushButton.show()
        global file_name
        file_name = QtWidgets.QFileDialog.getOpenFileName(
            myWin, "选择文件", "./", "Image Files (*.png *.jpg *.bmp)")
        print(file_name[0])

        # 预览图片
        # 创建scene
        scene = QGraphicsScene()
        # 添加图片
        scene.addItem(QGraphicsPixmapItem(QtGui.QPixmap(file_name[0])))
        # 设置scene
        myWin.graphicsView.setScene(scene)
        # 缩放大图
        myWin.graphicsView.fitInView(scene.itemsBoundingRect(),
                                     QtCore.Qt.KeepAspectRatio)

    # 定义开始嵌入的函数
    def start_add():
        # 检查输入，否则弹窗提醒
        if myWin.lineEdit_3.text() == '':
            QtWidgets.QMessageBox.warning(myWin, '警告', '请输入水印内容')
            return
        # 检查文件输入，否则弹窗提醒
        if file_name[0] == '':
            QtWidgets.QMessageBox.warning(myWin, '警告', '请选择文件')
            return
        # 获取嵌入的字符串
        str = myWin.lineEdit_3.text()

        # 向图像添加水印
        bwm = WaterMark(password_img=1, password_wm=1)
        # 读取载体图像
        bwm.read_img(file_name[0])
        # 设置水印内容
        wm = str
        # 读取水印
        bwm.read_wm(wm, mode='str')
        # 输出叠加水印的图片
        bwm.embed(file_name[0][:-4] + '_with_str_mark' + file_name[0][-4:])
        output_file = file_name[0][:-4] + '_with_str_mark' + file_name[0][-4:]
        # bwm.embed('../Pictures/test_with_str_mark.png')
        # 获取水印长度
        len_wm = len(bwm.wm_bit)
        print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))
        # 输出水印长度
        myWin.lineEdit_3.setText('水印长度为： {len_wm}'.format(len_wm=len_wm))

        # 显示嵌入后的图片
        # 创建scene
        scene = QGraphicsScene()
        # 添加图片
        scene.addItem(QGraphicsPixmapItem(QtGui.QPixmap(output_file)))
        # 设置scene
        myWin.graphicsView_2.setScene(scene)
        # 缩放大图
        myWin.graphicsView_2.fitInView(scene.itemsBoundingRect(),
                                       QtCore.Qt.KeepAspectRatio)

        myWin.label_3.show()

    # 定义水印解析的函数
    def read_wm():
        # 检查输入，否则弹窗提醒
        if myWin.lineEdit_3.text() == '':
            QtWidgets.QMessageBox.warning(myWin, '警告', '请输入水印长度')
            return
        # 检查输入的是否整数，否则弹窗提醒
        try:
            int(myWin.lineEdit_3.text())
        except:
            QtWidgets.QMessageBox.warning(myWin, '警告', '请输入整数')
            return
        # 检查文件的名字中是否包含mark，否则弹窗提醒
        if 'mark' not in file_name[0]:
            QtWidgets.QMessageBox.warning(myWin, '警告', '你可能选择了不带水印的图片')
            return

        # 检查文件输入，否则弹窗提醒
        if file_name[0] == '':
            QtWidgets.QMessageBox.warning(myWin, '警告', '请选择文件')
            return
        len_wm = int(myWin.lineEdit_3.text())
        bwm = WaterMark(password_img=1, password_wm=1)
        wm_extract = bwm.extract(file_name[0], wm_shape=len_wm, mode='str')
        # print(wm_extract)
        myWin.lineEdit_3.setText("水印内容为： {}".format(wm_extract))
        myWin.pushButton.hide()
        myWin.widget_3.show()


    # 获取列表
    list = myWin.findChild(QListWidget, "listWidget")
    list.itemClicked.connect(list_btn_function)

    # 添加选择文件的按钮
    myWin.pushButton_3.clicked.connect(open_file)

    # 设置label隐藏
    myWin.label_3.hide()
    myWin.widget_3.hide()

    # 固定视口大小
    myWin.graphicsView.setFixedSize(370, 370)

    # 添加开始嵌入按钮
    myWin.pushButton.clicked.connect(start_add)

    # 设置文本颜色
    myWin.lineEdit_3.setStyleSheet("color: rgb(0, 0, 0);")

    # 添加水印解析按钮
    myWin.pushButton_2.clicked.connect(read_wm)

    myWin.show()
    sys.exit(app.exec_())
