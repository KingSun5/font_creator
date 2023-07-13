# -*- coding: utf-8 -*-
import math
#####################################################################################


#####################################################################################


import sys

from PIL import Image
from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from main_win.mainUI import Ui_MainWin
import utils.fileUtils as fileUtils
import utils.timeUtils as timeUtils

# 单个图片信息
IMAGE_INFO_LIST = []
# 当前选择
CUR_SELECT_INDEX = -1
# image scale
IMAGE_SCALE_NUM = 1
# 默认全局宽度
GLOBAL_WIDTH = None
# 默认全局高度
GLOBAL_HEIGHT = None
# 默认全局X轴偏移
GLOBAL_OFFSET_X = 0
# 默认全局Y轴偏移
GLOBAL_OFFSET_Y = 0
# 默认空格宽度
GLOBAL_BLANK_WIDTH = None
# 字体信息
FNT_INFO_DATA = []
# 默认字体间距
DEFAULT_INTERVAL = 2
# 总宽度
TOTAL_WIDTH = 0
# 最大宽度
MAX_WIDTH = 0
# 最大高度
MAX_HEIGHT = 0
# 描述文本
FNT_FILE_TITLE_1 = 'info face="Arial" size=32 bold=0 italic=0 charset="" unicode=1 stretchH=100 smooth=1 aa=1 padding=0,0,0,0 spacing=1,1 outline=0'
FNT_FILE_TITLE_2 = 'common lineHeight=%d base=26 scaleW=%d scaleH=%d pages=1 packed=0 alphaChnl=1 redChnl=0 greenChnl=0 blueChnl=0'
FNT_FILE_TITLE_3 = 'page id=0 file="%s.png"'
FNT_FILE_TITLE_4 = 'chars count=%d'
FNT_FILE_TITLE_5 = 'char id=%d  x=%d   y=%d    width=%d   height=%d   xoffset=%d    yoffset=%d    xadvance=%d   page=0 chnl=15'


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
                addImageInfo(imgPath)
        else:
            if ".png" in filePath:
                addImageInfo(filePath)
        refreshList()
        refreshLayout()


def addImageInfo(path):
    global TOTAL_WIDTH
    global MAX_WIDTH
    global MAX_HEIGHT
    width, height = fileUtils.getImageSize(path)
    #
    itemList = path.replace("\\", "/").split("/")
    item = itemList[len(itemList) - 1].replace(".png", "").replace(".jpg", "")
    if len(item) > 1:
        QMessageBox.information(UI_WIN, "提示", "图片["+item+"]命名错误！！！", QMessageBox.Ok)
        return
    isExist = False
    for info in IMAGE_INFO_LIST:
        if info["name"] == item:
            isExist = True
    if isExist:
        return
    fnt_item_data = {}
    fnt_item_data["name"] = item
    fnt_item_data["path"] = path
    fnt_item_data["id"] = ord(item)
    fnt_item_data["width"] = width
    fnt_item_data["height"] = height
    fnt_item_data["xoffset"] = 0
    fnt_item_data["yoffset"] = 0
    fnt_item_data["xadvance"] = None
    fnt_item_data["page"] = 0
    fnt_item_data["chnl"] = 0
    fnt_item_data["x"] = TOTAL_WIDTH
    fnt_item_data["y"] = 0
    IMAGE_INFO_LIST.append(fnt_item_data)
    #
    TOTAL_WIDTH = TOTAL_WIDTH + width + DEFAULT_INTERVAL
    MAX_WIDTH = max(MAX_WIDTH, width)
    MAX_HEIGHT = max(MAX_HEIGHT, height)


def refreshList():
    keyList = []
    for item in IMAGE_INFO_LIST:
        keyList.append(item["name"])
    slm = QStringListModel()
    slm.setStringList(keyList)  # 将数据设置到model
    UI_WIN.keyList.setModel(slm)


