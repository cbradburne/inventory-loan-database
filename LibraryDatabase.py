
# Windows
# python -m pip install PySide6
# python -m pip install tinydb
# python -m pip install fpdf
# python -m pip install pyinstaller
# python -m PyInstaller --onefile --windowed --icon="dbIcon.ico" LibraryDatabase.py

# macOS
# python3 -m pip install PySide6
# python3 -m pip install tinydb
# python3 -m pip install fpdf
# python3 -m pip install pyinstaller

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import QWidget, QMainWindow, QFileDialog, QMessageBox

from datetime import datetime, timedelta
from tinydb import TinyDB, Query, where
from fpdf import FPDF
import sys, time, re, os, subprocess, csv


showLongTerm = False
watchCellChange = True

dateRangeFrom = 0.0
dateRangeTo = 0.0
historyItemID = ""
historyUserEmail = ""

allItemsSearchText = ""
allItemsSearchID = ""

allUsersSearchID = ""
allUsersSearchName = ""
allUsersSearchEmail = ""

DBquery = Query()
userNameList = []

if sys.platform == "win32" or sys.platform == "Windows" or sys.platform == "win":                           # Tests if using Windows as different OS has different Printer code
    isWindows = True

    try:
        os.mkdir('C:\\Users\\Public\\Documents\\Database')
    except:
        pass

    try:
        itemDB = TinyDB('C:\\Users\\Public\\Documents\\Database\\itemdb.json')
    except:
        file_name = 'C:\\Users\\Public\\Documents\\Database\\itemdb.json'
        f = open(file_name, 'a')  # open file, create if doesn't exist
        f.close()

    try:
        userDB = TinyDB('C:\\Users\\Public\\Documents\\Database\\userdb.json')
    except:
        file_name = 'C:\\Users\\Public\\Documents\\Database\\userdb.json'
        f = open(file_name, 'a')  # open file, create if doesn't exist
        f.close()

    try:
        outDB = TinyDB('C:\\Users\\Public\\Documents\\Database\\outdb.json')
    except:
        file_name = 'C:\\Users\\Public\\Documents\\Database\\outdb.json'
        f = open(file_name, 'a')  # open file, create if doesn't exist
        f.close()

    try:
        historyDB = TinyDB('C:\\Users\\Public\\Documents\\Database\\historydb.json')
    except:
        file_name = 'C:\\Users\\Public\\Documents\\Database\\historydb.json'
        f = open(file_name, 'a')  # open file, create if doesn't exist
        f.close()


    bookedOutPath = 'C:\\Users\\Public\\Documents\\Database\\BookedOut.pdf'
    f = open(bookedOutPath, 'a')  # open file, create if doesn't exist
    f.close()

    historyPath = 'C:\\Users\\Public\\Documents\\Database\\History.pdf'
    f = open(historyPath, 'a')  # open file, create if doesn't exist
    f.close()

    itemsPath = 'C:\\Users\\Public\\Documents\\Database\\Items.pdf'
    f = open(itemsPath, 'a')  # open file, create if doesn't exist
    f.close()

    usersPath = 'C:\\Users\\Public\\Documents\\Database\\Users.pdf'
    f = open(itemsPath, 'a')  # open file, create if doesn't exist
    f.close()
    #print("IS Windows")
else:
    isWindows = False

    try:
        os.mkdir('/Users/Shared/Database')
    except:
        pass

    try:
        itemDB = TinyDB('/Users/Shared/Database/itemdb.json')
    except:
        file_name = '/Users/Shared/Database/itemdb.json'
        f = open(file_name, 'a')  # open file, create if doesn't exist
        f.close()

    try:
        userDB = TinyDB('/Users/Shared/Database/userdb.json')
    except:
        file_name = '/Users/Shared/Database/userdb.json'
        f = open(file_name, 'a')  # open file, create if doesn't exist
        f.close()

    try:
        outDB = TinyDB('/Users/Shared/Database/outdb.json')
    except:
        file_name = '/Users/Shared/Database/outdb.json'
        f = open(file_name, 'a')  # open file, create if doesn't exist
        f.close()

    try:
        historyDB = TinyDB('/Users/Shared/Database/historydb.json')
    except:
        file_name = '/Users/Shared/Database/historydb.json'
        f = open(file_name, 'a')  # open file, create if doesn't exist
        f.close()


    bookedOutPath = '/Users/Shared/Database/BookedOut.pdf'
    f = open(bookedOutPath, 'a')  # open file, create if doesn't exist
    f.close()

    historyPath = '/Users/Shared/Database/History.pdf'
    f = open(historyPath, 'a')  # open file, create if doesn't exist
    f.close()

    itemsPath = '/Users/Shared/Database/Items.pdf'
    f = open(itemsPath, 'a')  # open file, create if doesn't exist
    f.close()

    usersPath = '/Users/Shared/Database/Users.pdf'
    f = open(itemsPath, 'a')  # open file, create if doesn't exist
    f.close()
    #print("is NOT Windows")

