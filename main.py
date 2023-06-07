# -*- coding: utf-8 -*-
import math
#####################################################################################


#####################################################################################


import sys

from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from main_win.mainUI import Ui_MainWin
import utils.fileUtils as fileUtils
import utils.timeUtils as timeUtils


IMAGE_PATH_LIST = []
# 当前选择
CUR_SELECT_INDEX = -1
# image scale
IMAGE_SCALE_NUM  = 1

class DragChangeWin(QMainWindow, Ui_MainWin):
    def __init__(self, parent=None):
        super(DragChangeWin, self).__init__(parent)
        self.setupUi(self)
        # 调用Drops方法
        self.setAcceptDrops(True)

    # 鼠标进入
    def dragEnterEvent(self, evn):
        # 鼠标放开函数事件
        evn.accept()

    # 鼠标放开
    def dropEvent(self, evn):
        filePath = evn.mimeData().text().split("///")[1]

        if fileUtils.isDir(filePath):
            pngList = fileUtils.getAllFileBySuffix(filePath, ".png")
            for imgPath in pngList:
                if not (imgPath in IMAGE_PATH_LIST):
                    IMAGE_PATH_LIST.append(imgPath)
        else:
            if (".png" in filePath) and not (filePath in IMAGE_PATH_LIST):
                IMAGE_PATH_LIST.append(filePath)
        refreshList()

def refreshList():
    keyList = []
    for sPath in IMAGE_PATH_LIST:
        itemList = sPath.replace("\\", "/").split("/")
        item = itemList[len(itemList) - 1]
        keyList.append(item)
    slm = QStringListModel()
    slm.setStringList(keyList)  # 将数据设置到model
    UI_WIN.keyList.setModel(slm)

def refreshLayout():
    if CUR_SELECT_INDEX < 0:
        return
    showPngPath = IMAGE_PATH_LIST[CUR_SELECT_INDEX]
    pix = QPixmap(showPngPath)
    w, h = fileUtils.getImageSize(showPngPath)

    UI_WIN.detect_image.resize(w*IMAGE_SCALE_NUM, h*IMAGE_SCALE_NUM)
    UI_WIN.detect_image.setPixmap(pix)
    UI_WIN.detect_image.setScaledContents(True)
    UI_WIN.detect_image.move(265 - w*IMAGE_SCALE_NUM/2, 70)


# list的点击事件
def onClickListViewEvent(qModelIndex):
    global CUR_SELECT_INDEX
    UI_WIN.statusbar.showMessage("")
    CUR_SELECT_INDEX = qModelIndex.row()
    refreshLayout()


# list的点击事件
def onChangeScaleBarEvent(value):
    print(value)
    global IMAGE_SCALE_NUM
    if value <= 50:
        IMAGE_SCALE_NUM = value/50
    else:
        IMAGE_SCALE_NUM = 1+((value-49)/50)*9
    UI_WIN.percentTxt.setText(str(math.ceil(IMAGE_SCALE_NUM*100))+"%")
    refreshLayout()

    # list的点击事件
def onClickDeleteEvent():
    global CUR_SELECT_INDEX
    if CUR_SELECT_INDEX < 0:
        return
    IMAGE_PATH_LIST.pop(CUR_SELECT_INDEX)
    CUR_SELECT_INDEX = -1
    refreshList()


def initEvent():
    UI_WIN.keyList.clicked.connect(onClickListViewEvent)
    UI_WIN.scaleBar.valueChanged.connect(onChangeScaleBarEvent)
    UI_WIN.deleteBtn.clicked.connect(onClickDeleteEvent)

def initLayout():
    UI_WIN.scaleBar.setValue(50)


if __name__ == '__main__':
    # app初始化
    app = QApplication(sys.argv)
    UI_WIN = DragChangeWin()
    UI_WIN.show()
    UI_WIN.setFixedSize(UI_WIN.width(), UI_WIN.height())
    initLayout()
    initEvent()
    sys.exit(app.exec_())

