import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QApplication
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.faker import Faker

from main1006 import Ui_MainWindow


class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.start_x = None
        self.start_y = None
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 设置窗口标志：隐藏窗口边框
        # self.html = '/Users/jianjin/Desktop/planning.html'
        # self.webEngineView.setUrl(QUrl('file://' + self.html))
        # self.init_cake()

    def init_cake(self,):
        """饼图"""
        html = 'planning.html'
        pie = Pie()
        pie.add(
            "",
            [list(z) for z in zip(Faker.choose(), Faker.values())],
            radius=["40%", "75%"],
        )
        pie.set_global_opts(
            title_opts=opts.TitleOpts(title=''),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
        )
        pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        pie.render(self.html)
        self.webEngineView.setUrl(QUrl('file://' + self.html))
        self.webEngineView.setZoomFactor(0.5)

    def mousePressEvent(self, event):
        super(MyMainForm, self).mousePressEvent(event)
        self.start_x = event.x()
        self.start_y = event.y()

    def mouseReleaseEvent(self, event):
        self.origin_x = None
        self.origin_y = None
        self.start_x = None
        self.start_y = None

    def mouseMoveEvent(self, event):
        try:
            super(MyMainForm, self).mouseMoveEvent(event)
            dis_x = event.x() - self.start_x
            dis_y = event.y() - self.start_y
            self.move(self.x() + dis_x, self.y() + dis_y)
        except BaseException as f:
            pass

    def effect_shadow_style(self, widget):
        effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        effect_shadow.setOffset(0, 8)  # 偏移
        effect_shadow.setBlurRadius(48)  # 阴影半径
        effect_shadow.setColor(QColor(162, 129, 247))  # 阴影颜色
        widget.setGraphicsEffect(effect_shadow)

    def effect_shadow_style2(self, widget):
        effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        effect_shadow.setOffset(0, 8)  # 偏移
        effect_shadow.setBlurRadius(48)  # 阴影半径
        effect_shadow.setColor(QColor(253, 139, 133))  # 阴影颜色
        widget.setGraphicsEffect(effect_shadow)

    def effect_shadow_style3(self, widget):
        effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        effect_shadow.setOffset(0, 8)  # 偏移
        effect_shadow.setBlurRadius(48)  # 阴影半径
        effect_shadow.setColor(QColor(243, 175, 189))  # 阴影颜色
        widget.setGraphicsEffect(effect_shadow)

    def effect_shadow_style4(self, widget):
        effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        effect_shadow.setOffset(0, 8)  # 偏移
        effect_shadow.setBlurRadius(48)  # 阴影半径
        effect_shadow.setColor(QColor(66, 226, 192))  # 阴影颜色
        widget.setGraphicsEffect(effect_shadow)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
