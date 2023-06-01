import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QListWidget
from Ui_ui import Ui_MainWindow  #导入你写的界面类
 
 
class MyMainWindow(QMainWindow,Ui_MainWindow): #这里也要记得改
    def __init__(self,parent =None):
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()

    # 定义槽
    def slot_btn_function():
        # 更改label的文字
        myWin.label.setText("Hello World")

    def list_btn_function():
        # 更改label的文字
        myWin.label.setText("Hello World")

        item = myWin.listWidget_2.currentItem()
        print(item.text())
        if item.text() == "1":
            item1_btn_function()
        elif item.text() == "2":
            item2_btn_function()
    
    def item1_btn_function():
        # 更改label的文字
        myWin.label.setText("Hello World1")

    def item2_btn_function():
        # 更改label的文字
        myWin.label.setText("Hello World2")

    # 定义信号和槽
    myWin.pushButton.clicked.connect(slot_btn_function)

    # 获取列表
    list = myWin.findChild(QListWidget, "listWidget_2")
    list.itemClicked.connect(list_btn_function)
    


    myWin.show()
    sys.exit(app.exec_())    