def refreshLayout():
    UI_WIN.letf_tips.setVisible(len(IMAGE_INFO_LIST) == 0)
    if CUR_SELECT_INDEX < 0:
        return
    showPngPath = IMAGE_INFO_LIST[CUR_SELECT_INDEX]["path"]
    pix = QPixmap(showPngPath)
    w, h = fileUtils.getImageSize(showPngPath)

    UI_WIN.detect_image.setVisible(True)
    UI_WIN.detect_image.resize(w * IMAGE_SCALE_NUM, h * IMAGE_SCALE_NUM)
    UI_WIN.detect_image.setPixmap(pix)
    UI_WIN.detect_image.setScaledContents(True)
    UI_WIN.detect_image.move(265 - w * IMAGE_SCALE_NUM / 2, 70)

    if GLOBAL_WIDTH is None:
        UI_WIN.lineEdit_1.setText("")
    else:
        UI_WIN.lineEdit_1.setText(str(GLOBAL_WIDTH))
    if GLOBAL_HEIGHT is None:
        UI_WIN.lineEdit_2.setText("")
    else:
        UI_WIN.lineEdit_2.setText(str(GLOBAL_HEIGHT))
    if GLOBAL_BLANK_WIDTH is None:
        UI_WIN.lineEdit_3.setText("")
    else:
        UI_WIN.lineEdit_3.setText(str(GLOBAL_BLANK_WIDTH))

    if "xadvance" in IMAGE_INFO_LIST[CUR_SELECT_INDEX]:
        UI_WIN.lineEdit_4.setText(str(IMAGE_INFO_LIST[CUR_SELECT_INDEX]["xadvance"]))
    else:
        UI_WIN.lineEdit_4.setText("")
    if "xoffset" in IMAGE_INFO_LIST[CUR_SELECT_INDEX]:
        UI_WIN.lineEdit_5.setText(str(IMAGE_INFO_LIST[CUR_SELECT_INDEX]["xoffset"]))
    else:
        UI_WIN.lineEdit_5.setText("")
    if "yoffset" in IMAGE_INFO_LIST[CUR_SELECT_INDEX]:
        UI_WIN.lineEdit_6.setText(str(IMAGE_INFO_LIST[CUR_SELECT_INDEX]["yoffset"]))
    else:
        UI_WIN.lineEdit_6.setText("")


# list的点击事件
def onClickListViewEvent(qModelIndex):
    global CUR_SELECT_INDEX
    UI_WIN.statusbar.showMessage("")
    CUR_SELECT_INDEX = qModelIndex.row()
    refreshLayout()


# list的点击事件
def onChangeScaleBarEvent(value):
    global IMAGE_SCALE_NUM
    if value <= 50:
        IMAGE_SCALE_NUM = value / 50
    else:
        IMAGE_SCALE_NUM = 1 + ((value - 49) / 50) * 2
    UI_WIN.percentTxt.setText(str(math.ceil(IMAGE_SCALE_NUM * 100)) + "%")
    refreshLayout()

    # list的点击事件


def onClickDeleteEvent():
    global CUR_SELECT_INDEX
    if CUR_SELECT_INDEX < 0:
        return
    IMAGE_INFO_LIST.pop(CUR_SELECT_INDEX)
    CUR_SELECT_INDEX = -1
    UI_WIN.detect_image.setVisible(False)
    refreshList()


# 一键等宽
def onClickAllWidthEvent():
    if GLOBAL_WIDTH is None:
        QMessageBox.information(UI_WIN, "提示", "字体宽度未设置！", QMessageBox.Ok)
        return
    itemIndex = 0
    for item in IMAGE_INFO_LIST:
        IMAGE_INFO_LIST[itemIndex]["xoffset"] = GLOBAL_WIDTH-item["width"]
        itemIndex += 1
    refreshLayout()
    QMessageBox.information(UI_WIN, "提示", "设置成功！", QMessageBox.Ok)


def onClickOpenEvent():
    fileInfo = QFileDialog.getOpenFileNames(UI_WIN, "选择", "C:/Users/Administrator/Desktop", "图片(*.png *jpg)")
    pathList = fileInfo[0]
    for path in pathList:
        addImageInfo(path)
    refreshList()
    refreshLayout()