class databaseApp(QMainWindow):
    def __init__(self, txt):
        self.text = txt
        super(databaseApp, self).__init__()
        self.setupUi()
        self.installEventFilter(self) #keyboard control

    def eventFilter(self, obj, event):
        if (event.type() == QtCore.QEvent.KeyPress):
            key = event.key()
            if key == QtCore.Qt.Key_Escape:
                if self.listWidgetBOUserName.isVisible():
                    self.listWidgetBOUserName.clear()
                    self.listWidgetBOUserName.hide()
                    self.lineEditBOUserName.setText("")
                    self.lineEditBOUserID.setFocus()
                elif self.listWidgetBOUserEmail.isVisible():
                    self.listWidgetBOUserEmail.hide()
                    self.listWidgetBOUserName.hide()
                    self.lineEditBOUserName.setText("")
                    self.lineEditBOUserEmail.setText("")
                    self.lineEditBOUserID.setFocus()
                    self.listWidgetBOUserName.clear()
                    self.listWidgetBOUserEmail.clear()

        return super(databaseApp, self).eventFilter(obj, event)

    def setupUi(self):
        ag = QtGui.QGuiApplication.primaryScreen().availableGeometry()
        agX = ag.width()
        agY = ag.height()

        if agX > 1800:
            agX = agX - 200
            agY = agY - 100

        sgX = agX / 200
        sgY = agY / 100

        self.setObjectName("MainWindow")
        self.resize(agX, agY)   #self.resize(1806, 1035)
        self.setStyleSheet("background-color: #080e13;")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBoxMenu = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxMenu.setGeometry(QtCore.QRect(sgX*2, sgY, sgX*196, sgY*8))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))


        # Top Menu
        self.groupBoxMenu.setFont(font)
        self.groupBoxMenu.setStyleSheet("background-color: #181e23; border: 0px solid #000;")
        self.groupBoxMenu.setTitle("")
        self.groupBoxMenu.setObjectName("groupBoxMenu")
        self.pushButtonBookOut = QtWidgets.QPushButton(self.groupBoxMenu, clicked = lambda: self.openWindowBookOut())
        self.pushButtonBookOut.setGeometry(QtCore.QRect(sgX, sgY, sgX*21, sgY*6))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonBookOut.setFont(font)
        self.pushButtonBookOut.setStyleSheet("border: 4px solid #aa3333; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonBookOut.setObjectName("pushButtonBookOut")
        self.pushButtonReturn = QtWidgets.QPushButton(self.groupBoxMenu, clicked = lambda: self.openWindowReturn())
        self.pushButtonReturn.setGeometry(QtCore.QRect(sgX*24, sgY, sgX*21, sgY*6))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonReturn.setFont(font)
        self.pushButtonReturn.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonReturn.setObjectName("pushButtonReturn")
        self.pushButtonBookedOut = QtWidgets.QPushButton(self.groupBoxMenu, clicked = lambda: self.openWindowBookedOut())
        self.pushButtonBookedOut.setGeometry(QtCore.QRect(sgX*76, sgY, sgX*21, sgY*6))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonBookedOut.setFont(font)
        self.pushButtonBookedOut.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonBookedOut.setObjectName("pushButtonBookedOut")
        self.pushButtonHistory = QtWidgets.QPushButton(self.groupBoxMenu, clicked = lambda: self.openWindowHistory())
        self.pushButtonHistory.setGeometry(QtCore.QRect(sgX*99, sgY, sgX*21, sgY*6))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonHistory.setFont(font)
        self.pushButtonHistory.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonHistory.setObjectName("pushButtonHistory")
        self.pushButtonItems = QtWidgets.QPushButton(self.groupBoxMenu, clicked = lambda: self.openWindowAllItems())
        self.pushButtonItems.setGeometry(QtCore.QRect(sgX*151, sgY, sgX*21, sgY*6))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonItems.setFont(font)
        self.pushButtonItems.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.setObjectName("pushButtonItems")
        self.pushButtonUsers = QtWidgets.QPushButton(self.groupBoxMenu, clicked = lambda: self.openWindowAllUsers())
        self.pushButtonUsers.setGeometry(QtCore.QRect(sgX*174, sgY, sgX*21, sgY*6))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonUsers.setFont(font)
        self.pushButtonUsers.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonUsers.setObjectName("pushButtonUsers")


        # Book Out
        self.groupBoxBO = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxBO.setGeometry(QtCore.QRect(sgX*2, sgY*10, sgX*196, sgY*90))
        self.groupBoxBO.setStyleSheet("background-color: #181e23; border: 0px solid #000;")
        self.groupBoxBO.setTitle("")
        self.groupBoxBO.setObjectName("groupBoxBO")

        self.tableWidgetBO = QtWidgets.QTableWidget(self.groupBoxBO)
        self.tableWidgetBO.setGeometry(QtCore.QRect(sgX*20, sgY*9, sgX*174, sgY*77))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetBO.sizePolicy().hasHeightForWidth())


        self.tableWidgetBO.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.tableWidgetBO.setFont(font)
        self.tableWidgetBO.setAutoFillBackground(False)
        
        styleSheet = """
QTableView {
    background-color: #181e23;
    alternate-background-color: #282e33;
    border: 1px solid black;
    gridline-color: black;
    font-size: """ + str(int(sgX*2.5)) + """px;
    color: white;
}

QHeaderView {
    background-color: #444;
    color: #444
}

QHeaderView::section {
    background-color: #444;
    color: white;
    font-size: """ + str(int(sgX*2)) + """px;
    padding: 2px;
}

QTableCornerButton::section {
    background-color: #444;
}
"""
        self.tableWidgetBO.setStyleSheet(styleSheet)
        self.tableWidgetBO.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidgetBO.setLineWidth(1)
        self.tableWidgetBO.setMidLineWidth(0)
        self.tableWidgetBO.setAlternatingRowColors(True)
        self.tableWidgetBO.setShowGrid(True)
        self.tableWidgetBO.setRowCount(0)
        self.tableWidgetBO.setObjectName("tableWidgetBO")
        self.tableWidgetBO.setColumnCount(6)
        self.tableWidgetBO.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidgetBO.setHorizontalHeaderItem(0, item)
        self.tableWidgetBO.setColumnWidth(0, sgX*12)    # longTerm
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QtGui.QColor("black"))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidgetBO.setHorizontalHeaderItem(1, item)
        self.tableWidgetBO.setColumnWidth(1, sgX*14)    # itemID
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QtGui.QColor("white"))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidgetBO.setHorizontalHeaderItem(2, item)
        self.tableWidgetBO.setColumnWidth(2, sgX*68)    # itemName
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidgetBO.setHorizontalHeaderItem(3, item)
        self.tableWidgetBO.setColumnWidth(3, sgX*24)    # itemMake
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidgetBO.setHorizontalHeaderItem(4, item)
        self.tableWidgetBO.setColumnWidth(4, sgX*28)    # itemModel
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidgetBO.setHorizontalHeaderItem(5, item)
        self.tableWidgetBO.setColumnWidth(5, sgX*28)    # itemSerial
        self.tableWidgetBO.verticalHeader().setVisible(True)
        self.tableWidgetBO.verticalHeader().setHighlightSections(True)

        self.pushButtonBOClear = QtWidgets.QPushButton(self.groupBoxBO, clicked = lambda: self.clearAll())
        self.pushButtonBOClear.setGeometry(QtCore.QRect(sgX*2, sgY*30, sgX*16, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonBOClear.setFont(font)
        self.pushButtonBOClear.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonBOClear.setObjectName("pushButtonBOClear")
        self.pushButtonBOClearLast = QtWidgets.QPushButton(self.groupBoxBO, clicked = lambda: self.clearPrev())
        self.pushButtonBOClearLast.setGeometry(QtCore.QRect(sgX*2, sgY*23, sgX*16, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonBOClearLast.setFont(font)
        self.pushButtonBOClearLast.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonBOClearLast.setObjectName("pushButtonBOClearLast")
        self.pushButtonBOCancel = QtWidgets.QPushButton(self.groupBoxBO, clicked = lambda: self.cancelBO())
        self.pushButtonBOCancel.setGeometry(QtCore.QRect(sgX*2, sgY*70, sgX*16, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonBOCancel.setFont(font)
        self.pushButtonBOCancel.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonBOCancel.setObjectName("pushButtonBOCancel")
        self.pushButtonBOSubmit = QtWidgets.QPushButton(self.groupBoxBO, clicked = lambda: self.processOutgoing())
        self.pushButtonBOSubmit.setGeometry(QtCore.QRect(sgX*2, sgY*79, sgX*16, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonBOSubmit.setFont(font)
        self.pushButtonBOSubmit.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonBOSubmit.setObjectName("pushButtonBOSubmit")

        self.labelBOUserID = QtWidgets.QLabel(self.groupBoxBO)
        self.labelBOUserID.setGeometry(QtCore.QRect(sgX*22, 0, sgX*16, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelBOUserID.setFont(font)
        self.labelBOUserID.setAutoFillBackground(False)
        self.labelBOUserID.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelBOUserID.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelBOUserID.setObjectName("labelBOUserID")
        self.lineEditBOUserID = QtWidgets.QLineEdit(self.groupBoxBO)
        self.lineEditBOUserID.returnPressed.connect(lambda: self.getUserFromID(0))
        self.lineEditBOUserID.setGeometry(QtCore.QRect(sgX*21, sgY*3, sgX*28, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.lineEditBOUserID.setFont(font)
        self.lineEditBOUserID.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px; color: #ffffff;")
        self.lineEditBOUserID.setText("")
        self.lineEditBOUserID.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditBOUserID.setObjectName("lineEditBOUserID")

        self.labelBOUserName = QtWidgets.QLabel(self.groupBoxBO)
        self.labelBOUserName.setGeometry(QtCore.QRect(sgX*77, 0, sgX*16, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelBOUserName.setFont(font)
        self.labelBOUserName.setAutoFillBackground(False)
        self.labelBOUserName.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelBOUserName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelBOUserName.setObjectName("labelBOUserName")
        self.lineEditBOUserName = QtWidgets.QLineEdit(self.groupBoxBO)
        self.lineEditBOUserName.returnPressed.connect(lambda: self.getUserFromName(-1))
        self.lineEditBOUserName.setGeometry(QtCore.QRect(sgX*76, sgY*3, sgX*44, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.lineEditBOUserName.setFont(font)
        self.lineEditBOUserName.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px; color: #ffffff;")
        self.lineEditBOUserName.setText("")
        self.lineEditBOUserName.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditBOUserName.setObjectName("lineEditBOUserName")
        self.listWidgetBOUserName = QtWidgets.QListWidget(self.groupBoxBO)
        self.listWidgetBOUserName.itemClicked.connect(self.listItemBOClicked)
        self.listWidgetBOUserName.setGeometry(QtCore.QRect(sgX*77, sgY*7, sgX*42, sgY*35))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.listWidgetBOUserName.setFont(font)
        self.listWidgetBOUserName.setStyleSheet("color: white; border: 1px solid grey;")
        self.listWidgetBOUserName.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.listWidgetBOUserName.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.listWidgetBOUserName.setObjectName("listWidgetBOUserName")
        self.listWidgetBOUserName.hide()

        self.labelBOUserEmail = QtWidgets.QLabel(self.groupBoxBO)
        self.labelBOUserEmail.setGeometry(QtCore.QRect(sgX*152, 0, sgX*16, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelBOUserEmail.setFont(font)
        self.labelBOUserEmail.setAutoFillBackground(False)
        self.labelBOUserEmail.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelBOUserEmail.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelBOUserEmail.setObjectName("labelBOUserEmail")
        self.lineEditBOUserEmail = QtWidgets.QLineEdit(self.groupBoxBO)
        self.lineEditBOUserEmail.returnPressed.connect(lambda: self.getUserFromEmail(-1))
        self.lineEditBOUserEmail.setGeometry(QtCore.QRect(sgX*151, sgY*3, sgX*44, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.lineEditBOUserEmail.setFont(font)
        self.lineEditBOUserEmail.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px; color: #ffffff;")
        self.lineEditBOUserEmail.setText("")
        self.lineEditBOUserEmail.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditBOUserEmail.setObjectName("lineEditBOUserEmail")
        self.listWidgetBOUserEmail = QtWidgets.QListWidget(self.groupBoxBO)
        self.listWidgetBOUserEmail.itemClicked.connect(self.listItemEmailBOClicked)
        self.listWidgetBOUserEmail.setGeometry(QtCore.QRect(sgX*152, sgY*7, sgX*42, sgY*35))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.listWidgetBOUserEmail.setFont(font)
        self.listWidgetBOUserEmail.setStyleSheet("color: white; border: 1px solid grey;")
        self.listWidgetBOUserEmail.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.listWidgetBOUserEmail.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.listWidgetBOUserEmail.setObjectName("listWidgetBOUserEmail")
        self.listWidgetBOUserEmail.hide()

        self.labelBOItemID = QtWidgets.QLabel(self.groupBoxBO)
        self.labelBOItemID.setGeometry(QtCore.QRect(sgX*3, sgY*9, sgX*16, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelBOItemID.setFont(font)
        self.labelBOItemID.setAutoFillBackground(False)
        self.labelBOItemID.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelBOItemID.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelBOItemID.setObjectName("labelBOItemID")
        self.lineEditBOItemID = QtWidgets.QLineEdit(self.groupBoxBO)
        self.lineEditBOItemID.returnPressed.connect(self.keyItemID)
        self.lineEditBOItemID.setGeometry(QtCore.QRect(sgX*2, sgY*12, sgX*16, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.lineEditBOItemID.setFont(font)
        self.lineEditBOItemID.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px; color: #ffffff;")
        self.lineEditBOItemID.setText("")
        self.lineEditBOItemID.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditBOItemID.setObjectName("lineEditBOItemID")
        self.lineEditBOMessage = QtWidgets.QLineEdit(self.groupBoxBO)
        self.lineEditBOMessage.setReadOnly(True)
        self.lineEditBOMessage.setGeometry(QtCore.QRect(0, sgY*3, sgX*20, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.lineEditBOMessage.setFont(font)
        self.lineEditBOMessage.setStyleSheet("color: #ffffff;")
        self.lineEditBOMessage.setText("")
        self.lineEditBOMessage.setFrame(False)
        self.lineEditBOMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditBOMessage.setObjectName("lineEditBOMessage")

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, sgX*180, sgY*2))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)


        # Return
        self.groupBoxRe = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxRe.setGeometry(QtCore.QRect(sgX*2, sgY*10, sgX*196, sgY*90))
        self.groupBoxRe.setStyleSheet("background-color: #181e23; border: 0px solid #000;")
        self.groupBoxRe.setTitle("")
        self.groupBoxRe.setObjectName("groupBoxRe")
        self.tableWidgetRe = QtWidgets.QTableWidget(self.groupBoxRe)
        self.tableWidgetRe.setGeometry(QtCore.QRect(sgX*20, sgY*9, sgX*174, sgY*77))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetRe.sizePolicy().hasHeightForWidth())
        self.tableWidgetRe.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.tableWidgetRe.setFont(font)
        self.tableWidgetRe.setAutoFillBackground(False)
        self.tableWidgetRe.setStyleSheet(styleSheet)
        self.tableWidgetRe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidgetRe.setLineWidth(1)
        self.tableWidgetRe.setMidLineWidth(0)
        self.tableWidgetRe.setAlternatingRowColors(True)
        self.tableWidgetRe.setShowGrid(True)
        self.tableWidgetRe.setRowCount(0)
        self.tableWidgetRe.setObjectName("tableWidgetRe")
        self.tableWidgetRe.setColumnCount(5)
        self.tableWidgetRe.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetRe.setHorizontalHeaderItem(0, item)
        self.tableWidgetRe.setColumnWidth(0, sgX*18)    # itemID
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetRe.setHorizontalHeaderItem(1, item)
        self.tableWidgetRe.setColumnWidth(1, sgX*60)    # itemName
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetRe.setHorizontalHeaderItem(2, item)
        self.tableWidgetRe.setColumnWidth(2, sgX*22)    # userID
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetRe.setHorizontalHeaderItem(3, item)
        self.tableWidgetRe.setColumnWidth(3, sgX*36)    # userName
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetRe.setHorizontalHeaderItem(4, item)
        self.tableWidgetRe.setColumnWidth(4, sgX*38)    # userEmail
        self.tableWidgetRe.verticalHeader().setVisible(True)
        self.tableWidgetRe.verticalHeader().setHighlightSections(True)
        self.lineEditReItemID = QtWidgets.QLineEdit(self.groupBoxRe)
        self.lineEditReItemID.returnPressed.connect(lambda: self.returnItems())
        self.lineEditReItemID.setGeometry(QtCore.QRect(sgX*2, sgY*12, sgX*16, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.lineEditReItemID.setFont(font)
        self.lineEditReItemID.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px; color: #ffffff;")
        self.lineEditReItemID.setText("")
        self.lineEditReItemID.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditReItemID.setObjectName("lineEditReItemID")
        self.labelReItemID = QtWidgets.QLabel(self.groupBoxRe)
        self.labelReItemID.setGeometry(QtCore.QRect(sgX*3, sgY*9, sgX*16, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelReItemID.setFont(font)
        self.labelReItemID.setAutoFillBackground(False)
        self.labelReItemID.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelReItemID.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelReItemID.setObjectName("labelReItemID")
        self.lineEditReMessage = QtWidgets.QLineEdit(self.groupBoxRe)
        self.lineEditReMessage.setReadOnly(True)
        self.lineEditReMessage.setGeometry(QtCore.QRect(0, sgY*3, sgX*20, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.lineEditReMessage.setFont(font)
        self.lineEditReMessage.setStyleSheet("color: #ffffff;")
        self.lineEditReMessage.setText("")
        self.lineEditReMessage.setFrame(False)
        self.lineEditReMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditReMessage.setObjectName("lineEditReMessage")


        # Booked Out
        self.groupBoxBkdO = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxBkdO.setGeometry(QtCore.QRect(sgX*2, sgY*10, sgX*196, sgY*90))
        self.groupBoxBkdO.setStyleSheet("background-color: #181e23; border: 0px solid #000;")
        self.groupBoxBkdO.setTitle("")
        self.groupBoxBkdO.setObjectName("groupBoxBkdO")
        self.labelBkdOShowLong = QtWidgets.QLabel(self.groupBoxBkdO)
        self.labelBkdOShowLong.setGeometry(QtCore.QRect(sgX*2, sgY*9, sgX*20, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(14)
        self.labelBkdOShowLong.setFont(font)
        self.labelBkdOShowLong.setAutoFillBackground(False)
        self.labelBkdOShowLong.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelBkdOShowLong.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelBkdOShowLong.setObjectName("labelBkdOShowLong")
        self.groupBoxBkdOCheck = QtWidgets.QGroupBox(self.groupBoxBkdO)
        self.groupBoxBkdOCheck.setGeometry(QtCore.QRect(sgX*9, sgY*14, sgX*5, sgY*5))
        self.groupBoxBkdOCheck.setStyleSheet("background-color: #666666; border-radius: 10px; color: #ffffff;")
        self.groupBoxBkdOCheck.setTitle("")
        self.groupBoxBkdOCheck.setObjectName("groupBoxBkdOCheck")
        self.checkBoxBkdO = QtWidgets.QCheckBox(self.groupBoxBkdOCheck, clicked = lambda: self.showLongTerm())
        self.checkBoxBkdO.setGeometry(QtCore.QRect(13,13,20,20))#sgX*9, sgY*14, sgX*3, sgY*3))
        self.checkBoxBkdO.setStyleSheet("QCheckBox::indicator { margin-left:50%; margin-right:50%; }")
        #self.checkBoxBkdO.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        #font = QtGui.QFont()
        #font.setFamily("Helvetica Neue")
        #font.setPointSize(int(sgX*5))
        #self.checkBoxBkdO.setFont(font)
        #self.checkBoxBkdO.setText("")
        #self.checkBoxBkdO.setIconSize(QtCore.QSize(32, 32))
        self.checkBoxBkdO.setChecked(False)
        self.checkBoxBkdO.setObjectName("checkBoxBkdO")
        self.tableWidgetBkdO = QtWidgets.QTableWidget(self.groupBoxBkdO)
        self.tableWidgetBkdO.cellChanged.connect(self.onCellChanged)
        self.tableWidgetBkdO.setGeometry(QtCore.QRect(sgX*20, sgY*9, sgX*174, sgY*77))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetBkdO.sizePolicy().hasHeightForWidth())
        self.tableWidgetBkdO.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.tableWidgetBkdO.setFont(font)
        self.tableWidgetBkdO.setAutoFillBackground(False)
        self.tableWidgetBkdO.setStyleSheet(styleSheet)
        self.tableWidgetBkdO.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidgetBkdO.setLineWidth(1)
        self.tableWidgetBkdO.setMidLineWidth(0)
        self.tableWidgetBkdO.setAlternatingRowColors(True)
        self.tableWidgetBkdO.setShowGrid(True)
        self.tableWidgetBkdO.setRowCount(0)
        self.tableWidgetBkdO.setObjectName("tableWidgetBkdO")
        self.tableWidgetBkdO.setColumnCount(6)
        self.tableWidgetBkdO.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetBkdO.setHorizontalHeaderItem(0, item)     # Long-Term
        self.tableWidgetBkdO.setColumnWidth(0, sgX*12)               
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetBkdO.setHorizontalHeaderItem(1, item)     # itemID
        self.tableWidgetBkdO.setColumnWidth(1, sgX*14)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetBkdO.setHorizontalHeaderItem(2, item)     # itemName
        self.tableWidgetBkdO.setColumnWidth(2, sgX*60)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetBkdO.setHorizontalHeaderItem(3, item)     # userName
        self.tableWidgetBkdO.setColumnWidth(3, sgX*26)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetBkdO.setHorizontalHeaderItem(4, item)     # userEmail
        self.tableWidgetBkdO.setColumnWidth(4, sgX*30)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetBkdO.setHorizontalHeaderItem(5, item)     # dateOut
        self.tableWidgetBkdO.setColumnWidth(5, sgX*32)
        self.tableWidgetBkdO.verticalHeader().setVisible(True)
        self.tableWidgetBkdO.verticalHeader().setHighlightSections(True)
        self.pushButtonBkdOExport = QtWidgets.QPushButton(self.groupBoxBkdO, clicked = lambda: self.exportBooked())
        self.pushButtonBkdOExport.setGeometry(QtCore.QRect(sgX*2, sgY*79, sgX*16, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonBkdOExport.setFont(font)
        self.pushButtonBkdOExport.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonBkdOExport.setObjectName("pushButtonBkdOExport")


        # History
        self.groupBoxHist = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxHist.setGeometry(QtCore.QRect(sgX*2, sgY*10, sgX*196, sgY*90))
        self.groupBoxHist.setStyleSheet("background-color: #181e23; border: 0px solid #000;")
        self.groupBoxHist.setTitle("")
        self.groupBoxHist.setObjectName("groupBoxHist")
        self.tableWidgetHist = QtWidgets.QTableWidget(self.groupBoxHist)
        self.tableWidgetHist.setGeometry(QtCore.QRect(sgX*20, sgY*9, sgX*174, sgY*77))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetHist.sizePolicy().hasHeightForWidth())
        self.listWidgetHistUserName = QtWidgets.QListWidget(self.groupBoxHist)
        self.listWidgetHistUserName.itemClicked.connect(self.listItemHistClicked)
        self.listWidgetHistUserName.setGeometry(QtCore.QRect(sgX*77, sgY*7, sgX*42, sgY*35))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.listWidgetHistUserName.setFont(font)
        self.listWidgetHistUserName.setStyleSheet("color: white; border: 1px solid grey;")
        self.listWidgetHistUserName.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.listWidgetHistUserName.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.listWidgetHistUserName.setObjectName("listWidgetHistUserName")
        self.listWidgetHistUserName.hide()
        self.tableWidgetHist.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.tableWidgetHist.setFont(font)
        self.tableWidgetHist.setAutoFillBackground(False)
        self.tableWidgetHist.setStyleSheet(styleSheet)
        self.tableWidgetHist.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidgetHist.setLineWidth(1)
        self.tableWidgetHist.setMidLineWidth(0)
        self.tableWidgetHist.setAlternatingRowColors(True)
        self.tableWidgetHist.setShowGrid(True)
        self.tableWidgetHist.setRowCount(0)
        self.tableWidgetHist.setObjectName("tableWidgetHist")
        self.tableWidgetHist.setColumnCount(6)
        self.tableWidgetHist.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetHist.setHorizontalHeaderItem(0, item)
        self.tableWidgetHist.setColumnWidth(0, sgX*14)  # itemID
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetHist.setHorizontalHeaderItem(1, item)
        self.tableWidgetHist.setColumnWidth(1, sgX*69) # itemName
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetHist.setHorizontalHeaderItem(2, item)
        self.tableWidgetHist.setColumnWidth(2, sgX*26) # userName
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetHist.setHorizontalHeaderItem(3, item)
        self.tableWidgetHist.setColumnWidth(3, sgX*26) # userEmail
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetHist.setHorizontalHeaderItem(4, item)
        self.tableWidgetHist.setColumnWidth(4, sgX*18) # dateOUT
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetHist.setHorizontalHeaderItem(5, item)
        self.tableWidgetHist.setColumnWidth(5, sgX*18) # dateIN
        self.tableWidgetHist.verticalHeader().setVisible(True)
        self.tableWidgetHist.verticalHeader().setHighlightSections(True)
        self.pushButtonHistClear = QtWidgets.QPushButton(self.groupBoxHist, clicked = lambda: self.clearHist())
        self.pushButtonHistClear.setGeometry(QtCore.QRect(sgX*2, sgY*23, sgX*16, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonHistClear.setFont(font)
        self.pushButtonHistClear.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonHistClear.setObjectName("pushButtonHistClear")
        self.pushButtonHistExport = QtWidgets.QPushButton(self.groupBoxHist, clicked = lambda: self.exportHistory())
        self.pushButtonHistExport.setGeometry(QtCore.QRect(sgX*2, sgY*79, sgX*16, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonHistExport.setFont(font)
        self.pushButtonHistExport.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonHistExport.setObjectName("pushButtonHistExport")
        self.lineEditHistUserID = QtWidgets.QLineEdit(self.groupBoxHist)
        self.lineEditHistUserID.returnPressed.connect(lambda: self.getUserFromID(0))
        self.lineEditHistUserID.setGeometry(QtCore.QRect(sgX*21, sgY*3, sgX*28, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.lineEditHistUserID.setFont(font)
        self.lineEditHistUserID.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px; color: #ffffff;")
        self.lineEditHistUserID.setText("")
        self.lineEditHistUserID.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditHistUserID.setObjectName("lineEditHistUserID")
        self.labelHistUserID = QtWidgets.QLabel(self.groupBoxHist)
        self.labelHistUserID.setGeometry(QtCore.QRect(sgX*22, 0, sgX*16, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelHistUserID.setFont(font)
        self.labelHistUserID.setAutoFillBackground(False)
        self.labelHistUserID.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelHistUserID.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelHistUserID.setObjectName("labelHistUserID")
        self.lineEditHistUserName = QtWidgets.QLineEdit(self.groupBoxHist)
        self.lineEditHistUserName.returnPressed.connect(lambda: self.getUserFromName(-1))
        self.lineEditHistUserName.setGeometry(QtCore.QRect(sgX*76, sgY*3, sgX*44, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.lineEditHistUserName.setFont(font)
        self.lineEditHistUserName.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px; color: #ffffff;")
        self.lineEditHistUserName.setText("")
        self.lineEditHistUserName.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditHistUserName.setObjectName("lineEditHistUserName")
        self.labelHistUserName = QtWidgets.QLabel(self.groupBoxHist)
        self.labelHistUserName.setGeometry(QtCore.QRect(sgX*77, 0, sgX*16, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelHistUserName.setFont(font)
        self.labelHistUserName.setAutoFillBackground(False)
        self.labelHistUserName.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelHistUserName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelHistUserName.setObjectName("labelHistUserName")
        self.lineEditHistUserEmail = QtWidgets.QLineEdit(self.groupBoxHist)
        self.lineEditHistUserEmail.returnPressed.connect(lambda: self.getUserFromEmail(-1))
        self.lineEditHistUserEmail.setGeometry(QtCore.QRect(sgX*151, sgY*3, sgX*44, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.lineEditHistUserEmail.setFont(font)
        self.lineEditHistUserEmail.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px; color: #ffffff;")
        self.lineEditHistUserEmail.setText("")
        self.lineEditHistUserEmail.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditHistUserEmail.setObjectName("lineEditHistUserEmail")
        self.labelHistUserEmail = QtWidgets.QLabel(self.groupBoxHist)
        self.labelHistUserEmail.setGeometry(QtCore.QRect(sgX*152, 0, sgX*16, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelHistUserEmail.setFont(font)
        self.labelHistUserEmail.setAutoFillBackground(False)
        self.labelHistUserEmail.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelHistUserEmail.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelHistUserEmail.setObjectName("labelHistUserEmail")
        self.listWidgetHistEmail = QtWidgets.QListWidget(self.groupBoxHist)
        self.listWidgetHistEmail.itemClicked.connect(self.listItemEmailHistClicked)
        self.listWidgetHistEmail.setGeometry(QtCore.QRect(sgX*131, sgY*7, sgX*42, sgY*35))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.listWidgetHistEmail.setFont(font)
        self.listWidgetHistEmail.setStyleSheet("color: white; border: 1px solid grey;")
        self.listWidgetHistEmail.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.listWidgetHistEmail.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.listWidgetHistEmail.setObjectName("listWidgetHistEmail")
        self.listWidgetHistEmail.hide()
        self.lineEditHistItemID = QtWidgets.QLineEdit(self.groupBoxHist)
        self.lineEditHistItemID.returnPressed.connect(lambda: self.getItemFromID())
        self.lineEditHistItemID.setGeometry(QtCore.QRect(sgX*2, sgY*12, sgX*16, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.lineEditHistItemID.setFont(font)
        self.lineEditHistItemID.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px; color: #ffffff;")
        self.lineEditHistItemID.setText("")
        self.lineEditHistItemID.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditHistItemID.setObjectName("lineEditHistItemID")
        self.labelHistItemID = QtWidgets.QLabel(self.groupBoxHist)
        self.labelHistItemID.setGeometry(QtCore.QRect(sgX*3, sgY*9, sgX*16, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelHistItemID.setFont(font)
        self.labelHistItemID.setAutoFillBackground(False)
        self.labelHistItemID.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelHistItemID.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelHistItemID.setObjectName("labelHistItemID")
        self.lineEditHistMessage = QtWidgets.QLineEdit(self.groupBoxHist)
        self.lineEditHistMessage.setReadOnly(True)
        self.lineEditHistMessage.setGeometry(QtCore.QRect(0, sgY*3, sgX*20, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.lineEditHistMessage.setFont(font)
        self.lineEditHistMessage.setStyleSheet("color: #ffffff;")
        self.lineEditHistMessage.setText("")
        self.lineEditHistMessage.setFrame(False)
        self.lineEditHistMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditHistMessage.setObjectName("lineEditHistMessage")
        
        currentDate = QtCore.QDate.currentDate()
        self.labelHistDateFrom = QtWidgets.QLabel(self.groupBoxHist)
        self.labelHistDateFrom.setGeometry(QtCore.QRect(sgX*2, sgY*36, sgX*16, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelHistDateFrom.setFont(font)
        self.labelHistDateFrom.setAutoFillBackground(False)
        self.labelHistDateFrom.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelHistDateFrom.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelHistDateFrom.setObjectName("labelHistDateFrom")
        self.dateEditFrom = QtWidgets.QDateEdit(self.groupBoxHist, calendarPopup=True)
        self.dateEditFrom.setGeometry(QtCore.QRect(sgX, sgY*39, sgX*18, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*1.8))
        self.dateEditFrom.setFont(font)
        self.dateEditFrom.setStyleSheet("color: white; background-color: #444;border: 2px solid grey; border-radius: 5px;")
        self.dateEditFrom.setObjectName("dateEditFrom")
        self.dateEditFrom.setDate(currentDate.addDays(-28))
        self.dateEditFrom.dateChanged.connect(lambda: self.refreshHistory())
        self.labelHistDateTo = QtWidgets.QLabel(self.groupBoxHist)
        self.labelHistDateTo.setGeometry(QtCore.QRect(sgX*2, sgY*55, sgX*16, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelHistDateTo.setFont(font)
        self.labelHistDateTo.setAutoFillBackground(False)
        self.labelHistDateTo.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelHistDateTo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelHistDateTo.setObjectName("labelHistDateTo")
        self.dateEditTo = QtWidgets.QDateEdit(self.groupBoxHist, calendarPopup=True)
        self.dateEditTo.setGeometry(QtCore.QRect(sgX, sgY*58, sgX*18, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*1.8))
        self.dateEditTo.setFont(font)
        self.dateEditTo.setStyleSheet("color: white; background-color: #444;border: 2px solid grey; border-radius: 5px;")
        self.dateEditTo.setObjectName("dateEditTo")
        self.dateEditTo.setDate(currentDate)
        self.dateEditTo.dateChanged.connect(lambda: self.refreshHistory())
        self.pushButtonHistResetDate = QtWidgets.QPushButton(self.groupBoxHist, clicked = lambda: self.resetDateHist())
        self.pushButtonHistResetDate.setGeometry(QtCore.QRect(sgX*2, sgY*48, sgX*16, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonHistResetDate.setFont(font)
        self.pushButtonHistResetDate.setStyleSheet("border: 4px solid grey; border-radius: 10px;background-color: #804040; color: #ffffff;")
        self.pushButtonHistResetDate.setObjectName("pushButtonHistResetDate")


        # Items
        self.groupBoxAllItemsOuter = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxAllItemsOuter.setGeometry(QtCore.QRect(sgX*2, sgY*10, sgX*196, sgY*90))
        self.groupBoxAllItemsOuter.setStyleSheet("background-color: #181e23; border: 0px solid #000;")
        self.groupBoxAllItemsOuter.setTitle("")
        self.groupBoxAllItemsOuter.setObjectName("groupBoxAllItemsOuter")

        # All Items
        self.groupBoxAllItems = QtWidgets.QGroupBox(self.groupBoxAllItemsOuter)
        self.groupBoxAllItems.setGeometry(QtCore.QRect(0, 0, sgX*196, sgY*90))
        self.groupBoxAllItems.setStyleSheet("background-color: #1c2428")
        self.groupBoxAllItems.setTitle("")
        self.groupBoxAllItems.setObjectName("groupBoxAllItems")

        self.pushButtonAllItemsAllItems = QtWidgets.QPushButton(self.groupBoxMenu, clicked = lambda: self.openWindowAllItems())
        self.pushButtonAllItemsAllItems.setGeometry(QtCore.QRect(sgX*151, sgY, sgX*10, sgY*6))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.pushButtonAllItemsAllItems.setFont(font)
        self.pushButtonAllItemsAllItems.setStyleSheet("border: 4px solid #aa3333; background-color: #408040; border-radius: 10px;color: #ffffff;")
        self.pushButtonAllItemsAllItems.setObjectName("pushButtonAllItemsAllItems")
        self.pushButtonAllItemsAllItems.hide()
        self.pushButtonAllItemsAddItem = QtWidgets.QPushButton(self.groupBoxMenu, clicked = lambda: self.openWindowAddItem())
        self.pushButtonAllItemsAddItem.setGeometry(QtCore.QRect(sgX*162, sgY, sgX*10, sgY*6))

        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.pushButtonAllItemsAddItem.setFont(font)
        self.pushButtonAllItemsAddItem.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px;color: #ffffff;")
        self.pushButtonAllItemsAddItem.setObjectName("pushButtonAllItemsAddItem")
        self.pushButtonAllItemsAddItem.hide()

        self.labelAllItemsItemID = QtWidgets.QLabel(self.groupBoxAllItems)
        self.labelAllItemsItemID.setGeometry(QtCore.QRect(sgX*22, 0, sgX*16, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelAllItemsItemID.setFont(font)
        self.labelAllItemsItemID.setAutoFillBackground(False)
        self.labelAllItemsItemID.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAllItemsItemID.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAllItemsItemID.setObjectName("labelAllItemsItemID")
        self.lineEditAllItemsItemID = QtWidgets.QLineEdit(self.groupBoxAllItems)
        self.lineEditAllItemsItemID.returnPressed.connect(lambda: self.populateAllItems())
        self.lineEditAllItemsItemID.setGeometry(QtCore.QRect(sgX*21, sgY*3, sgX*28, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.lineEditAllItemsItemID.setFont(font)
        self.lineEditAllItemsItemID.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px;color: #ffffff;")
        self.lineEditAllItemsItemID.setText("")
        self.lineEditAllItemsItemID.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAllItemsItemID.setObjectName("lineEditAllItemsItemID")
        self.labelAllItemsItemSearch = QtWidgets.QLabel(self.groupBoxAllItems)
        self.labelAllItemsItemSearch.setGeometry(QtCore.QRect(sgX*77, 0, sgX*16, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelAllItemsItemSearch.setFont(font)
        self.labelAllItemsItemSearch.setAutoFillBackground(False)
        self.labelAllItemsItemSearch.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAllItemsItemSearch.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAllItemsItemSearch.setObjectName("labelAllItemsItemSearch")
        self.lineEditAllItemSearch = QtWidgets.QLineEdit(self.groupBoxAllItems)
        self.lineEditAllItemSearch.returnPressed.connect(lambda: self.populateAllItems())
        self.lineEditAllItemSearch.setGeometry(QtCore.QRect(sgX*76, sgY*3, sgX*44, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.lineEditAllItemSearch.setFont(font)
        self.lineEditAllItemSearch.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px;color: #ffffff;")
        self.lineEditAllItemSearch.setText("")
        self.lineEditAllItemSearch.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAllItemSearch.setObjectName("lineEditAllItemSearch")

        self.tableWidgetAllItems = QtWidgets.QTableWidget(self.groupBoxAllItems)
        self.tableWidgetAllItems.setGeometry(QtCore.QRect(sgX*20, sgY*9, sgX*174, sgY*77))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetAllItems.sizePolicy().hasHeightForWidth())
        self.tableWidgetAllItems.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.tableWidgetAllItems.setFont(font)
        self.tableWidgetAllItems.setAutoFillBackground(False)
        self.tableWidgetAllItems.setStyleSheet(styleSheet)
        self.tableWidgetAllItems.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidgetAllItems.setLineWidth(1)
        self.tableWidgetAllItems.setMidLineWidth(0)
        self.tableWidgetAllItems.setAlternatingRowColors(True)
        self.tableWidgetAllItems.setShowGrid(True)
        self.tableWidgetAllItems.setRowCount(0)
        self.tableWidgetAllItems.setObjectName("tableWidgetAllItems")
        self.tableWidgetAllItems.setColumnCount(5)
        self.tableWidgetAllItems.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetAllItems.setHorizontalHeaderItem(0, item)
        self.tableWidgetAllItems.setColumnWidth(0, sgX*14)    # itemID
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidgetAllItems.setHorizontalHeaderItem(1, item)
        self.tableWidgetAllItems.setColumnWidth(1, sgX*70)    # itemName
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetAllItems.setHorizontalHeaderItem(2, item)
        self.tableWidgetAllItems.setColumnWidth(2, sgX*26)    # itemMake
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetAllItems.setHorizontalHeaderItem(3, item)
        self.tableWidgetAllItems.setColumnWidth(3, sgX*26)    # itemModel
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetAllItems.setHorizontalHeaderItem(4, item)
        self.tableWidgetAllItems.setColumnWidth(4, sgX*26)    # itemSerial
        self.tableWidgetAllItems.verticalHeader().setVisible(True)
        self.tableWidgetAllItems.verticalHeader().setHighlightSections(True)
        
        self.pushButtonAllItemsClear = QtWidgets.QPushButton(self.groupBoxAllItems)
        self.pushButtonAllItemsClear = QtWidgets.QPushButton(self.groupBoxAllItems, clicked = lambda: self.clearAllItems())
        self.pushButtonAllItemsClear.setGeometry(QtCore.QRect(sgX*2, sgY*23, sgX*16, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonAllItemsClear.setFont(font)
        self.pushButtonAllItemsClear.setStyleSheet("border: 4px solid grey; border-radius: 10px;background-color: #804040; color: #ffffff;")
        self.pushButtonAllItemsClear.setObjectName("pushButtonAllItemsClear")
        self.pushButtonAllItemsExport = QtWidgets.QPushButton(self.groupBoxAllItems)
        self.pushButtonAllItemsExport = QtWidgets.QPushButton(self.groupBoxAllItems, clicked = lambda: self.exportItems())
        self.pushButtonAllItemsExport.setGeometry(QtCore.QRect(sgX*2, sgY*79, sgX*16, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonAllItemsExport.setFont(font)
        self.pushButtonAllItemsExport.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px;color: #ffffff;")
        self.pushButtonAllItemsExport.setObjectName("pushButtonAllItemsExport")
        self.lineEditAllItemsMessage = QtWidgets.QLineEdit(self.groupBoxAllItems)
        self.lineEditAllItemsMessage.setGeometry(QtCore.QRect(0, sgY*3, sgX*20, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.lineEditAllItemsMessage.setFont(font)
        self.lineEditAllItemsMessage.setStyleSheet("color: #ffffff;")
        self.lineEditAllItemsMessage.setText("")
        self.lineEditAllItemsMessage.setFrame(False)
        self.lineEditAllItemsMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAllItemsMessage.setObjectName("lineEditAllItemsMessage")
        
        # Add Item
        self.groupBoxAddItem = QtWidgets.QGroupBox(self.groupBoxAllItemsOuter)
        self.groupBoxAddItem.setGeometry(QtCore.QRect(0, 0, sgX*196, sgY*90))
        self.groupBoxAddItem.setStyleSheet("background-color: #1c2428")
        self.groupBoxAddItem.setTitle("")
        self.groupBoxAddItem.setObjectName("groupBoxAddItem")

        self.lineEditAddItemID = QtWidgets.QLineEdit(self.groupBoxAddItem)
        self.lineEditAddItemID.returnPressed.connect(lambda: self.addItemIDCheck())
        self.lineEditAddItemID.setGeometry(QtCore.QRect(sgX*74, sgY*16, sgX*48, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.lineEditAddItemID.setFont(font)
        self.lineEditAddItemID.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px;color: #ffffff;")
        self.lineEditAddItemID.setText("")
        self.lineEditAddItemID.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddItemID.setObjectName("lineEditAddItemID")
        self.lineEditAddItemSerial = QtWidgets.QLineEdit(self.groupBoxAddItem)
        self.lineEditAddItemSerial.returnPressed.connect(lambda: self.addItemSerial())
        self.lineEditAddItemSerial.setGeometry(QtCore.QRect(sgX*74, sgY*27, sgX*48, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.lineEditAddItemSerial.setFont(font)
        self.lineEditAddItemSerial.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px;color: #ffffff;")
        self.lineEditAddItemSerial.setText("")
        self.lineEditAddItemSerial.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddItemSerial.setObjectName("lineEditAddItemSerial")
        self.lineEditAddItemName = QtWidgets.QLineEdit(self.groupBoxAddItem)
        self.lineEditAddItemName.returnPressed.connect(lambda: self.addItemName())
        self.lineEditAddItemName.setGeometry(QtCore.QRect(sgX*74, sgY*38, sgX*48, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.lineEditAddItemName.setFont(font)
        self.lineEditAddItemName.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px;color: #ffffff;")
        self.lineEditAddItemName.setText("")
        self.lineEditAddItemName.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddItemName.setObjectName("lineEditAddItemName")
        self.lineEditAddItemMake = QtWidgets.QLineEdit(self.groupBoxAddItem)
        self.lineEditAddItemMake.returnPressed.connect(lambda: self.addItemMake())
        self.lineEditAddItemMake.setGeometry(QtCore.QRect(sgX*74, sgY*49, sgX*48, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.lineEditAddItemMake.setFont(font)
        self.lineEditAddItemMake.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px;color: #ffffff;")
        self.lineEditAddItemMake.setText("")
        self.lineEditAddItemMake.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddItemMake.setObjectName("lineEditAddItemMake")
        self.lineEditAddItemModel = QtWidgets.QLineEdit(self.groupBoxAddItem)
        self.lineEditAddItemModel.returnPressed.connect(lambda: self.addItemModel())
        self.lineEditAddItemModel.setGeometry(QtCore.QRect(sgX*74, sgY*60, sgX*48, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.lineEditAddItemModel.setFont(font)
        self.lineEditAddItemModel.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px;color: #ffffff;")
        self.lineEditAddItemModel.setText("")
        self.lineEditAddItemModel.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddItemModel.setObjectName("lineEditAddItemModel")
        self.labelAddItemBarcode = QtWidgets.QLabel(self.groupBoxAddItem)
        self.labelAddItemBarcode.setGeometry(QtCore.QRect(sgX*75, sgY*13, sgX*18, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelAddItemBarcode.setFont(font)
        self.labelAddItemBarcode.setAutoFillBackground(False)
        self.labelAddItemBarcode.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAddItemBarcode.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAddItemBarcode.setObjectName("labelAddItemBarcode")
        self.labelAddItemSerial = QtWidgets.QLabel(self.groupBoxAddItem)
        self.labelAddItemSerial.setGeometry(QtCore.QRect(sgX*75, sgY*24, sgX*19, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelAddItemSerial.setFont(font)
        self.labelAddItemSerial.setAutoFillBackground(False)
        self.labelAddItemSerial.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAddItemSerial.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAddItemSerial.setObjectName("labelAddItemSerial")
        self.labelAddItemName = QtWidgets.QLabel(self.groupBoxAddItem)
        self.labelAddItemName.setGeometry(QtCore.QRect(sgX*75, sgY*35, sgX*19, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelAddItemName.setFont(font)
        self.labelAddItemName.setAutoFillBackground(False)
        self.labelAddItemName.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAddItemName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAddItemName.setObjectName("labelAddItemName")
        self.labelAddItemMake = QtWidgets.QLabel(self.groupBoxAddItem)
        self.labelAddItemMake.setGeometry(QtCore.QRect(sgX*75, sgY*46, sgX*19, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelAddItemMake.setFont(font)
        self.labelAddItemMake.setAutoFillBackground(False)
        self.labelAddItemMake.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAddItemMake.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAddItemMake.setObjectName("labelAddItemMake")
        self.labelAddItemModel = QtWidgets.QLabel(self.groupBoxAddItem)
        self.labelAddItemModel.setGeometry(QtCore.QRect(sgX*75, sgY*57, sgX*19, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelAddItemModel.setFont(font)
        self.labelAddItemModel.setAutoFillBackground(False)
        self.labelAddItemModel.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAddItemModel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAddItemModel.setObjectName("labelAddItemModel")
        self.pushButtonAddItemSave = QtWidgets.QPushButton(self.groupBoxAddItem, clicked = lambda: self.addItemSave())
        self.pushButtonAddItemSave.setGeometry(QtCore.QRect(sgX*74, sgY*70, sgX*14, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonAddItemSave.setFont(font)
        self.pushButtonAddItemSave.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonAddItemSave.setObjectName("pushButtonAddItemSave")
        self.pushButtonAddItemClear = QtWidgets.QPushButton(self.groupBoxAddItem, clicked = lambda: self.addItemClear())
        self.pushButtonAddItemClear.setGeometry(QtCore.QRect(sgX*108, sgY*70, sgX*14, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonAddItemClear.setFont(font)
        self.pushButtonAddItemClear.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonAddItemClear.setObjectName("pushButtonAddItemClear")
        self.lineEditAddItemMessage = QtWidgets.QLineEdit(self.groupBoxAddItem)
        self.lineEditAddItemMessage.setReadOnly(True)
        self.lineEditAddItemMessage.setGeometry(QtCore.QRect(0, sgY*3, sgX*26, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.lineEditAddItemMessage.setFont(font)
        self.lineEditAddItemMessage.setStyleSheet("color: #ffffff;")
        self.lineEditAddItemMessage.setText("")
        self.lineEditAddItemMessage.setFrame(False)
        self.lineEditAddItemMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddItemMessage.setObjectName("lineEditAddItemMessage")

        self.pushButtonAddItemDelete = QtWidgets.QPushButton(self.groupBoxAddItem, clicked = lambda: self.deleteItem())
        self.pushButtonAddItemDelete.setGeometry(QtCore.QRect(sgX*155, sgY*70, sgX*10, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonAddItemDelete.setFont(font)
        self.pushButtonAddItemDelete.setStyleSheet("border: 4px solid grey; background-color: #908000; border-radius: 10px; color: #ffffff;")
        self.pushButtonAddItemDelete.setObjectName("pushButtonAddItemDelete")

        '''
        self.pushButtonAddItemAdmin = QtWidgets.QPushButton(self.groupBoxAddItem, clicked = lambda: self.openWindowAddItemAdmin())
        self.pushButtonAddItemAdmin.setGeometry(QtCore.QRect(sgX*171, sgY*70, sgX*10, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonAddItemAdmin.setFont(font)
        self.pushButtonAddItemAdmin.setStyleSheet("border: 4px solid grey; background-color: #908000; border-radius: 10px; color: #ffffff;")
        self.pushButtonAddItemAdmin.setObjectName("pushButtonAddItemAdmin")

        # Admin
        
        self.groupBoxAddItemAdmin = QtWidgets.QGroupBox(self.groupBoxAllItemsOuter)
        self.groupBoxAddItemAdmin.setGeometry(QtCore.QRect(0, 0, sgX*196, sgY*90))
        self.groupBoxAddItemAdmin.setStyleSheet("background-color: #1c2428; border: 0px solid #000;")
        self.groupBoxAddItemAdmin.setTitle("")
        self.groupBoxAddItemAdmin.setObjectName("groupBoxAddItemAdmin")
        self.groupBoxAddItemAdmin.hide()



        self.pushButtonAddItemAdminImport = QtWidgets.QPushButton(self.groupBoxAddItemAdmin, clicked = lambda: self.AddItemAdminImport())
        self.pushButtonAddItemAdminImport.setGeometry(QtCore.QRect(sgX*31, sgY*20, sgX*14, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonAddItemAdminImport.setFont(font)
        self.pushButtonAddItemAdminImport.setStyleSheet("border: 4px solid grey; background-color: #903030; border-radius: 10px; color: #ffffff;")
        self.pushButtonAddItemAdminImport.setObjectName("pushButtonAddItemAdminImport")

        self.labelAddItemAdminCSVinfo = QtWidgets.QLabel(self.groupBoxAddItemAdmin)
        self.labelAddItemAdminCSVinfo.setGeometry(QtCore.QRect(sgX*50, sgY*14, sgX*90, sgY*17))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelAddItemAdminCSVinfo.setFont(font)
        self.labelAddItemAdminCSVinfo.setAutoFillBackground(False)
        self.labelAddItemAdminCSVinfo.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAddItemAdminCSVinfo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAddItemAdminCSVinfo.setObjectName("labelAddItemAdminCSVinfo")

        '''

        # Users

        self.groupBoxUsersOuter = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxUsersOuter.setGeometry(QtCore.QRect(sgX*2, sgY*10, sgX*196, sgY*90))
        self.groupBoxUsersOuter.setStyleSheet("background-color: #181e23; border: 0px solid #000;")
        self.groupBoxUsersOuter.setTitle("")
        self.groupBoxUsersOuter.setObjectName("groupBoxUsersOuter")

        # All Users

        self.groupBoxAllUsers = QtWidgets.QGroupBox(self.groupBoxUsersOuter)
        self.groupBoxAllUsers.setGeometry(QtCore.QRect(0, 0, sgX*196, sgY*90))
        self.groupBoxAllUsers.setStyleSheet("background-color: #1c2428; border: 0px solid #000;")
        self.groupBoxAllUsers.setTitle("")
        self.groupBoxAllUsers.setObjectName("groupBoxAllUsers")

        self.pushButtonAllUsersAllUsers = QtWidgets.QPushButton(self.groupBoxMenu, clicked = lambda: self.openWindowAllUsers())
        self.pushButtonAllUsersAllUsers.setGeometry(QtCore.QRect(sgX*174, sgY, sgX*10, sgY*6))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.pushButtonAllUsersAllUsers.setFont(font)
        self.pushButtonAllUsersAllUsers.setStyleSheet("border: 4px solid #aa3333; background-color: #408040; border-radius: 10px;color: #ffffff;")
        self.pushButtonAllUsersAllUsers.setObjectName("pushButtonAllUsersAllUsers")
        self.pushButtonAllUsersAllUsers.hide()
        self.pushButtonAllUsersAddUser = QtWidgets.QPushButton(self.groupBoxMenu, clicked = lambda: self.openWindowAddUser())
        self.pushButtonAllUsersAddUser.setGeometry(QtCore.QRect(sgX*185, sgY, sgX*10, sgY*6))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.pushButtonAllUsersAddUser.setFont(font)
        self.pushButtonAllUsersAddUser.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonAllUsersAddUser.setObjectName("pushButtonAllUsersAddUser")
        self.pushButtonAllUsersAddUser.hide()


        # All Users

        self.tableWidgetAllUsers = QtWidgets.QTableWidget(self.groupBoxAllUsers)
        self.tableWidgetAllUsers.setGeometry(QtCore.QRect(sgX*20, sgY*9, sgX*174, sgY*77))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetAllUsers.sizePolicy().hasHeightForWidth())
        self.tableWidgetAllUsers.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.tableWidgetAllUsers.setFont(font)
        self.tableWidgetAllUsers.setAutoFillBackground(False)
        self.tableWidgetAllUsers.setStyleSheet(styleSheet)
        self.tableWidgetAllUsers.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidgetAllUsers.setLineWidth(1)
        self.tableWidgetAllUsers.setMidLineWidth(0)
        self.tableWidgetAllUsers.setAlternatingRowColors(True)
        self.tableWidgetAllUsers.setShowGrid(True)
        self.tableWidgetAllUsers.setRowCount(0)
        self.tableWidgetAllUsers.setObjectName("tableWidgetAllUsers")
        self.tableWidgetAllUsers.setColumnCount(3)
        self.tableWidgetAllUsers.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetAllUsers.setHorizontalHeaderItem(0, item)
        self.tableWidgetAllUsers.setColumnWidth(0, sgX*25)    # userID
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidgetAllUsers.setHorizontalHeaderItem(1, item)
        self.tableWidgetAllUsers.setColumnWidth(1, sgX*50)    # userName
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        item.setFont(font)
        self.tableWidgetAllUsers.setHorizontalHeaderItem(2, item)
        self.tableWidgetAllUsers.setColumnWidth(2, sgX*50)    # userEmail
        self.tableWidgetAllUsers.verticalHeader().setVisible(True)
        self.tableWidgetAllUsers.verticalHeader().setHighlightSections(True)

        self.labelAllUsersUserID = QtWidgets.QLabel(self.groupBoxAllUsers)
        self.labelAllUsersUserID.setGeometry(QtCore.QRect(sgX*22, 0, sgX*16, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelAllUsersUserID.setFont(font)
        self.labelAllUsersUserID.setAutoFillBackground(False)
        self.labelAllUsersUserID.setStyleSheet("color: white; background-color: rgba(255, 255, 255, 0);")
        self.labelAllUsersUserID.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAllUsersUserID.setObjectName("labelAllUsersUserID")
        self.lineEditAllUsersUserID = QtWidgets.QLineEdit(self.groupBoxAllUsers)
        self.lineEditAllUsersUserID.returnPressed.connect(lambda: self.getUserFromID(0))
        self.lineEditAllUsersUserID.setGeometry(QtCore.QRect(sgX*21, sgY*3, sgX*28, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.lineEditAllUsersUserID.setFont(font)
        self.lineEditAllUsersUserID.setStyleSheet("Border: 4px solid grey; background-color: #111; border-radius: 10px; color: #ffffff;")
        self.lineEditAllUsersUserID.setText("")
        self.lineEditAllUsersUserID.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAllUsersUserID.setObjectName("lineEditAllUsersUserID")

        self.labelAllUsersUserName = QtWidgets.QLabel(self.groupBoxAllUsers)
        self.labelAllUsersUserName.setGeometry(QtCore.QRect(sgX*77, 0, sgX*16, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelAllUsersUserName.setFont(font)
        self.labelAllUsersUserName.setAutoFillBackground(False)
        self.labelAllUsersUserName.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAllUsersUserName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAllUsersUserName.setObjectName("labelAllUsersUserName")
        self.lineEditAllUsersUserName = QtWidgets.QLineEdit(self.groupBoxAllUsers)
        self.lineEditAllUsersUserName.returnPressed.connect(lambda: self.getUserFromName(-1))
        self.lineEditAllUsersUserName.setGeometry(QtCore.QRect(sgX*76, sgY*3, sgX*44, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.lineEditAllUsersUserName.setFont(font)
        self.lineEditAllUsersUserName.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px; color: #ffffff;")
        self.lineEditAllUsersUserName.setText("")
        self.lineEditAllUsersUserName.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAllUsersUserName.setObjectName("lineEditAllUsersUserName")
        self.listWidgetAllUsersUserName = QtWidgets.QListWidget(self.groupBoxAllUsers)
        self.listWidgetAllUsersUserName.itemClicked.connect(self.listItemAllUsersClicked)
        self.listWidgetAllUsersUserName.setGeometry(QtCore.QRect(sgX*77, sgY*7, sgX*42, sgY*35))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.listWidgetAllUsersUserName.setFont(font)
        self.listWidgetAllUsersUserName.setStyleSheet("color: white; border: 1px solid grey;")
        self.listWidgetAllUsersUserName.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.listWidgetAllUsersUserName.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.listWidgetAllUsersUserName.setObjectName("listWidgetAllUsersUserName")
        self.listWidgetAllUsersUserName.hide()

        self.labelAllUsersUserEmail = QtWidgets.QLabel(self.groupBoxAllUsers)
        self.labelAllUsersUserEmail.setGeometry(QtCore.QRect(sgX*152, 0, sgX*16, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelAllUsersUserEmail.setFont(font)
        self.labelAllUsersUserEmail.setAutoFillBackground(False)
        self.labelAllUsersUserEmail.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAllUsersUserEmail.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAllUsersUserEmail.setObjectName("labelAllUsersUserEmail")
        self.lineEditAllUsersUserEmail = QtWidgets.QLineEdit(self.groupBoxAllUsers)
        self.lineEditAllUsersUserEmail.returnPressed.connect(lambda: self.getUserFromEmail(-1))
        self.lineEditAllUsersUserEmail.setGeometry(QtCore.QRect(sgX*151, sgY*3, sgX*44, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.lineEditAllUsersUserEmail.setFont(font)
        self.lineEditAllUsersUserEmail.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px; color: #ffffff;")
        self.lineEditAllUsersUserEmail.setText("")
        self.lineEditAllUsersUserEmail.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAllUsersUserEmail.setObjectName("lineEditAllUsersUserEmail")
        self.listWidgetAllUsersUserEmail = QtWidgets.QListWidget(self.groupBoxAllUsers)
        self.listWidgetAllUsersUserEmail.itemClicked.connect(self.listItemEmailAllUsersClicked)
        self.listWidgetAllUsersUserEmail.setGeometry(QtCore.QRect(sgX*152, sgY*7, sgX*42, sgY*35))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.listWidgetAllUsersUserEmail.setFont(font)
        self.listWidgetAllUsersUserEmail.setStyleSheet("color: white; border: 1px solid grey;")
        self.listWidgetAllUsersUserEmail.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.listWidgetAllUsersUserEmail.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.listWidgetAllUsersUserEmail.setObjectName("listWidgetAllUsersUserEmail")
        self.listWidgetAllUsersUserEmail.hide()
        
        self.pushButtonAllUsersClear = QtWidgets.QPushButton(self.groupBoxAllUsers)
        self.pushButtonAllUsersClear = QtWidgets.QPushButton(self.groupBoxAllUsers, clicked = lambda: self.clearAllUsers())
        self.pushButtonAllUsersClear.setGeometry(QtCore.QRect(sgX*2, sgY*23, sgX*16, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonAllUsersClear.setFont(font)
        self.pushButtonAllUsersClear.setStyleSheet("border: 4px solid grey; border-radius: 10px;background-color: #804040; color: #ffffff;")
        self.pushButtonAllUsersClear.setObjectName("pushButtonAllUsersClear")

        # Add User

        self.groupBoxAddUser = QtWidgets.QGroupBox(self.groupBoxUsersOuter)
        self.groupBoxAddUser.setGeometry(QtCore.QRect(0, 0, sgX*196, sgY*90))
        self.groupBoxAddUser.setStyleSheet("background-color: #1c2428; border: 0px solid #000;")
        self.groupBoxAddUser.setTitle("")
        self.groupBoxAddUser.setObjectName("groupBoxAddUser")

        self.lineEditAddUserID = QtWidgets.QLineEdit(self.groupBoxAddUser)
        self.lineEditAddUserID.returnPressed.connect(lambda: self.addUserIDCheck())
        self.lineEditAddUserID.setGeometry(QtCore.QRect(sgX*74, sgY*16, sgX*48, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.lineEditAddUserID.setFont(font)
        self.lineEditAddUserID.setStyleSheet("border: 4px solid grey;background-color: #111;border-radius: 10px; color: #ffffff;")
        self.lineEditAddUserID.setText("")
        self.lineEditAddUserID.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddUserID.setObjectName("lineEditAddUserID")
        self.lineEditAddUserFirst = QtWidgets.QLineEdit(self.groupBoxAddUser)
        self.lineEditAddUserFirst.returnPressed.connect(lambda: self.addUserFirstCheck())
        self.lineEditAddUserFirst.setGeometry(QtCore.QRect(sgX*74, sgY*27, sgX*48, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.lineEditAddUserFirst.setFont(font)
        self.lineEditAddUserFirst.setStyleSheet("border: 4px solid grey;background-color: #111;border-radius: 10px; color: #ffffff;")
        self.lineEditAddUserFirst.setText("")
        self.lineEditAddUserFirst.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddUserFirst.setObjectName("lineEditAddUserFirst")
        self.lineEditAddUserLast = QtWidgets.QLineEdit(self.groupBoxAddUser)
        self.lineEditAddUserLast.returnPressed.connect(lambda: self.addUserLastCheck())
        self.lineEditAddUserLast.setGeometry(QtCore.QRect(sgX*74, sgY*38, sgX*48, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.lineEditAddUserLast.setFont(font)
        self.lineEditAddUserLast.setStyleSheet("border: 4px solid grey;background-color: #111;border-radius: 10px; color: #ffffff;")
        self.lineEditAddUserLast.setText("")
        self.lineEditAddUserLast.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddUserLast.setObjectName("lineEditAddUserLast")
        self.lineEditAddUserEmail = QtWidgets.QLineEdit(self.groupBoxAddUser)
        self.lineEditAddUserEmail.returnPressed.connect(lambda: self.addUserEmailCheck())
        self.lineEditAddUserEmail.setGeometry(QtCore.QRect(sgX*74, sgY*49, sgX*48, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.lineEditAddUserEmail.setFont(font)
        self.lineEditAddUserEmail.setStyleSheet("border: 4px solid grey;background-color: #111;border-radius: 10px; color: #ffffff;")
        self.lineEditAddUserEmail.setText("")
        self.lineEditAddUserEmail.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddUserEmail.setObjectName("lineEditAddUserEmail")
        self.labelAddUserBarcode = QtWidgets.QLabel(self.groupBoxAddUser)
        self.labelAddUserBarcode.setGeometry(QtCore.QRect(sgX*75, sgY*13, sgX*18, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelAddUserBarcode.setFont(font)
        self.labelAddUserBarcode.setAutoFillBackground(False)
        self.labelAddUserBarcode.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAddUserBarcode.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAddUserBarcode.setObjectName("labelAddUserBarcode")
        self.labelAddUserFirstName = QtWidgets.QLabel(self.groupBoxAddUser)
        self.labelAddUserFirstName.setGeometry(QtCore.QRect(sgX*75, sgY*24, sgX*19, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelAddUserFirstName.setFont(font)
        self.labelAddUserFirstName.setAutoFillBackground(False)
        self.labelAddUserFirstName.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAddUserFirstName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAddUserFirstName.setObjectName("labelAddUserFirstName")
        self.labelAddUserLastName = QtWidgets.QLabel(self.groupBoxAddUser)
        self.labelAddUserLastName.setGeometry(QtCore.QRect(sgX*75, sgY*35, sgX*19, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelAddUserLastName.setFont(font)
        self.labelAddUserLastName.setAutoFillBackground(False)
        self.labelAddUserLastName.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAddUserLastName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAddUserLastName.setObjectName("labelAddUserLastName")
        self.labelAddUserEmail = QtWidgets.QLabel(self.groupBoxAddUser)
        self.labelAddUserEmail.setGeometry(QtCore.QRect(sgX*75, sgY*46, sgX*19, sgY*3))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelAddUserEmail.setFont(font)
        self.labelAddUserEmail.setAutoFillBackground(False)
        self.labelAddUserEmail.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAddUserEmail.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAddUserEmail.setObjectName("labelAddUserEmail")
        self.pushButtonAddUserSave = QtWidgets.QPushButton(self.groupBoxAddUser, clicked = lambda: self.addUserSave())
        self.pushButtonAddUserSave.setGeometry(QtCore.QRect(sgX*74, sgY*70, sgX*14, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonAddUserSave.setFont(font)
        self.pushButtonAddUserSave.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonAddUserSave.setObjectName("pushButtonAddUserSave")
        self.pushButtonAddUserClear = QtWidgets.QPushButton(self.groupBoxAddUser, clicked = lambda: self.addUserClear())
        self.pushButtonAddUserClear.setGeometry(QtCore.QRect(sgX*108, sgY*70, sgX*14, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonAddUserClear.setFont(font)
        self.pushButtonAddUserClear.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonAddUserClear.setObjectName("pushButtonAddUserSave")
        self.lineEditAddUserMessage = QtWidgets.QLineEdit(self.groupBoxAddUser)
        self.lineEditAddUserMessage.setReadOnly(True)
        self.lineEditAddUserMessage.setGeometry(QtCore.QRect(0, sgY*3, sgX*26, sgY*4))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.lineEditAddUserMessage.setFont(font)
        self.lineEditAddUserMessage.setStyleSheet("color: #ffffff;")
        self.lineEditAddUserMessage.setText("")
        self.lineEditAddUserMessage.setFrame(False)
        self.lineEditAddUserMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddUserMessage.setObjectName("lineEditAddUserMessage")

        self.pushButtonAddUserAdmin = QtWidgets.QPushButton(self.groupBoxAddUser, clicked = lambda: self.openWindowAddUserAdmin())
        self.pushButtonAddUserAdmin.setGeometry(QtCore.QRect(sgX*171, sgY*70, sgX*10, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonAddUserAdmin.setFont(font)
        self.pushButtonAddUserAdmin.setStyleSheet("border: 4px solid grey; background-color: #908000; border-radius: 10px; color: #ffffff;")
        self.pushButtonAddUserAdmin.setObjectName("pushButtonAddUserAdmin")

        # Admin

        self.groupBoxAddUserAdmin = QtWidgets.QGroupBox(self.groupBoxUsersOuter)
        self.groupBoxAddUserAdmin.setGeometry(QtCore.QRect(0, 0, sgX*196, sgY*90))
        self.groupBoxAddUserAdmin.setStyleSheet("background-color: #1c2428; border: 0px solid #000;")
        self.groupBoxAddUserAdmin.setTitle("")
        self.groupBoxAddUserAdmin.setObjectName("groupBoxAddUserAdmin")
        self.groupBoxAddUserAdmin.hide()



        self.pushButtonAddUserAdminImport = QtWidgets.QPushButton(self.groupBoxAddUserAdmin, clicked = lambda: self.addUserAdminImport())
        self.pushButtonAddUserAdminImport.setGeometry(QtCore.QRect(sgX*31, sgY*20, sgX*14, sgY*5))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2.5))
        self.pushButtonAddUserAdminImport.setFont(font)
        self.pushButtonAddUserAdminImport.setStyleSheet("border: 4px solid grey; background-color: #903030; border-radius: 10px; color: #ffffff;")
        self.pushButtonAddUserAdminImport.setObjectName("pushButtonAddUserAdminImport")

        self.labelAddUserAdminCSVinfo = QtWidgets.QLabel(self.groupBoxAddUserAdmin)
        self.labelAddUserAdminCSVinfo.setGeometry(QtCore.QRect(sgX*50, sgY*14, sgX*90, sgY*17))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(int(sgX*2))
        self.labelAddUserAdminCSVinfo.setFont(font)
        self.labelAddUserAdminCSVinfo.setAutoFillBackground(False)
        self.labelAddUserAdminCSVinfo.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAddUserAdminCSVinfo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAddUserAdminCSVinfo.setObjectName("labelAddUserAdminCSVinfo")




        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Database"))
        self.pushButtonBookOut.setText(_translate("MainWindow", "Book-Out"))
        self.pushButtonReturn.setText(_translate("MainWindow", "Return"))
        self.pushButtonBookedOut.setText(_translate("MainWindow", "Booked Out"))
        self.pushButtonHistory.setText(_translate("MainWindow", "History"))
        self.pushButtonItems.setText(_translate("MainWindow", "Items"))
        self.pushButtonUsers.setText(_translate("MainWindow", "Users"))


        item = self.tableWidgetBO.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Long-Term"))
        item = self.tableWidgetBO.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Item ID"))
        item = self.tableWidgetBO.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Item Name"))
        item = self.tableWidgetBO.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Item Make"))
        item = self.tableWidgetBO.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Item Model"))
        item = self.tableWidgetBO.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Item Serial #"))
        self.pushButtonBOClear.setText(_translate("MainWindow", "Clear All"))
        self.pushButtonBOClearLast.setText(_translate("MainWindow", "Clear Last"))
        self.pushButtonBOCancel.setText(_translate("MainWindow", "Cancel"))
        self.pushButtonBOSubmit.setText(_translate("MainWindow", "Submit"))
        self.labelBOItemID.setText(_translate("MainWindow", "Item ID"))
        self.labelBOUserID.setText(_translate("MainWindow", "User ID"))
        self.labelBOUserName.setText(_translate("MainWindow", "User Name"))
        self.labelBOUserEmail.setText(_translate("MainWindow", "User Email"))


        item = self.tableWidgetRe.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Item ID"))
        item = self.tableWidgetRe.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Item Name"))
        item = self.tableWidgetRe.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "User ID"))
        item = self.tableWidgetRe.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "User Name"))
        item = self.tableWidgetRe.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "User Email"))
        self.labelReItemID.setText(_translate("MainWindow", "Item ID"))


        item = self.tableWidgetBkdO.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Long-Term"))
        item = self.tableWidgetBkdO.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Item ID"))
        item = self.tableWidgetBkdO.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Item Name"))
        item = self.tableWidgetBkdO.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "User Name"))
        item = self.tableWidgetBkdO.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "User Email"))
        item = self.tableWidgetBkdO.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Date Booked Out"))
        self.pushButtonBkdOExport.setText(_translate("MainWindow", "Export"))
        self.labelBkdOShowLong.setText(_translate("MainWindow", "Show Long Term"))


        item = self.tableWidgetHist.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Item ID"))
        item = self.tableWidgetHist.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Item Name"))
        item = self.tableWidgetHist.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "User Name"))
        item = self.tableWidgetHist.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "User Email"))
        item = self.tableWidgetHist.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Date Out"))
        item = self.tableWidgetHist.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Date In"))
        self.pushButtonHistClear.setText(_translate("MainWindow", "Clear"))
        self.pushButtonHistExport.setText(_translate("MainWindow", "Export"))
        self.pushButtonHistResetDate.setText(_translate("MainWindow", "Reset"))
        self.labelHistItemID.setText(_translate("MainWindow", "Item ID"))
        self.labelHistUserID.setText(_translate("MainWindow", "User ID"))
        self.labelHistUserName.setText(_translate("MainWindow", "User Name"))
        self.labelHistUserEmail.setText(_translate("MainWindow", "User Email"))
        self.labelHistDateFrom.setText(_translate("MainWindow", "From"))
        self.labelHistDateTo.setText(_translate("MainWindow", "To"))


        item = self.tableWidgetAllItems.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Item ID"))
        item = self.tableWidgetAllItems.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Item Name"))
        item = self.tableWidgetAllItems.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Item Make"))
        item = self.tableWidgetAllItems.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Item Model"))
        item = self.tableWidgetAllItems.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Item Serial #"))

        self.pushButtonAllItemsAllItems.setText(_translate("MainWindow", "All\nItems"))
        self.pushButtonAllItemsAddItem.setText(_translate("MainWindow", "Edit\nItems"))
        self.pushButtonAllItemsClear.setText(_translate("MainWindow", "Clear"))
        self.pushButtonAllItemsExport.setText(_translate("MainWindow", "Export"))
        self.labelAllItemsItemID.setText(_translate("MainWindow", "Item ID"))
        self.labelAllItemsItemSearch.setText(_translate("MainWindow", "Item Search"))


        self.labelAddItemBarcode.setText(_translate("MainWindow", "Item BarCode"))
        self.labelAddItemSerial.setText(_translate("MainWindow", "Item Serial No."))
        self.labelAddItemName.setText(_translate("MainWindow", "Item Name"))
        self.labelAddItemMake.setText(_translate("MainWindow", "Item Make"))
        self.labelAddItemModel.setText(_translate("MainWindow", "Item Model"))
        self.pushButtonAddItemSave.setText(_translate("MainWindow", "Save"))
        self.pushButtonAddItemClear.setText(_translate("MainWindow", "Clear"))

        self.pushButtonAddItemDelete.setText(_translate("MainWindow", "Delete"))
        #self.pushButtonAddItemAdmin.setText(_translate("MainWindow", "Admin"))
        
        #self.pushButtonAddItemAdminImport.setText(_translate("MainWindow", "Import"))
        #self.labelAddItemAdminCSVinfo.setText(_translate("MainWindow", "This will add new items to the current database.\nUse .csv file, ****"))

        self.pushButtonAllUsersAllUsers.setText(_translate("MainWindow", "All\nUsers"))
        self.pushButtonAllUsersAddUser.setText(_translate("MainWindow", "Edit\nUsers"))
        self.labelAllUsersUserID.setText(_translate("MainWindow", "UserID"))
        self.labelAllUsersUserName.setText(_translate("MainWindow", "User Name"))
        self.labelAllUsersUserEmail.setText(_translate("MainWindow", "User Email"))
        item = self.tableWidgetAllUsers.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "User ID"))
        item = self.tableWidgetAllUsers.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "User Name"))
        item = self.tableWidgetAllUsers.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "User Email"))
        self.pushButtonAllUsersClear.setText(_translate("MainWindow", "Clear"))


        self.pushButtonAddUserSave.setText(_translate("MainWindow", "Save"))
        self.pushButtonAddUserClear.setText(_translate("MainWindow", "Clear"))
        self.labelAddUserBarcode.setText(_translate("MainWindow", "User BarCode"))
        self.labelAddUserFirstName.setText(_translate("MainWindow", "User First Name"))
        self.labelAddUserLastName.setText(_translate("MainWindow", "User Last Name"))
        self.labelAddUserEmail.setText(_translate("MainWindow", "User Email"))

        self.pushButtonAddUserAdmin.setText(_translate("MainWindow", "Admin"))
        self.pushButtonAddUserAdminImport.setText(_translate("MainWindow", "Import"))
        
        self.labelAddUserAdminCSVinfo.setText(_translate("MainWindow", "This will add new users to the current database.\nUse .csv file, with coloumns, User ID, First Name, Last Name, Email"))



        self.show()
        self.groupBoxRe.hide()
        self.groupBoxBkdO.hide()
        self.groupBoxHist.hide()
        self.groupBoxAllItemsOuter.hide()
        self.groupBoxAllItems.hide()
        self.groupBoxAddItem.hide()
        self.groupBoxUsersOuter.hide()
        self.groupBoxAllUsers.hide()
        self.groupBoxAddUser.hide()

        self.lineEditBOUserID.setFocus()

    def onCellChanged(self, row, column):
        global watchCellChange

        if watchCellChange:
            checkBox = self.tableWidgetBkdO.item(row, column)
            currentState = checkBox.checkState()
            state = currentState.value
            
            if state > 0:
                longTerm = "*"
            else:
                longTerm = ""
                
            itemID = self.tableWidgetBkdO.item(row, 1).text()
            
            outDB.update({'longTerm': longTerm}, DBquery.itemID == itemID)

            self.populateBookedOut()



    def openWindowBookOut(self):
        self.pushButtonBookOut.setStyleSheet("border: 4px solid #aa3333; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonReturn.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonBookedOut.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonHistory.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.show()
        self.pushButtonAllItemsAllItems.hide()
        self.pushButtonAllItemsAddItem.hide()
        self.pushButtonUsers.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonUsers.show()
        self.pushButtonAllUsersAllUsers.hide()
        self.pushButtonAllUsersAddUser.hide()
        self.groupBoxBO.show()
        self.groupBoxRe.hide()
        self.groupBoxBkdO.hide()
        self.groupBoxHist.hide()
        self.groupBoxAllItemsOuter.hide()
        self.groupBoxAllItems.hide()
        self.groupBoxAddItem.hide()
        self.groupBoxUsersOuter.hide()
        self.groupBoxAllUsers.hide()
        self.groupBoxAddUser.hide()
        self.groupBoxAddUserAdmin.hide()
        #self.groupBoxAddItemAdmin.hide()

        self.lineEditBOUserID.setText("")
        self.lineEditBOUserName.setText("")
        self.lineEditBOUserEmail.setText("")

        self.clearAll()

        self.lineEditBOUserID.setFocus()

    def openWindowReturn(self):
        self.pushButtonBookOut.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonReturn.setStyleSheet("border: 4px solid #aa3333; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonBookedOut.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonHistory.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.show()
        self.pushButtonAllItemsAllItems.hide()
        self.pushButtonAllItemsAddItem.hide()
        self.pushButtonUsers.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonUsers.show()
        self.pushButtonAllUsersAllUsers.hide()
        self.pushButtonAllUsersAddUser.hide()
        self.groupBoxBO.hide()
        self.groupBoxRe.show()
        self.groupBoxBkdO.hide()
        self.groupBoxHist.hide()
        self.groupBoxAllItemsOuter.hide()
        self.groupBoxAllItems.hide()
        self.groupBoxAddItem.hide()
        self.groupBoxUsersOuter.hide()
        self.groupBoxAllUsers.hide()
        self.groupBoxAddUser.hide()
        self.groupBoxAddUserAdmin.hide()
        #self.groupBoxAddItemAdmin.hide()
        
        self.tableWidgetRe.setRowCount(0)
        
        self.lineEditReItemID.setFocus()

    def openWindowBookedOut(self):
        self.pushButtonBookOut.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonReturn.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonBookedOut.setStyleSheet("border: 4px solid #aa3333; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonHistory.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.show()
        self.pushButtonAllItemsAllItems.hide()
        self.pushButtonAllItemsAddItem.hide()
        self.pushButtonUsers.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonUsers.show()
        self.pushButtonAllUsersAllUsers.hide()
        self.pushButtonAllUsersAddUser.hide()
        self.groupBoxBO.hide()
        self.groupBoxRe.hide()
        self.groupBoxBkdO.show()
        self.groupBoxHist.hide()
        self.groupBoxAllItemsOuter.hide()
        self.groupBoxAllItems.hide()
        self.groupBoxAddItem.hide()
        self.groupBoxUsersOuter.hide()
        self.groupBoxAllUsers.hide()
        self.groupBoxAddUser.hide()
        self.groupBoxAddUserAdmin.hide()
        #self.groupBoxAddItemAdmin.hide()

        self.populateBookedOut()

    def openWindowHistory(self):
        global dateRangeFrom
        global dateRangeTo
        global historyItemID
        global historyUserEmail

        historyItemID = ""
        historyUserEmail = ""

        currentDate = QtCore.QDate.currentDate()

        self.dateEditFrom.setDate(currentDate.addDays(-28))
        self.dateEditTo.setDate(currentDate)

        self.pushButtonBookOut.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonReturn.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonBookedOut.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonHistory.setStyleSheet("border: 4px solid #aa3333; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.show()
        self.pushButtonAllItemsAllItems.hide()
        self.pushButtonAllItemsAddItem.hide()
        self.pushButtonUsers.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonUsers.show()
        self.pushButtonAllUsersAllUsers.hide()
        self.pushButtonAllUsersAddUser.hide()
        self.groupBoxBO.hide()
        self.groupBoxRe.hide()
        self.groupBoxBkdO.hide()
        self.groupBoxHist.show()
        self.groupBoxAllItemsOuter.hide()
        self.groupBoxAllItems.hide()
        self.groupBoxAddItem.hide()
        self.groupBoxUsersOuter.hide()
        self.groupBoxAddUserAdmin.hide()
        #self.groupBoxAddItemAdmin.hide()

        self.refreshHistory()

    def openWindowAllItems(self):
        self.pushButtonBookOut.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonReturn.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonBookedOut.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonHistory.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.setStyleSheet("border: 4px solid #aa3333; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.hide()
        self.pushButtonAllItemsAllItems.setStyleSheet("border: 4px solid #aa3333; background-color: #408040; border-radius: 10px;color: #ffffff;")
        self.pushButtonAllItemsAllItems.show()
        self.pushButtonAllItemsAddItem.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px;color: #ffffff;")
        self.pushButtonAllItemsAddItem.show()
        self.pushButtonUsers.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonUsers.show()
        self.pushButtonAllUsersAllUsers.hide()
        self.pushButtonAllUsersAddUser.hide()
        self.groupBoxBO.hide()
        self.groupBoxRe.hide()
        self.groupBoxBkdO.hide()
        self.groupBoxHist.hide()
        self.groupBoxAllItemsOuter.show()
        self.groupBoxAllItems.show()
        self.groupBoxAddItem.hide()
        self.groupBoxUsersOuter.hide()
        self.groupBoxAllUsers.hide()
        self.groupBoxAddUser.hide()
        self.groupBoxAddUserAdmin.hide()
        #self.groupBoxAddItemAdmin.hide()

        global allItemsSearchText
        global allItemsSearchID

        allItemsSearchText = ""
        allItemsSearchID = ""

        self.populateAllItems()

    def openWindowAddItem(self):
        self.pushButtonBookOut.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonReturn.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonBookedOut.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonHistory.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.setStyleSheet("border: 4px solid #aa3333; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.hide()
        self.pushButtonAllItemsAllItems.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px;color: #ffffff;")
        self.pushButtonAllItemsAllItems.show()
        self.pushButtonAllItemsAddItem.setStyleSheet("border: 4px solid #aa3333; background-color: #408040; border-radius: 10px;color: #ffffff;")
        self.pushButtonAllItemsAddItem.show()
        self.pushButtonUsers.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonUsers.show()
        self.pushButtonAllUsersAllUsers.hide()
        self.pushButtonAllUsersAddUser.hide()
        self.groupBoxBO.hide()
        self.groupBoxRe.hide()
        self.groupBoxBkdO.hide()
        self.groupBoxHist.hide()
        self.groupBoxAllItemsOuter.show()
        self.groupBoxAllItems.hide()
        self.groupBoxAddItem.show()
        self.groupBoxUsersOuter.hide()
        self.groupBoxAllUsers.hide()
        self.groupBoxAddUser.hide()
        self.groupBoxAddUserAdmin.hide()
        #self.groupBoxAddItemAdmin.hide()

        self.lineEditAddItemID.setFocus()

    def openWindowAllUsers(self):
        self.pushButtonBookOut.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonReturn.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonBookedOut.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonHistory.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.show()
        self.pushButtonAllItemsAllItems.hide()
        self.pushButtonAllItemsAddItem.hide()
        self.pushButtonUsers.setStyleSheet("border: 4px solid #aa3333; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonUsers.hide()
        self.pushButtonAllUsersAllUsers.setStyleSheet("border: 4px solid #aa3333; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonAllUsersAllUsers.show()
        self.pushButtonAllUsersAddUser.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonAllUsersAddUser.show()
        self.groupBoxBO.hide()
        self.groupBoxRe.hide()
        self.groupBoxBkdO.hide()
        self.groupBoxHist.hide()
        self.groupBoxAllItemsOuter.hide()
        self.groupBoxAllItems.hide()
        self.groupBoxAddItem.hide()
        self.groupBoxUsersOuter.show()
        self.groupBoxAllUsers.show()
        self.groupBoxAddUser.hide()
        self.groupBoxAddUserAdmin.hide()
        #self.groupBoxAddItemAdmin.hide()

        global allUsersSearchID
        global allUsersSearchName
        global allUsersSearchEmail

        allUsersSearchID = ""
        allUsersSearchName = ""
        allUsersSearchEmail = ""

        self.populateAllUsers()

    def openWindowAddUser(self):
        self.pushButtonBookOut.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonReturn.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonBookedOut.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonHistory.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.show()
        self.pushButtonAllItemsAllItems.hide()
        self.pushButtonAllItemsAddItem.hide()
        self.pushButtonUsers.setStyleSheet("border: 4px solid #aa3333; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonUsers.hide()
        self.pushButtonAllUsersAllUsers.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonAllUsersAllUsers.show()
        self.pushButtonAllUsersAddUser.setStyleSheet("border: 4px solid #aa3333; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonAllUsersAddUser.show()
        self.groupBoxBO.hide()
        self.groupBoxRe.hide()
        self.groupBoxBkdO.hide()
        self.groupBoxHist.hide()
        self.groupBoxAllItemsOuter.hide()
        self.groupBoxAllItems.hide()
        self.groupBoxAddItem.hide()
        self.groupBoxUsersOuter.show()
        self.groupBoxAllUsers.hide()
        self.groupBoxAddUser.show()
        self.groupBoxAddUserAdmin.hide()
        #self.groupBoxAddItemAdmin.hide()

        self.lineEditAddUserID.setFocus()

    def openWindowAddUserAdmin(self):
        self.pushButtonBookOut.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonReturn.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonBookedOut.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonHistory.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.show()
        self.pushButtonAllItemsAllItems.hide()
        self.pushButtonAllItemsAddItem.hide()
        self.pushButtonUsers.setStyleSheet("border: 4px solid #aa3333; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonUsers.hide()
        self.pushButtonAllUsersAllUsers.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonAllUsersAllUsers.show()
        self.pushButtonAllUsersAddUser.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonAllUsersAddUser.show()
        self.groupBoxBO.hide()
        self.groupBoxRe.hide()
        self.groupBoxBkdO.hide()
        self.groupBoxHist.hide()
        self.groupBoxAllItemsOuter.hide()
        self.groupBoxAllItems.hide()
        self.groupBoxAddItem.hide()
        self.groupBoxUsersOuter.show()
        self.groupBoxAllUsers.hide()
        self.groupBoxAddUser.hide()
        self.groupBoxAddUserAdmin.show()
        #self.groupBoxAddItemAdmin.hide()


    def getUserFromID(self, userID):
        userEmail = ""
        userName = ""

        if userID == 0:

            if self.groupBoxHist.isHidden():
                userID = self.lineEditBOUserID.text()
            elif self.groupBoxBO.isHidden():
                userID = self.lineEditHistUserID.text()

        if len(userID) > 5:
            userID = userID.rstrip(userID[-1])
            foundID = userDB.search(DBquery.userID.search(userID))
            userID = (foundID[0]['userID'])
            
        getUser = (userDB.search(DBquery.userID == userID))                                 # search for user number in item database

        if not getUser:                                                                     # If user not found...                     # Remove text in main page message box after 2 seconds
            self.doMessage("No user found")
            self.lineEditBOUserID.setText("")

        else:
            userName = (getUser[0]['firstName']) + " " + (getUser[0]['lastName'])
            userEmail = (getUser[0]['email'])
            if self.groupBoxHist.isHidden():
                self.lineEditBOUserName.setText(userName)
                self.lineEditBOUserEmail.setText(userEmail)
                self.lineEditBOItemID.setFocus()
            elif self.groupBoxBO.isHidden():
                self.lineEditHistUserName.setText(userName)
                self.lineEditHistUserEmail.setText(userEmail)

                self.refreshHistory()

        return userID, userName, userEmail
    
    def getUserFromName(self, nameIndex):
        global userNameList

        userNameList = []
        userID = ""
        userName = ""
        userEmail = ""
        foundNames = ""

        if self.groupBoxHist.isHidden() and self.groupBoxAllUsers.isHidden():
            names = self.lineEditBOUserName.text()
        elif self.groupBoxBO.isHidden() and self.groupBoxAllUsers.isHidden():
            names = self.lineEditHistUserName.text()
        elif self.groupBoxHist.isHidden() and self.groupBoxBO.isHidden():
            names = self.lineEditAllUsersUserName.text()

        foundFirstNames = userDB.search(DBquery.firstName.search(names + '+', flags=re.IGNORECASE))
        foundLastNames = userDB.search(DBquery.lastName.search(names + '+', flags=re.IGNORECASE))

        foundNames = foundFirstNames + foundLastNames
        
        if len(foundNames) == 1:
            userID = (foundNames[0]['userID'])
            userName = (foundNames[0]['firstName']) + " " + (foundNames[0]['lastName'])
            userEmail = (foundNames[0]['email'])

            if self.groupBoxHist.isHidden() and self.groupBoxAllUsers.isHidden():
                self.lineEditBOUserID.setText(userID)
                self.lineEditBOUserName.setText(userName)
                self.lineEditBOUserEmail.setText(userEmail)

            elif self.groupBoxBO.isHidden() and self.groupBoxAllUsers.isHidden():
                self.lineEditHistUserID.setText(userID)
                self.lineEditHistUserName.setText(userName)
                self.lineEditHistUserEmail.setText(userEmail)

            elif self.groupBoxHist.isHidden() and self.groupBoxBO.isHidden():
                self.lineEditAllUsersUserID.setText(userID)
                self.lineEditAllUsersUserName.setText(userName)
                self.lineEditAllUsersUserEmail.setText(userEmail)

        elif len(foundNames) > 1:
            if nameIndex == -1:
                i=0
                while i < len(foundNames):
                    userID = (foundNames[i]['userID'])
                    getUser = (userDB.search(DBquery.userID == userID)) 
                    userName = (getUser[0]['firstName']) + " " + (getUser[0]['lastName'])
                    userNameList.append(userName)
                    i += 1
                
                if self.groupBoxHist.isHidden() and self.groupBoxAllUsers.isHidden():
                    self.listWidgetBOUserName.clear()
                    self.listWidgetBOUserName.addItems(userNameList)
                    self.listWidgetBOUserName.show()

                elif self.groupBoxBO.isHidden() and self.groupBoxAllUsers.isHidden():
                    self.listWidgetHistUserName.clear()
                    self.listWidgetHistUserName.addItems(userNameList)
                    self.listWidgetHistUserName.show()

                elif self.groupBoxHist.isHidden() and self.groupBoxBO.isHidden():
                    self.listWidgetAllUsersUserName.clear()
                    self.listWidgetAllUsersUserName.addItems(userNameList)
                    self.listWidgetAllUsersUserName.show()

            else:
                userID = (foundNames[nameIndex]['userID'])
                getUser = (userDB.search(DBquery.userID == userID)) 
                userName = (getUser[0]['firstName']) + " " + (getUser[0]['lastName'])
                userEmail = (getUser[0]['email'])

                if self.groupBoxHist.isHidden() and self.groupBoxAllUsers.isHidden():
                    self.lineEditBOUserID.setText(userID)
                    self.lineEditBOUserName.setText(userName)
                    self.lineEditBOUserEmail.setText(userEmail)
                    self.lineEditBOItemID.setFocus()

                elif self.groupBoxBO.isHidden() and self.groupBoxAllUsers.isHidden():
                    self.lineEditHistUserID.setText(userID)
                    self.lineEditHistUserName.setText(userName)
                    self.lineEditHistUserEmail.setText(userEmail)
                    self.lineEditHistItemID.setFocus()

                elif self.groupBoxHist.isHidden() and self.groupBoxBO.isHidden():
                    self.lineEditAllUsersUserID.setText(userID)
                    self.lineEditAllUsersUserName.setText(userName)
                    self.lineEditAllUsersUserEmail.setText(userEmail)
                    self.lineEditAllUsersUserID.setFocus()

        else:
            self.doMessage("No user found")
            self.lineEditBOUserName.setText("")
            self.lineEditHistUserName.setText("")

        return userID, userName, userEmail
    
    def getUserFromEmail(self, nameIndex):
        global userEmailList

        userEmailList = []
        userID = ""
        userName = ""
        userEmail = ""
        foundNames = ""

        if self.groupBoxHist.isHidden() and self.groupBoxAllUsers.isHidden():
            emails = self.lineEditBOUserEmail.text()
        elif self.groupBoxBO.isHidden() and self.groupBoxAllUsers.isHidden():
            emails = self.lineEditHistUserEmail.text()
        elif self.groupBoxHist.isHidden() and self.groupBoxBO.isHidden():
            emails = self.lineEditAllUsersUserEmail.text()



        foundEmails = userDB.search(DBquery.email.search(emails + '+', flags=re.IGNORECASE))
        
        if len(foundEmails) == 1:
            userID = (foundEmails[0]['userID'])
            userName = (foundEmails[0]['firstName']) + " " + (foundEmails[0]['lastName'])
            userEmail = (foundEmails[0]['email'])

            if self.groupBoxHist.isHidden() and self.groupBoxAllUsers.isHidden():
                self.lineEditBOUserID.setText(userID)
                self.lineEditBOUserName.setText(userName)
                self.lineEditBOUserEmail.setText(userEmail)
                self.lineEditBOItemID.setFocus()

            elif self.groupBoxBO.isHidden() and self.groupBoxAllUsers.isHidden():
                self.lineEditHistUserID.setText(userID)
                self.lineEditHistUserName.setText(userName)
                self.lineEditHistUserEmail.setText(userEmail)
                self.lineEditHistItemID.setFocus()

            elif self.groupBoxHist.isHidden() and self.groupBoxBO.isHidden():
                self.lineEditAllUsersUserID.setText(userID)
                self.lineEditAllUsersUserName.setText(userName)
                self.lineEditAllUsersUserEmail.setText(userEmail)
            

        elif len(foundEmails) > 1:
            if nameIndex == -1:
                i=0
                while i < len(foundEmails):
                    userID = (foundEmails[i]['userID'])
                    getUser = (userDB.search(DBquery.userID == userID)) 
                    userName = (getUser[0]['firstName']) + " " + (getUser[0]['lastName'])
                    userEmail = (getUser[0]['email'])
                    userEmailList.append(userEmail)
                    i += 1
                
                if self.groupBoxHist.isHidden() and self.groupBoxAllUsers.isHidden():
                    self.listWidgetBOUserEmail.clear()
                    self.listWidgetBOUserEmail.addItems(userEmailList)
                    self.listWidgetBOUserEmail.show()

                elif self.groupBoxBO.isHidden() and self.groupBoxAllUsers.isHidden():
                    self.listWidgetHistEmail.clear()
                    self.listWidgetHistEmail.addItems(userEmailList)
                    self.listWidgetHistEmail.show()

                elif self.groupBoxHist.isHidden() and self.groupBoxBO.isHidden():
                    self.listWidgetAllUsersUserEmail.clear()
                    self.listWidgetAllUsersUserEmail.addItems(userEmailList)
                    self.listWidgetAllUsersUserEmail.show()
            
            else:
                userID = (foundEmails[nameIndex]['userID'])
                getUser = (userDB.search(DBquery.userID == userID))
                userName = (getUser[0]['firstName']) + " " + (getUser[0]['lastName'])
                userEmail = (getUser[0]['email'])

                if self.groupBoxHist.isHidden() and self.groupBoxAllUsers.isHidden():
                    self.lineEditBOUserID.setText(userID)
                    self.lineEditBOUserName.setText(userName)
                    self.lineEditBOUserEmail.setText(userEmail)
                    self.lineEditBOItemID.setFocus()

                elif self.groupBoxBO.isHidden() and self.groupBoxAllUsers.isHidden():
                    self.lineEditHistUserID.setText(userID)
                    self.lineEditHistUserName.setText(userName)
                    self.lineEditHistUserEmail.setText(userEmail)
                    self.lineEditHistItemID.setFocus()

                elif self.groupBoxHist.isHidden() and self.groupBoxBO.isHidden():
                    self.lineEditAllUsersUserID.setText(userID)
                    self.lineEditAllUsersUserName.setText(userName)
                    self.lineEditAllUsersUserEmail.setText(userEmail)
                    self.lineEditAllUsersUserID.setFocus()


        else:
            self.doMessage("No user found")
            self.lineEditBOUserEmail.setText("")
            self.lineEditHistUserEmail.setText("")
            self.lineEditAllUsersUserEmail.setText("")

        return userID, userName, userEmail

    def getItemFromID(self):
        global historyItemID

        historyItemID = self.lineEditHistItemID.text()
        self.refreshHistory()



    def listItemBOClicked(self, item):
        self.listWidgetBOUserName.hide()
        nameIndex = self.listWidgetBOUserName.currentRow()
        self.getUserFromName(nameIndex)

    def listItemEmailBOClicked(self, item):
        self.listWidgetBOUserEmail.hide()
        nameIndex = self.listWidgetBOUserEmail.currentRow()
        self.getUserFromEmail(nameIndex)

    def listItemHistClicked(self, item):
        global historyUserEmail
        self.listWidgetHistUserName.hide()
        nameIndex = self.listWidgetHistUserName.currentRow()
        self.getUserFromName(nameIndex)

        historyUserEmail = self.lineEditHistUserEmail.text()
        self.refreshHistory()

    def listItemEmailHistClicked(self, item):
        self.listWidgetHistEmail.hide()
        nameIndex = self.listWidgetHistEmail.currentRow()
        self.getUserFromEmail(nameIndex)
        self.refreshHistory()

    def listItemAllUsersClicked(self, item):
        self.listWidgetAllUsersUserName.hide()
        nameIndex = self.listWidgetAllUsersUserName.currentRow()
        self.getUserFromName(nameIndex)

    def listItemEmailAllUsersClicked(self, item):
        global allUsersSearchID
        global allUsersSearchName
        global allUsersSearchEmail

        allUsersSearchID = ""
        allUsersSearchName = ""

        self.listWidgetAllUsersUserEmail.hide()
        nameIndex = self.listWidgetAllUsersUserEmail.currentRow()
        self.getUserFromEmail(nameIndex)

        allUsersSearchEmail = self.lineEditAllUsersUserEmail.text()
        self.refreshAllUsers()

    def showLongTerm(self):
        global showLongTerm

        if self.checkBoxBkdO.isChecked():
            showLongTerm = True
            self.populateBookedOut()
        else:
            showLongTerm = False
            self.populateBookedOut()

    def clearHist(self):
        global historyItemID
        global historyUserEmail

        historyItemID = ""
        historyUserEmail = ""

        self.lineEditHistItemID.setText("")
        self.lineEditHistUserID.setText("")
        self.lineEditHistUserName.setText("")
        self.lineEditHistUserEmail.setText("")
        self.refreshHistory()

    def resetDateHist(self):
        global dateRangeFrom
        global dateRangeTo

        currentDate = QtCore.QDate.currentDate()

        self.dateEditFrom.setDate(currentDate.addDays(-28))
        self.dateEditTo.setDate(currentDate)

        self.refreshHistory()
        
    def keyItemID(self):
        tempItemInput = self.lineEditBOItemID.text()
        listLength = self.tableWidgetBO.rowCount()

        chkBoxItem = QtWidgets.QTableWidgetItem()
        chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
        
        if listLength > 0:
            i=0
            while i < listLength:                                                           # Iterate through rows
                lineData = self.tableWidgetBO.model().index(i, 1)
                itemID = lineData.data()                

                if itemID == tempItemInput:                                                 # If itemID found in list
                    self.doMessage("Duplicate item")
                    self.lineEditBOItemID.setText("")
                    return                                                                  # Cancel adding to list
                i +=1                                                                       # Iterate i

        tempItemName = (itemDB.search(DBquery.itemID == tempItemInput))                     # search for item number in item database
        if tempItemName == "" or tempItemName == []:                                        # If text input blank
            self.doMessage("Item not found")
            self.lineEditBOItemID.setText("")

        else:
            self.tableWidgetBO.insertRow(0)
            self.tableWidgetBO.setItem(0 , 0, chkBoxItem)
            self.tableWidgetBO.setItem(0 , 1, QtWidgets.QTableWidgetItem(tempItemInput))
            self.tableWidgetBO.setItem(0 , 2, QtWidgets.QTableWidgetItem(tempItemName[0]['itemName']))
            self.tableWidgetBO.setItem(0 , 3, QtWidgets.QTableWidgetItem(tempItemName[0]['itemMake']))
            self.tableWidgetBO.setItem(0 , 4, QtWidgets.QTableWidgetItem(tempItemName[0]['itemModel']))
            self.tableWidgetBO.setItem(0 , 5, QtWidgets.QTableWidgetItem(tempItemName[0]['itemSerial']))
            self.lineEditBOItemID.setText("")


    def doMessage(self, message):
        self.lineEditBOMessage.setText(message)
        self.lineEditReMessage.setText(message)
        self.lineEditHistMessage.setText(message)
        self.lineEditAllItemsMessage.setText(message)
        self.lineEditAddUserMessage.setText(message)
        self.lineEditAddItemMessage.setText(message)
        QtCore.QTimer.singleShot(2000, self.resetMessage)

    def resetMessage(self):
        self.lineEditBOMessage.setText("")
        self.lineEditReMessage.setText("")
        self.lineEditHistMessage.setText("")
        self.lineEditAllItemsMessage.setText("")
        self.lineEditAddUserMessage.setText("")
        self.lineEditAddItemMessage.setText("")

    def clearPrev(self):
        self.tableWidgetBO.removeRow(0)

    def clearAll(self):
        self.tableWidgetBO.setRowCount(0)

    def cancelBO(self):
        self.tableWidgetBO.setRowCount(0)
        self.lineEditBOUserID.setText("")
        self.lineEditBOUserName.setText("")
        self.lineEditBOUserEmail.setText("")
        self.lineEditBOUserID.setFocus()

        if self.listWidgetBOUserName.isVisible():
            self.listWidgetBOUserName.clear()
            self.listWidgetBOUserName.hide()
            self.lineEditBOUserName.setText("")
            self.lineEditBOUserID.setFocus()

    def processOutgoing(self):
        userData = self.getUserFromID(self.lineEditBOUserID.text())
        userID = userData[0]

        if userData[1] == "":
            self.doMessage("No user found")
            QtCore.QTimer.singleShot(2000, self.resetMessage)
            self.lineEditBOUserID.setText("")
            self.lineEditBOUserID.setFocus()

        else:
            currentDate = datetime.timestamp(datetime.now())
            listLength = self.tableWidgetBO.rowCount()

            if listLength == 0:
                self.doMessage("List empty")

            elif self.lineEditBOUserID.text == "":
                self.doMessage("No User selected")

            else:
                i=0
                while i < listLength:
                    lineData = self.tableWidgetBO.model().index(i, 1)
                    itemID = lineData.data()
                    if self.tableWidgetBO.item(i, 0).checkState() == Qt.CheckState.Unchecked:
                        longTerm = ""
                    else:
                        longTerm = "*"

                    outCheck = (outDB.search(DBquery.itemID == itemID))                                 # Check if item already booked out

                    if not outCheck:                                                                    # If not booked out
                        outDB.insert({'itemID': itemID, 'userID': userID, 'longTerm': longTerm, 'dateID': currentDate})

                    else:                                                                               # If booked out already
                        tempRead = (outDB.search(DBquery.itemID == itemID))                             # Find item in outDB
                        tempUserID = (tempRead[0]['userID'])                                            # Read and store who it was booked out to
                        tempStartDate = (tempRead[0]['dateID'])                                         # Read and store date booked out

                        getUser = (userDB.search(DBquery.userID == tempUserID))
                        tempUserFirst = (getUser[0]['firstName'])
                        tempUserLast = (getUser[0]['lastName'])
                        tempUserEmail = (getUser[0]['email'])

                        outDB.remove(where('itemID') == itemID)                                         # Remove item from outDB

                        historyDB.insert({'itemID': itemID, 
                                        'userID': tempUserID, 
                                        'userFirst': tempUserFirst,                                     # Store name & email in case they're later removed from userDB
                                        'userLast': tempUserLast, 
                                        'email': tempUserEmail,
                                        'startDate': tempStartDate, 
                                        'returnDate': currentDate})                                     # Insert old booking in to historyDB
                        
                        outDB.insert({'itemID': itemID, 'userID': userID, 'longTerm': longTerm, 'dateID': currentDate})

                    i +=1

                self.tableWidgetBO.setRowCount(0)
                self.lineEditBOUserID.setText("")
                self.lineEditBOUserName.setText("")
                self.lineEditBOUserEmail.setText("")
                self.lineEditBOUserID.setFocus()

    def returnItems(self):
        tempItemInput = self.lineEditReItemID.text()
        
        tempItemName = (itemDB.search(DBquery.itemID == tempItemInput))                     # Check item number is in item database

        if tempItemName == "" or tempItemName == []:                                        # If item not in item DB
            self.doMessage("Item doesn't exist")
            self.lineEditReItemID.setText("")

        else:
            tempRead = (outDB.search(DBquery.itemID == tempItemInput))                      # Fine and store item from outDB
            if tempRead == "" or tempRead == []:                                            # If item not in booked out DB
                self.doMessage("Item not booked out")

            else:
                tempStartDateTS = (tempRead[0]['dateID'])                                   # Store date item was booked out
                userID = (tempRead[0]['userID'])                                            # Store userID item was booked out to
                
                getUser = (userDB.search(DBquery.userID == userID))
                userFirst = (getUser[0]['firstName'])
                userLast = (getUser[0]['lastName'])
                userName = (userFirst + " " + userLast)
                userEmail = (getUser[0]['email'])

                getItem = (itemDB.search(DBquery.itemID == tempItemInput)) 
                itemName = (getItem[0]['itemName'])

                tempStartDate = datetime.utcfromtimestamp(tempStartDateTS).strftime('%Y-%m-%d - %H:%M:%S')

                outDB.remove(where('itemID') == tempItemInput)                              # Remove item from outDB
                historyDB.insert({'itemID': tempItemInput,                                  # Insert returned item to historyDB
                                'userID': userID, 
                                'userFirst': userFirst,                                     # Store name & email in case they're later removed from userDB
                                'userLast': userLast, 
                                'email': userEmail,
                                'startDate': tempStartDateTS, 
                                'returnDate': datetime.timestamp(datetime.now())})
                
                rowPosition = self.tableWidgetRe.rowCount()
                self.tableWidgetRe.insertRow(rowPosition)
                self.tableWidgetRe.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(tempItemInput))
                self.tableWidgetRe.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(itemName))
                self.tableWidgetRe.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(userID))
                self.tableWidgetRe.setItem(rowPosition , 3, QtWidgets.QTableWidgetItem(userName))
                self.tableWidgetRe.setItem(rowPosition , 4, QtWidgets.QTableWidgetItem(userEmail))
                self.lineEditReItemID.setText("")

    def populateBookedOut(self):
        global bookedOutPath
        global showLongTerm
        global watchCellChange

        self.tableWidgetBkdO.cellChanged.disconnect(self.onCellChanged)

        watchCellChange = False

        outText = outDB.all()
        DBLength = len(outDB)

        chkBoxItem = QtWidgets.QTableWidgetItem()
        chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        chkBoxItem.setCheckState(QtCore.Qt.Unchecked)

        self.tableWidgetBkdO.setRowCount(0)

        pdf = FPDF('P', 'pt', 'A4')
        pdf.add_page()
        pdf.set_font('helvetica', size=7)

        pdf.set_fill_color(240,240,240)

        pdf.cell(w=30, h=9, txt= "Item ID", fill = True)
        pdf.cell(w=200, h=9, txt= "Item Name", fill = True)
        pdf.cell(w=100, h=9, txt= "User", fill = True)
        pdf.cell(w=120, h=9, txt= "Email", fill = True)
        pdf.cell(w=80, h=9, txt= "Date Out", ln=(1), fill = True)

        i=0
        flipPDFBackground = False

        while i < DBLength:
            itemID = outText[i]['itemID']
            userID = outText[i]['userID']
            dateID = outText[i]['dateID']
            longTerm = outText[i]['longTerm']

            getItem = (itemDB.search(DBquery.itemID == itemID)) 
            itemName = (getItem[0]['itemName'])
            
            userData = self.getUserFromID(userID)
            userName = userData[1]
            userEmail = userData[2]

            dateOut = datetime.utcfromtimestamp(dateID).strftime('%Y-%m-%d - %H:%M:%S')

            if showLongTerm == True and longTerm == "*":
                if flipPDFBackground:
                    pdf.set_fill_color(240,240,240)
                else:
                    pdf.set_fill_color(255,255,255)
                
                pdf.cell(w=30, h=9, txt= itemID, fill = True)
                pdf.cell(w=200, h=9, txt= itemName, fill = True)
                pdf.cell(w=100, h=9, txt= userName, fill = True)
                pdf.cell(w=120, h=9, txt= userEmail, fill = True)
                pdf.cell(w=80, h=9, txt= dateOut, fill = True)
                pdf.cell(w=5, h=9, txt= longTerm, ln=(1), fill = True)

                chkBoxItem.setCheckState(QtCore.Qt.Checked)

                rowPosition = self.tableWidgetBkdO.rowCount()
                self.tableWidgetBkdO.insertRow(rowPosition)
                self.tableWidgetBkdO.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(chkBoxItem))
                self.tableWidgetBkdO.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(itemID))
                self.tableWidgetBkdO.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(itemName))
                self.tableWidgetBkdO.setItem(rowPosition , 3, QtWidgets.QTableWidgetItem(userName))
                self.tableWidgetBkdO.setItem(rowPosition , 4, QtWidgets.QTableWidgetItem(userEmail))
                self.tableWidgetBkdO.setItem(rowPosition , 5, QtWidgets.QTableWidgetItem(dateOut))

            elif longTerm == "":
                if flipPDFBackground:
                    pdf.set_fill_color(240,240,240)
                else:
                    pdf.set_fill_color(255,255,255)
                
                pdf.cell(w=30, h=9, txt= itemID, fill = True)
                pdf.cell(w=200, h=9, txt= itemName, fill = True)
                pdf.cell(w=100, h=9, txt= userName, fill = True)
                pdf.cell(w=120, h=9, txt= userEmail, fill = True)
                pdf.cell(w=80, h=9, txt= dateOut, ln=(1), fill = True)

                chkBoxItem.setCheckState(QtCore.Qt.Unchecked)

                rowPosition = self.tableWidgetBkdO.rowCount()
                self.tableWidgetBkdO.insertRow(rowPosition)
                self.tableWidgetBkdO.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(chkBoxItem))
                self.tableWidgetBkdO.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(itemID))
                self.tableWidgetBkdO.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(itemName))
                self.tableWidgetBkdO.setItem(rowPosition , 3, QtWidgets.QTableWidgetItem(userName))
                self.tableWidgetBkdO.setItem(rowPosition , 4, QtWidgets.QTableWidgetItem(userEmail))
                self.tableWidgetBkdO.setItem(rowPosition , 5, QtWidgets.QTableWidgetItem(dateOut))

            i +=1
            if flipPDFBackground:
                flipPDFBackground = False
            else:
                flipPDFBackground = True

        pdf.output(bookedOutPath)
        
        watchCellChange = True

        self.tableWidgetBkdO.cellChanged.connect(self.onCellChanged)

    def populateAllItems(self):
        global allItemsSearchText
        global allItemsSearchID
        global itemsPath
        
        self.lineEditAllItemSearch.setFocus()

        allItemsSearchText = self.lineEditAllItemSearch.text()
        allItemsSearchID = self.lineEditAllItemsItemID.text()

        if allItemsSearchText != "":
            allItemsTextSearch = itemDB.search(DBquery.itemName.search(allItemsSearchText + '+', flags=re.IGNORECASE))
            allItemsTextSearch += itemDB.search(DBquery.itemMake.search(allItemsSearchText + '+', flags=re.IGNORECASE))
            allItemsTextSearch += itemDB.search(DBquery.itemModel.search(allItemsSearchText + '+', flags=re.IGNORECASE))

            new_list = []
            [new_list.append(item) for item in allItemsTextSearch if item not in new_list]

            allItemsText = new_list

        elif allItemsSearchID != "":
            allItemsText = itemDB.search(DBquery.itemID == allItemsSearchID)
        else:
            allItemsText = itemDB.all()
            
        DBLengthItems = len(allItemsText)

        pdf = FPDF('P', 'pt', 'A4')
        pdf.add_page()
        pdf.set_font('helvetica', size=7)

        pdf.set_fill_color(240,240,240)

        pdf.cell(w=30, h=9, txt= "Item ID", fill = True)
        pdf.cell(w=200, h=9, txt= "Item Name", fill = True)
        pdf.cell(w=100, h=9, txt= "Item Make", fill = True)
        pdf.cell(w=120, h=9, txt= "Item Model", fill = True)
        pdf.cell(w=90, h=9, txt= "Item Serial No.", ln=(1), fill = True)

        self.tableWidgetAllItems.setRowCount(0)

        i=0
        while i < DBLengthItems:
            itemID = allItemsText[i]['itemID']
            itemName = allItemsText[i]['itemName']
            itemMake = allItemsText[i]['itemMake']
            itemModel = allItemsText[i]['itemModel']
            try:
                itemSerial = allItemsText[i]['itemSerial']
            except:
                itemSerial = ""

            if ((i % 2) == 0):
                pdf.set_fill_color(255,255,255)
            else:
                pdf.set_fill_color(240,240,240)
            
            pdf.cell(w=30, h=9, txt= itemID, fill = True)
            pdf.cell(w=200, h=9, txt= itemName, fill = True)
            pdf.cell(w=100, h=9, txt= itemMake, fill = True)
            pdf.cell(w=120, h=9, txt= itemModel, fill = True)
            pdf.cell(w=90, h=9, txt= itemSerial, ln=(1), fill = True)
        
            rowPosition = self.tableWidgetAllItems.rowCount()
            self.tableWidgetAllItems.insertRow(rowPosition)

            self.tableWidgetAllItems.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(itemID))
            self.tableWidgetAllItems.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(itemName))
            self.tableWidgetAllItems.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(itemMake))
            self.tableWidgetAllItems.setItem(rowPosition , 3, QtWidgets.QTableWidgetItem(itemModel))
            self.tableWidgetAllItems.setItem(rowPosition , 4, QtWidgets.QTableWidgetItem(itemSerial))

            i +=1

        pdf.output(itemsPath)

    def clearAllItems(self):
        self.lineEditAllItemSearch.setText("")
        self.lineEditAllItemsItemID.setText("")
        self.populateAllItems()

    def clearAllUsers(self):
        self.lineEditAllUsersUserID.setText("")
        self.lineEditAllUsersUserName.setText("")
        self.lineEditAllUsersUserEmail.setText("")
        self.populateAllUsers()

    def populateAllUsers(self):
        global allUsersSearchID
        global allUsersSearchName
        global allUsersSearchEmail
        
        self.lineEditAllUsersUserID.setFocus()

        allUsersSearchID = self.lineEditAllUsersUserID.text()
        allUsersSearchName = self.lineEditAllUsersUserName.text()
        allUsersSearchEmail = self.lineEditAllUsersUserEmail.text()

        if allUsersSearchID != "":
            allUsersText = userDB.search(DBquery.itemName.search(allUsersSearchID + '+', flags=re.IGNORECASE))
        elif allUsersSearchName != "":
            allUsersText = userDB.search(DBquery.itemName.search(allUsersSearchName + '+', flags=re.IGNORECASE))
        elif allUsersSearchEmail != "":
            allUsersText = userDB.search(DBquery.itemName.search(allUsersSearchEmail + '+', flags=re.IGNORECASE))
        else:
            allUsersText = userDB.all()
            
        DBLengthItems = len(allUsersText)

        pdf = FPDF('P', 'pt', 'A4')
        pdf.add_page()
        pdf.set_font('helvetica', size=7)

        pdf.set_fill_color(240,240,240)

        pdf.cell(w=30, h=9, txt= "User ID", fill = True)
        pdf.cell(w=200, h=9, txt= "User Name", fill = True)
        pdf.cell(w=200, h=9, txt= "User Email", ln=(1), fill = True)

        self.tableWidgetAllUsers.setRowCount(0)

        
        i=0
        while i < DBLengthItems:
            userID = allUsersText[i]['userID']
            userFirst = allUsersText[i]['firstName']
            userLast = allUsersText[i]['lastName']
            userEmail = allUsersText[i]['email']

            userName = (userFirst + " " + userLast)

            if ((i % 2) == 0):
                pdf.set_fill_color(255,255,255)
            else:
                pdf.set_fill_color(240,240,240)
            
            pdf.cell(w=30, h=9, txt= userID, fill = True)
            pdf.cell(w=200, h=9, txt= userName, fill = True)
            pdf.cell(w=200, h=9, txt= userEmail, ln=(1), fill = True)
        
            rowPosition = self.tableWidgetAllUsers.rowCount()
            self.tableWidgetAllUsers.insertRow(rowPosition)

            self.tableWidgetAllUsers.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(userID))
            self.tableWidgetAllUsers.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(userName))
            self.tableWidgetAllUsers.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(userEmail))

            i +=1
        
        pdf.output(usersPath)
        

    def refreshHistory(self):
        global historyPath
        global dateRangeFrom
        global dateRangeTo
        global historyItemID
        global historyUserEmail

        self.tableWidgetHist.setRowCount(0)

        historyUserEmail = self.lineEditHistUserEmail.text()

        dateRangeFrom = self.dateEditFrom.date()
        dateRangeFrom = str(dateRangeFrom.toPython())
        dateRangeFrom = time.mktime(datetime.strptime(dateRangeFrom, "%Y-%m-%d").timetuple())

        dateRangeTo = self.dateEditTo.date()
        dateRangeTo = dateRangeTo.toPython()
        dateRangeTo = str(dateRangeTo + timedelta(days=1))
        dateRangeTo = time.mktime(datetime.strptime(dateRangeTo, "%Y-%m-%d").timetuple())
        
        if historyItemID == "":
            if historyUserEmail == "":
                historyText = historyDB.search((DBquery.startDate > dateRangeFrom) & (DBquery.startDate <= dateRangeTo))
            else:
                historyText = historyDB.search((DBquery.startDate > dateRangeFrom) & (DBquery.startDate <= dateRangeTo) & (DBquery.email == historyUserEmail))
        else:
            historyText = historyDB.search((DBquery.startDate > dateRangeFrom) & (DBquery.startDate <= dateRangeTo) & (DBquery.itemID == historyItemID))

        DBLength = len(historyText)

        pdf = FPDF('P', 'pt', 'A4')
        pdf.add_page()
        pdf.set_font('helvetica', size=7)

        pdf.set_fill_color(240,240,240)

        pdf.cell(w=30, h=9, txt= "Item ID", fill = True)
        pdf.cell(w=200, h=9, txt= "Item Name", fill = True)
        pdf.cell(w=100, h=9, txt= "User", fill = True)
        pdf.cell(w=120, h=9, txt= "Email", fill = True)
        pdf.cell(w=45, h=9, txt= "Date Out", fill = True)
        pdf.cell(w=45, h=9, txt= "Date In", ln=(1), fill = True)

        i=0
        while i < DBLength:
            itemID = historyText[i]['itemID']
            userID = historyText[i]['userID']
            userFirst = historyText[i]['userFirst']
            userLast = historyText[i]['userLast']
            userEmail = historyText[i]['email']
            startDate = historyText[i]['startDate']
            returnDate = historyText[i]['returnDate']

            getItem = (itemDB.search(DBquery.itemID == itemID))

            if getItem == "" or getItem == []:
                pass
            else:
                itemName = (getItem[0]['itemName'])

            userName = (userFirst + " " + userLast)

            dateOut = datetime.utcfromtimestamp(startDate).strftime('%Y-%m-%d')
            dateIn = datetime.utcfromtimestamp(returnDate).strftime('%Y-%m-%d')

            if ((i % 2) == 0):
                pdf.set_fill_color(255,255,255)
            else:
                pdf.set_fill_color(240,240,240)
            
            pdf.cell(w=30, h=9, txt= itemID, fill = True)
            pdf.cell(w=200, h=9, txt= itemName, fill = True)
            pdf.cell(w=100, h=9, txt= userName, fill = True)
            pdf.cell(w=120, h=9, txt= userEmail, fill = True)
            pdf.cell(w=45, h=9, txt= dateOut, fill = True)
            pdf.cell(w=45, h=9, txt= dateIn, ln=(1), fill = True)

            rowPosition = self.tableWidgetHist.rowCount()
            self.tableWidgetHist.insertRow(rowPosition)

            self.tableWidgetHist.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(itemID))
            self.tableWidgetHist.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(itemName))
            self.tableWidgetHist.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(userName))
            self.tableWidgetHist.setItem(rowPosition , 3, QtWidgets.QTableWidgetItem(userEmail))
            self.tableWidgetHist.setItem(rowPosition , 4, QtWidgets.QTableWidgetItem(dateOut))
            self.tableWidgetHist.setItem(rowPosition , 5, QtWidgets.QTableWidgetItem(dateIn))

            i +=1

        pdf.output(historyPath)

    def refreshAllUsers(self):
        global allUsersSearchID
        global allUsersSearchName
        global allUsersSearchEmail
        global usersPath

        self.tableWidgetAllUsers.setRowCount(0)

        #historyUserEmail = self.lineEditHistUserEmail.text()
        
        if allUsersSearchID == "":
            if allUsersSearchName == "":
                allUsersText = (userDB.search(DBquery.email == allUsersSearchEmail))
            else:
                allUsersText = (userDB.search(DBquery.email == allUsersSearchEmail))
        else:
            allUsersText = (userDB.search(DBquery.userID == allUsersSearchID))

        DBLength = len(allUsersText)

        #pdf = FPDF('P', 'pt', 'A4')
        #pdf.add_page()
        #pdf.set_font('helvetica', size=7)

        #pdf.set_fill_color(240,240,240)

        #pdf.cell(w=30, h=9, txt= "Item ID", fill = True)
        #pdf.cell(w=200, h=9, txt= "Item Name", fill = True)
        #pdf.cell(w=100, h=9, txt= "User", fill = True)
        #pdf.cell(w=120, h=9, txt= "Email", fill = True)
        #pdf.cell(w=45, h=9, txt= "Date Out", fill = True)
        #pdf.cell(w=45, h=9, txt= "Date In", ln=(1), fill = True)

        i=0
        while i < DBLength:
            userID = allUsersText[i]['userID']
            userFirst = allUsersText[i]['firstName']
            userLast = allUsersText[i]['lastName']
            userEmail = allUsersText[i]['email']

            userName = (userFirst + " " + userLast)

            #if ((i % 2) == 0):
            #    pdf.set_fill_color(255,255,255)
            #else:
            #    pdf.set_fill_color(240,240,240)
            
            #pdf.cell(w=30, h=9, txt= itemID, fill = True)
            #pdf.cell(w=200, h=9, txt= itemName, fill = True)
            #pdf.cell(w=100, h=9, txt= userName, fill = True)
            #pdf.cell(w=120, h=9, txt= userEmail, fill = True)
            #pdf.cell(w=45, h=9, txt= dateOut, fill = True)
            #pdf.cell(w=45, h=9, txt= dateIn, ln=(1), fill = True)

            rowPosition = self.tableWidgetAllUsers.rowCount()
            self.tableWidgetAllUsers.insertRow(rowPosition)

            self.tableWidgetAllUsers.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(userID))
            self.tableWidgetAllUsers.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(userName))
            self.tableWidgetAllUsers.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(userEmail))

            i +=1

        #pdf.output(usersPath)

    def addUserIDCheck(self):
        userID = self.lineEditAddUserID.text()
        userIDSearch = (userDB.search(DBquery.userID == userID))

        if userIDSearch != []:
            self.doMessage("User ID Already Used")
        
            userFirstName = (userIDSearch[0]['firstName'])
            userLastName = (userIDSearch[0]['lastName'])
            userEmail = (userIDSearch[0]['email'])

            self.lineEditAddUserFirst.setText(userFirstName)
            self.lineEditAddUserLast.setText(userLastName)
            self.lineEditAddUserEmail.setText(userEmail)
            return

        self.doMessage("user ID Available")
        self.lineEditAddUserFirst.setFocus()

    def addUserFirstCheck(self):
        self.lineEditAddUserLast.setFocus()

    def addUserLastCheck(self):
        self.lineEditAddUserEmail.setFocus()

    def addUserEmailCheck(self):
        self.addUserSave()

    def addUserSave(self):
        addUserID = self.lineEditAddUserID.text()
        addUserFirstName = self.lineEditAddUserFirst.text()
        addUserLastName = self.lineEditAddUserLast.text()
        addUserEmail = self.lineEditAddUserEmail.text()
        
        itemIDSearch = (userDB.search(DBquery.userID == addUserID))

        if itemIDSearch != []:
            userDB.update({'userID': addUserID,                                                             # Insert returned item to itemDB
                        'firstName': addUserFirstName, 
                        'lastName': addUserLastName, 
                        'email': addUserEmail}, DBquery.userID == addUserID)
            
            self.doMessage("User updated")

            self.lineEditAddUserID.setText("")
            self.lineEditAddUserFirst.setText("")
            self.lineEditAddUserLast.setText("")
            self.lineEditAddUserEmail.setText("")

            self.lineEditAddUserID.setFocus()
            return

        userDB.insert({'userID': addUserID,                                                             # Insert returned item to itemDB
                        'firstName': addUserFirstName, 
                        'lastName': addUserLastName, 
                        'email': addUserEmail})
        
        self.doMessage("User added")

        self.lineEditAddUserID.setText("")
        self.lineEditAddUserFirst.setText("")
        self.lineEditAddUserLast.setText("")
        self.lineEditAddUserEmail.setText("")
        
        self.lineEditAddUserID.setFocus()

    def addUserClear(self):
        self.lineEditAddUserID.setText("")
        self.lineEditAddUserFirst.setText("")
        self.lineEditAddUserLast.setText("")
        self.lineEditAddUserEmail.setText("")
        self.lineEditAddUserID.setFocus()

    def addUserAdminImport(self):
        if isWindows:
            fname = QFileDialog.getOpenFileName(self, "Open Config", "C:\\Users\\Public\\Documents\\Database", "CSV (*.csv)")
        else:
            fname = QFileDialog.getOpenFileName(self, "Open Config", '/Users/Shared/Database/', "CSV (*.csv)")

        if fname:
            filename = fname[0]
            try:
                with open(filename, encoding='utf-8-sig') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count_added = 0
                    line_count_skipped = 0

                    for row in csv_reader:
                        userIDSearch = (userDB.search(DBquery.userID == row[0]))

                        if userIDSearch == []:
                            row[1] = row[1].replace(' ', '-')
                            row[2] = row[2].replace(' ', '-')
                            userDB.insert({'userID': row[0],
                                            'firstName': row[1], 
                                            'lastName': row[2], 
                                            'email': row[3]})
                            line_count_added += 1
                        else:
                            line_count_skipped += 1
                
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText("%s Users added\n%s Users skipped" %(line_count_added, line_count_skipped))
                msgBox.setWindowTitle("Import Complete")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()

            except:
                self.doMessage("Couldn't Load File")
        

    def addItemIDCheck(self):
        itemID = self.lineEditAddItemID.text()
        itemIDSearch = (itemDB.search(DBquery.itemID == itemID))

        if itemIDSearch != []:
            self.doMessage("Item ID Already Used")
            
            itemName = (itemIDSearch[0]['itemName'])
            itemMake = (itemIDSearch[0]['itemMake'])
            itemModel = (itemIDSearch[0]['itemModel'])
            itemSerial = (itemIDSearch[0]['itemSerial'])

            self.lineEditAddItemName.setText(itemName)
            self.lineEditAddItemMake.setText(itemMake)
            self.lineEditAddItemModel.setText(itemModel)
            self.lineEditAddItemSerial.setText(itemSerial)
            return

        self.doMessage("Item ID Available")
        self.lineEditAddItemSerial.setFocus()

    def addItemSerial(self):
        self.lineEditAddItemName.setFocus()
    
    def addItemName(self):
        self.lineEditAddItemMake.setFocus()
    
    def addItemMake(self):
        self.lineEditAddItemModel.setFocus()
    
    def addItemModel(self):
        pass

    def addItemSave(self):
        addItemID = self.lineEditAddItemID.text()
        addItemName = self.lineEditAddItemName.text()
        addItemMake = self.lineEditAddItemMake.text()
        addItemModel = self.lineEditAddItemModel.text()
        addItemSerial = self.lineEditAddItemSerial.text()
        
        itemID = self.lineEditAddItemID.text()
        itemIDSearch = (itemDB.search(DBquery.itemID == itemID))

        if itemIDSearch != []:
            itemDB.update({'itemID': addItemID,                                                             # Insert returned item to itemDB
                        'itemName': addItemName, 
                        'itemMake': addItemMake, 
                        'itemModel': addItemModel, 
                        'itemSerial': addItemSerial}, DBquery.itemID == addItemID)
            
            self.doMessage("Item updated")

            self.lineEditAddItemID.setText("")
            self.lineEditAddItemName.setText("")
            self.lineEditAddItemMake.setText("")
            self.lineEditAddItemModel.setText("")
            self.lineEditAddItemSerial.setText("")

            self.lineEditAddItemID.setFocus()
            return


        if addItemID != "":
            itemDB.insert({'itemID': addItemID,                                                             # Insert returned item to itemDB
                            'itemName': addItemName, 
                            'itemMake': addItemMake, 
                            'itemModel': addItemModel, 
                            'itemSerial': addItemSerial})
            
            self.doMessage("Item added")
            self.lineEditAddItemID.setText("")
            self.lineEditAddItemSerial.setText("")
            self.lineEditAddItemID.setFocus()
        else:
            self.doMessage("No Item ID provided")
            self.lineEditAddItemID.setFocus()

    def addItemClear(self):
        self.lineEditAddItemID.setText("")
        self.lineEditAddItemName.setText("")
        self.lineEditAddItemMake.setText("")
        self.lineEditAddItemModel.setText("")
        self.lineEditAddItemSerial.setText("")
        self.lineEditAddItemID.setFocus()

    def deleteItem(self):
        itemID = self.lineEditAddItemID.text()
        if itemID == "":
            self.lineEditAddItemID.setFocus()
            return
        
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Confirm Delete")
        dlg.setText("Confirm Delete?")
        detail = "Item ID = %s" % (itemID)
        dlg.setDetailedText(detail) 

        dlg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        dlg.setDefaultButton(QMessageBox.No) 
        dlg.setStyleSheet("background-color: rgb(0, 0, 0);color: rgb(255, 255, 255);")

        button = dlg.exec()

        if button == QMessageBox.Yes:
            print("Delete", itemID)
            
            outCheck = (outDB.search(DBquery.itemID == itemID))                                 # Check if item already booked out

            if not outCheck:                                                                    # If not booked out
                itemDB.remove(DBquery.itemID == itemID)

            else:                                                                               # If booked out already
                currentDate = datetime.timestamp(datetime.now())

                tempRead = (outDB.search(DBquery.itemID == itemID))                             # Find item in outDB
                tempUserID = (tempRead[0]['userID'])                                            # Read and store who it was booked out to
                tempStartDate = (tempRead[0]['dateID'])                                         # Read and store date booked out

                getUser = (userDB.search(DBquery.userID == tempUserID))
                tempUserFirst = (getUser[0]['firstName'])
                tempUserLast = (getUser[0]['lastName'])
                tempUserEmail = (getUser[0]['email'])

                outDB.remove(where('itemID') == itemID)                                         # Remove item from outDB

                historyDB.insert({'itemID': itemID, 
                                'userID': tempUserID, 
                                'userFirst': tempUserFirst,                                     # Store name & email in case they're later removed from userDB
                                'userLast': tempUserLast, 
                                'email': tempUserEmail,
                                'startDate': tempStartDate, 
                                'returnDate': currentDate})                                     # Insert old booking in to historyDB

                itemDB.remove(where('itemID') == itemID)

            #self.lineEditAddItemID.setText("")
            self.addItemClear()
            self.doMessage("Item Deleted")

        else:
            print("Cancelled")


    def openWindowAddItemAdmin(self):
        self.pushButtonBookOut.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonReturn.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonBookedOut.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonHistory.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.hide()
        self.pushButtonAllItemsAllItems.show()
        self.pushButtonAllItemsAddItem.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonAllItemsAddItem.show()
        #self.pushButtonUsers.setStyleSheet("border: 4px solid #aa3333; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonUsers.show()
        self.pushButtonAllUsersAllUsers.hide()
        self.pushButtonAllUsersAddUser.hide()
        self.groupBoxBO.hide()
        self.groupBoxRe.hide()
        self.groupBoxBkdO.hide()
        self.groupBoxHist.hide()
        self.groupBoxAllItemsOuter.hide()
        self.groupBoxAllItems.hide()
        self.groupBoxAddItem.hide()
        self.groupBoxUsersOuter.show()
        self.groupBoxAllUsers.hide()
        self.groupBoxAddUser.hide()
        self.groupBoxAddUserAdmin.hide()
        #self.groupBoxAddItemAdmin.show()

    def exportBooked(self):
        global isWindows
        global bookedOutPath

        if isWindows:
            os.startfile(bookedOutPath)
        else:
            subprocess.run(['open', bookedOutPath], check=True)

    def exportHistory(self):
        global isWindows
        global historyPath

        if isWindows:
            os.startfile(historyPath)
        else:
            subprocess.run(['open', historyPath], check=True)

    def exportItems(self):
        global isWindows
        global itemsPath

        if isWindows:
            os.startfile(itemsPath)
        else:
            subprocess.run(['open', itemsPath], check=True)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = databaseApp("")
    sys.exit(app.exec_())