def onClickExportEvent():
    imgNum = len(IMAGE_INFO_LIST)
    if imgNum == 0:
        return
    if GLOBAL_WIDTH is None:
        QMessageBox.information(UI_WIN, "提示", "字体宽度未设置！", QMessageBox.Ok)
        return
    if GLOBAL_HEIGHT is None:
        QMessageBox.information(UI_WIN, "提示", "字体行高未设置！", QMessageBox.Ok)
        return
    # 保存图片
    toImage = Image.new('RGBA', (TOTAL_WIDTH, MAX_HEIGHT))
    for item in IMAGE_INFO_LIST:
        fromImage = Image.open(item["path"])
        toImage.paste(fromImage, (item["x"], item["y"]))
    fileInfo = QFileDialog.getSaveFileName(UI_WIN, "保存", "C:/Users/Administrator/Desktop", "fnt(*)")
    savaPath = fileInfo[0]
    if len(savaPath) < 5:
        return
    toImage.save(savaPath + ".png")
    tempList = savaPath.split("/")
    fileName = tempList[len(tempList) - 1]
    fntStr = ""
    fntStr = fntStr + FNT_FILE_TITLE_1 + "\n"
    fntStr = fntStr + FNT_FILE_TITLE_2 % (GLOBAL_HEIGHT, TOTAL_WIDTH, MAX_HEIGHT) + "\n"
    fntStr = fntStr + FNT_FILE_TITLE_3 % (fileName) + "\n"
    fntStr = fntStr + FNT_FILE_TITLE_4 % (imgNum - 1) + "\n"
    for item in IMAGE_INFO_LIST:
        p_width = GLOBAL_WIDTH
        if item["xadvance"] is not None:
            p_width = item["xadvance"]
        fntStr = fntStr + FNT_FILE_TITLE_5 % (item["id"], item["x"], item["y"], item["width"], item["height"], item["xoffset"], item["yoffset"], p_width) + "\n"
    if GLOBAL_BLANK_WIDTH is None:
        fntStr = fntStr + FNT_FILE_TITLE_5 % (32, 0, 0, GLOBAL_BLANK_WIDTH, 0, 0, 0, GLOBAL_BLANK_WIDTH) + "\n"

    fileUtils.writeFileTxt(savaPath + ".fnt", fntStr)
    QMessageBox.information(UI_WIN, "提示", "导出成功！", QMessageBox.Ok)


# 设置全局参数
def onClickGlobalEvent():
    global GLOBAL_WIDTH
    global GLOBAL_HEIGHT
    global GLOBAL_BLANK_WIDTH
    g_width = UI_WIN.lineEdit_1.text()
    g_height = UI_WIN.lineEdit_2.text()
    g_blank = UI_WIN.lineEdit_3.text()
    if g_width.isdigit():
        GLOBAL_WIDTH = int(g_width)
    else:
        GLOBAL_WIDTH = None
    if g_height.isdigit():
        GLOBAL_HEIGHT = int(g_height)
    else:
        GLOBAL_HEIGHT = None
    if g_blank.isdigit():
        GLOBAL_BLANK_WIDTH = int(g_blank)
    else:
        GLOBAL_BLANK_WIDTH = None
    QMessageBox.information(UI_WIN, "提示", "设置成功！", QMessageBox.Ok)

# 设置定制参数
def onClickPrivateEvent():
    if CUR_SELECT_INDEX < 0:
        return
    p_width = UI_WIN.lineEdit_4.text()
    p_offsetX = UI_WIN.lineEdit_5.text()
    p_offsetY = UI_WIN.lineEdit_6.text()
    if p_width.isdigit():
        IMAGE_INFO_LIST[CUR_SELECT_INDEX]["xadvance"] = int(p_width)
    else:
        IMAGE_INFO_LIST[CUR_SELECT_INDEX]["xadvance"] = None
    if p_offsetX.isdigit():
        IMAGE_INFO_LIST[CUR_SELECT_INDEX]["xoffset"] = int(p_offsetX)
    if p_offsetY.isdigit():
        IMAGE_INFO_LIST[CUR_SELECT_INDEX]["yoffset"] = int(p_offsetY)
    QMessageBox.information(UI_WIN, "提示", "设置成功！", QMessageBox.Ok)


def initEvent():
    UI_WIN.keyList.clicked.connect(onClickListViewEvent)
    UI_WIN.scaleBar.valueChanged.connect(onChangeScaleBarEvent)
    UI_WIN.btnDelete.clicked.connect(onClickDeleteEvent)
    UI_WIN.btnOpen.clicked.connect(onClickOpenEvent)
    UI_WIN.btnExport.clicked.connect(onClickExportEvent)
    # line edit
    UI_WIN.btnGlobal.clicked.connect(onClickGlobalEvent)
    UI_WIN.btnPrivate.clicked.connect(onClickPrivateEvent)
    # btn width
    UI_WIN.btnWidth.clicked.connect(onClickAllWidthEvent)


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
