
# Windows
# python -m pip install pyqt5
# python -m pip install tinydb
# python -m pip install fpdf
# python -m pip install pyinstaller
# python -m PyInstaller --onefile --windowed --icon="dbIcon.ico" LibraryDatabase.py

# macOS
# python3 -m pip install pyqt5
# python3 -m pip install tinydb
# python3 -m pip install fpdf
# python3 -m pip install pyinstaller


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
import time
from datetime import datetime
from datetime import timedelta
from tinydb import TinyDB
from tinydb import Query
from tinydb import where
from fpdf import FPDF
import sys, time, re, os, subprocess

showLongTerm = False
watchCellChange = True

dateRangeFrom = 0.0
dateRangeTo = 0.0
historyItemID = ""
historyUserEmail = ""
allItemsSearchText = ""
allItemsSearchID = ""

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


    bookedOutPath = 'C:\\Users\\Public\\Documents\\Database\\BookedOut.json'
    f = open(bookedOutPath, 'a')  # open file, create if doesn't exist
    f.close()

    historyPath = 'C:\\Users\\Public\\Documents\\Database\\History.json'
    f = open(historyPath, 'a')  # open file, create if doesn't exist
    f.close()

    itemsPath = 'C:\\Users\\Public\\Documents\\Database\\Items.json'
    f = open(itemsPath, 'a')  # open file, create if doesn't exist
    f.close()

    #itemDB = TinyDB('C:\\Users\\Public\\Documents\\Database\\itemdb.json')
    #userDB = TinyDB('C:\\Users\\Public\\Documents\\Database\\userdb.json')
    #outDB = TinyDB('C:\\Users\\Public\\Documents\\Database\\outdb.json')
    #historyDB = TinyDB('C:\\Users\\Public\\Documents\\Database\\historydb.json')
    #bookedOutPath = 'C:\\Users\\Public\\Documents\\Database\\BookedOut.pdf'
    #historyPath = 'C:\\Users\\Public\\Documents\\Database\\History.pdf'
    #itemsPath = 'C:\\Users\\Public\\Documents\\Database\\Items.pdf'
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


    bookedOutPath = '/Users/Shared/Database/BookedOut.json'
    f = open(bookedOutPath, 'a')  # open file, create if doesn't exist
    f.close()

    historyPath = '/Users/Shared/Database/History.json'
    f = open(historyPath, 'a')  # open file, create if doesn't exist
    f.close()

    itemsPath = '/Users/Shared/Database/Items.json'
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
                if self.listWidgetBOName.isVisible():
                    self.listWidgetBOName.clear()
                    self.listWidgetBOName.hide()
                    self.lineEditBOStudentName.setText("")
                    self.lineEditBOStudentID.setFocus()

        return super(databaseApp, self).eventFilter(obj, event)

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1806, 1035)
        self.setStyleSheet("background-color: #080e13;")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBoxMenu = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxMenu.setGeometry(QtCore.QRect(20, 0, 1761, 81))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)


        # Top Menu
        self.groupBoxMenu.setFont(font)
        self.groupBoxMenu.setStyleSheet("background-color: #181e23; border: 0px solid #000;")
        self.groupBoxMenu.setTitle("")
        self.groupBoxMenu.setObjectName("groupBoxMenu")
        self.pushButtonBookOut = QtWidgets.QPushButton(self.groupBoxMenu, clicked = lambda: self.openWindowBookOut())
        self.pushButtonBookOut.setGeometry(QtCore.QRect(10, 10, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonBookOut.setFont(font)
        self.pushButtonBookOut.setStyleSheet("border: 4px solid #aa3333; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonBookOut.setObjectName("pushButtonBookOut")
        self.pushButtonReturn = QtWidgets.QPushButton(self.groupBoxMenu, clicked = lambda: self.openWindowReturn())
        self.pushButtonReturn.setGeometry(QtCore.QRect(240, 10, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonReturn.setFont(font)
        self.pushButtonReturn.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonReturn.setObjectName("pushButtonReturn")
        self.pushButtonBookedOut = QtWidgets.QPushButton(self.groupBoxMenu, clicked = lambda: self.openWindowBookedOut())
        self.pushButtonBookedOut.setGeometry(QtCore.QRect(660, 10, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonBookedOut.setFont(font)
        self.pushButtonBookedOut.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonBookedOut.setObjectName("pushButtonBookedOut")
        self.pushButtonHistory = QtWidgets.QPushButton(self.groupBoxMenu, clicked = lambda: self.openWindowHistory())
        self.pushButtonHistory.setGeometry(QtCore.QRect(890, 10, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonHistory.setFont(font)
        self.pushButtonHistory.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonHistory.setObjectName("pushButtonHistory")
        self.pushButtonItems = QtWidgets.QPushButton(self.groupBoxMenu, clicked = lambda: self.openWindowItems())
        self.pushButtonItems.setGeometry(QtCore.QRect(1310, 10, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonItems.setFont(font)
        self.pushButtonItems.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.setObjectName("pushButtonItems")
        self.pushButtonUsers = QtWidgets.QPushButton(self.groupBoxMenu, clicked = lambda: self.openWindowUser())
        self.pushButtonUsers.setGeometry(QtCore.QRect(1540, 10, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonUsers.setFont(font)
        self.pushButtonUsers.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonUsers.setObjectName("pushButtonUsers")


        # Book Out
        self.groupBoxBO = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxBO.setGeometry(QtCore.QRect(20, 100, 1761, 871))
        self.groupBoxBO.setStyleSheet("background-color: #181e23; border: 0px solid #000;")
        self.groupBoxBO.setTitle("")
        self.groupBoxBO.setObjectName("groupBoxBO")

        self.tableWidgetBO = QtWidgets.QTableWidget(self.groupBoxBO)
        self.tableWidgetBO.setGeometry(QtCore.QRect(190, 90, 1561, 771))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetBO.sizePolicy().hasHeightForWidth())
        self.tableWidgetBO.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.tableWidgetBO.setFont(font)
        self.tableWidgetBO.setAutoFillBackground(False)
        #self.tableWidgetBO.setStyleSheet("alternate-background-color: #282e33; background-color: #181e23; color: white; QHeaderView::section { color: white; background-color: #747678;    gridline-color: #747678; };")
        styleSheet = """
QTableView {
    background-color: #181e23;
    alternate-background-color: #282e33;
    border: 1px solid black;
    gridline-color: black;
    font-size: 18;
    color: white;
}

QHeaderView {
    background-color: #444;
    color: #444
}

QHeaderView::section {
    background-color: #444;
    color: white;
    font-size: 24px;
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
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidgetBO.setHorizontalHeaderItem(0, item)
        self.tableWidgetBO.setColumnWidth(0, 120)
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QtGui.QColor("black"))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidgetBO.setHorizontalHeaderItem(1, item)
        self.tableWidgetBO.setColumnWidth(1, 120)
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QtGui.QColor("white"))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidgetBO.setHorizontalHeaderItem(2, item)
        self.tableWidgetBO.setColumnWidth(2, 570)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidgetBO.setHorizontalHeaderItem(3, item)
        self.tableWidgetBO.setColumnWidth(3, 200)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidgetBO.setHorizontalHeaderItem(4, item)
        self.tableWidgetBO.setColumnWidth(4, 280)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidgetBO.setHorizontalHeaderItem(5, item)
        self.tableWidgetBO.setColumnWidth(5, 260)
        self.tableWidgetBO.verticalHeader().setVisible(True)
        self.tableWidgetBO.verticalHeader().setHighlightSections(True)
        self.pushButtonBOClear = QtWidgets.QPushButton(self.groupBoxBO, clicked = lambda: self.clearAll())
        self.pushButtonBOClear.setGeometry(QtCore.QRect(20, 300, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(20)
        self.pushButtonBOClear.setFont(font)
        self.pushButtonBOClear.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonBOClear.setObjectName("pushButtonBOClear")
        self.pushButtonBOClearLast = QtWidgets.QPushButton(self.groupBoxBO, clicked = lambda: self.clearPrev())
        self.pushButtonBOClearLast.setGeometry(QtCore.QRect(20, 230, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(20)
        self.pushButtonBOClearLast.setFont(font)
        self.pushButtonBOClearLast.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonBOClearLast.setObjectName("pushButtonBOClearLast")
        self.pushButtonBOCancel = QtWidgets.QPushButton(self.groupBoxBO, clicked = lambda: self.cancelBO())
        self.pushButtonBOCancel.setGeometry(QtCore.QRect(20, 700, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(20)
        self.pushButtonBOCancel.setFont(font)
        self.pushButtonBOCancel.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonBOCancel.setObjectName("pushButtonBOCancel")
        self.pushButtonBOSubmit = QtWidgets.QPushButton(self.groupBoxBO, clicked = lambda: self.processOutgoing())
        self.pushButtonBOSubmit.setGeometry(QtCore.QRect(20, 790, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(20)
        self.pushButtonBOSubmit.setFont(font)
        self.pushButtonBOSubmit.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonBOSubmit.setObjectName("pushButtonBOSubmit")
        self.lineEditBOStudentID = QtWidgets.QLineEdit(self.groupBoxBO)
        self.lineEditBOStudentID.returnPressed.connect(lambda: self.getUserFromID(0))
        self.lineEditBOStudentID.setGeometry(QtCore.QRect(240, 30, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.lineEditBOStudentID.setFont(font)
        self.lineEditBOStudentID.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px; color: #ffffff;")
        self.lineEditBOStudentID.setText("")
        self.lineEditBOStudentID.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditBOStudentID.setObjectName("lineEditBOStudentID")
        self.lineEditBOStudentName = QtWidgets.QLineEdit(self.groupBoxBO)
        self.lineEditBOStudentName.returnPressed.connect(lambda: self.getUserFromName(-1))
        self.lineEditBOStudentName.setGeometry(QtCore.QRect(660, 30, 441, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.lineEditBOStudentName.setFont(font)
        self.lineEditBOStudentName.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px; color: #ffffff;")
        self.lineEditBOStudentName.setText("")
        self.lineEditBOStudentName.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditBOStudentName.setObjectName("lineEditBOStudentName")
        self.lineEditBOStudentEmail = QtWidgets.QLineEdit(self.groupBoxBO)
        self.lineEditBOStudentEmail.returnPressed.connect(lambda: self.getUserFromEmail(-1))
        self.lineEditBOStudentEmail.setGeometry(QtCore.QRect(1310, 30, 441, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.lineEditBOStudentEmail.setFont(font)
        self.lineEditBOStudentEmail.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px; color: #ffffff;")
        self.lineEditBOStudentEmail.setText("")
        self.lineEditBOStudentEmail.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditBOStudentEmail.setObjectName("lineEditBOStudentEmail")
        self.lineEditBOItemID = QtWidgets.QLineEdit(self.groupBoxBO)
        self.lineEditBOItemID.returnPressed.connect(self.keyItemID)
        self.lineEditBOItemID.setGeometry(QtCore.QRect(20, 120, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.lineEditBOItemID.setFont(font)
        self.lineEditBOItemID.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px; color: #ffffff;")
        self.lineEditBOItemID.setText("")
        self.lineEditBOItemID.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditBOItemID.setObjectName("lineEditBOItemID")
        self.labelBOItemID = QtWidgets.QLabel(self.groupBoxBO)
        self.labelBOItemID.setGeometry(QtCore.QRect(20, 90, 200, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelBOItemID.setFont(font)
        self.labelBOItemID.setAutoFillBackground(False)
        self.labelBOItemID.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelBOItemID.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelBOItemID.setObjectName("labelBOItemID")
        self.labelBOUserID = QtWidgets.QLabel(self.groupBoxBO)
        self.labelBOUserID.setGeometry(QtCore.QRect(240, 0, 200, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelBOUserID.setFont(font)
        self.labelBOUserID.setAutoFillBackground(False)
        self.labelBOUserID.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelBOUserID.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelBOUserID.setObjectName("labelBOUserID")
        self.labelBOUserName = QtWidgets.QLabel(self.groupBoxBO)
        self.labelBOUserName.setGeometry(QtCore.QRect(660, 0, 200, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelBOUserName.setFont(font)
        self.labelBOUserName.setAutoFillBackground(False)
        self.labelBOUserName.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelBOUserName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelBOUserName.setObjectName("labelBOUserName")
        self.labelBOUserEmail = QtWidgets.QLabel(self.groupBoxBO)
        self.labelBOUserEmail.setGeometry(QtCore.QRect(1310, 0, 200, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelBOUserEmail.setFont(font)
        self.labelBOUserEmail.setAutoFillBackground(False)
        self.labelBOUserEmail.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelBOUserEmail.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelBOUserEmail.setObjectName("labelBOUserEmail")
        self.lineEditBOMessage = QtWidgets.QLineEdit(self.groupBoxBO)
        self.lineEditBOMessage.setReadOnly(True)
        self.lineEditBOMessage.setGeometry(QtCore.QRect(20, 30, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.lineEditBOMessage.setFont(font)
        self.lineEditBOMessage.setStyleSheet("color: #ffffff;")
        self.lineEditBOMessage.setText("")
        self.lineEditBOMessage.setFrame(False)
        self.lineEditBOMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditBOMessage.setObjectName("lineEditBOMessage")
        self.listWidgetBOName = QtWidgets.QListWidget(self.groupBoxBO)
        self.listWidgetBOName.itemClicked.connect(self.listItemBOClicked)         #itemDoubleClicked.connect
        self.listWidgetBOName.setGeometry(QtCore.QRect(670, 70, 421, 351))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.listWidgetBOName.setFont(font)
        self.listWidgetBOName.setStyleSheet("color: white; border: 1px solid grey;")
        self.listWidgetBOName.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.listWidgetBOName.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.listWidgetBOName.setObjectName("listWidgetBOName")
        self.listWidgetBOName.hide()
        self.listWidgetBOEmail = QtWidgets.QListWidget(self.groupBoxBO)
        self.listWidgetBOEmail.itemClicked.connect(self.listItemEmailBOClicked)         #itemDoubleClicked.connect
        self.listWidgetBOEmail.setGeometry(QtCore.QRect(1310, 70, 421, 351))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.listWidgetBOEmail.setFont(font)
        self.listWidgetBOEmail.setStyleSheet("color: white; border: 1px solid grey;")
        self.listWidgetBOEmail.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.listWidgetBOEmail.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.listWidgetBOEmail.setObjectName("listWidgetBOEmail")
        self.listWidgetBOEmail.hide()
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1806, 24))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)


        # Return
        self.groupBoxRe = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxRe.setGeometry(QtCore.QRect(20, 100, 1761, 871))
        self.groupBoxRe.setStyleSheet("background-color: #181e23; border: 0px solid #000;")
        self.groupBoxRe.setTitle("")
        self.groupBoxRe.setObjectName("groupBoxRe")
        self.tableWidgetRe = QtWidgets.QTableWidget(self.groupBoxRe)
        self.tableWidgetRe.setGeometry(QtCore.QRect(190, 90, 1561, 771))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetRe.sizePolicy().hasHeightForWidth())
        self.tableWidgetRe.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
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
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        self.tableWidgetRe.setHorizontalHeaderItem(0, item)
        self.tableWidgetRe.setColumnWidth(0, 100)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        self.tableWidgetRe.setHorizontalHeaderItem(1, item)
        self.tableWidgetRe.setColumnWidth(1, 650)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        self.tableWidgetRe.setHorizontalHeaderItem(2, item)
        self.tableWidgetRe.setColumnWidth(2, 260)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        self.tableWidgetRe.setHorizontalHeaderItem(3, item)
        self.tableWidgetRe.setColumnWidth(3, 280)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        self.tableWidgetRe.setHorizontalHeaderItem(4, item)
        self.tableWidgetRe.setColumnWidth(4, 260)
        self.tableWidgetRe.verticalHeader().setVisible(True)
        self.tableWidgetRe.verticalHeader().setHighlightSections(True)
        self.lineEditReItemID = QtWidgets.QLineEdit(self.groupBoxRe)
        self.lineEditReItemID.returnPressed.connect(lambda: self.returnItems())
        self.lineEditReItemID.setGeometry(QtCore.QRect(20, 120, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.lineEditReItemID.setFont(font)
        self.lineEditReItemID.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px; color: #ffffff;")
        self.lineEditReItemID.setText("")
        self.lineEditReItemID.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditReItemID.setObjectName("lineEditReItemID")
        self.labelReItemID = QtWidgets.QLabel(self.groupBoxRe)
        self.labelReItemID.setGeometry(QtCore.QRect(20, 90, 200, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelReItemID.setFont(font)
        self.labelReItemID.setAutoFillBackground(False)
        self.labelReItemID.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelReItemID.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelReItemID.setObjectName("labelReItemID")
        self.lineEditReMessage = QtWidgets.QLineEdit(self.groupBoxRe)
        self.lineEditReMessage.setReadOnly(True)
        self.lineEditReMessage.setGeometry(QtCore.QRect(20, 30, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.lineEditReMessage.setFont(font)
        self.lineEditReMessage.setStyleSheet("color: #ffffff;")
        self.lineEditReMessage.setText("")
        self.lineEditReMessage.setFrame(False)
        self.lineEditReMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditReMessage.setObjectName("lineEditReMessage")


        # Booked Out
        self.groupBoxBkdO = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxBkdO.setGeometry(QtCore.QRect(20, 100, 1761, 871))
        self.groupBoxBkdO.setStyleSheet("background-color: #181e23; border: 0px solid #000;")
        self.groupBoxBkdO.setTitle("")
        self.groupBoxBkdO.setObjectName("groupBoxBkdO")
        self.labelBkdOShowLong = QtWidgets.QLabel(self.groupBoxBkdO)
        self.labelBkdOShowLong.setGeometry(QtCore.QRect(20, 90, 200, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        self.labelBkdOShowLong.setFont(font)
        self.labelBkdOShowLong.setAutoFillBackground(False)
        self.labelBkdOShowLong.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelBkdOShowLong.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelBkdOShowLong.setObjectName("labelBkdOShowLong")
        self.checkBoxBkdO = QtWidgets.QCheckBox(self.groupBoxBkdO, clicked = lambda: self.showLongTerm())
        self.checkBoxBkdO.setGeometry(QtCore.QRect(76, 130, 21, 21))
        self.checkBoxBkdO.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(48)
        self.checkBoxBkdO.setFont(font)
        self.checkBoxBkdO.setStyleSheet("QCheckBox::indicator { margin-left:50%; margin-right:50%; }")
        self.checkBoxBkdO.setText("")
        self.checkBoxBkdO.setIconSize(QtCore.QSize(32, 32))
        self.checkBoxBkdO.setChecked(False)
        self.checkBoxBkdO.setObjectName("checkBoxBkdO")
        self.tableWidgetBkdO = QtWidgets.QTableWidget(self.groupBoxBkdO)
        self.tableWidgetBkdO.cellChanged.connect(self.onCellChanged)
        self.tableWidgetBkdO.setGeometry(QtCore.QRect(190, 90, 1561, 771))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetBkdO.sizePolicy().hasHeightForWidth())
        self.tableWidgetBkdO.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.tableWidgetBkdO.setFont(font)
        self.tableWidgetBkdO.setAutoFillBackground(False)
        #self.tableWidgetBkdO.setStyleSheet("alternate-background-color: #282e33;background-color: #181e23; color: white;")
        self.tableWidgetBkdO.setStyleSheet(styleSheet)
        self.tableWidgetBkdO.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidgetBkdO.setLineWidth(1)
        self.tableWidgetBkdO.setMidLineWidth(0)
        self.tableWidgetBkdO.setAlternatingRowColors(True)
        self.tableWidgetBkdO.setShowGrid(True)
        self.tableWidgetBkdO.setRowCount(0)
        self.tableWidgetBkdO.setObjectName("tableWidgetBkdO")
        self.tableWidgetBkdO.setColumnCount(6)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        self.tableWidgetBkdO.setHorizontalHeaderItem(0, item)     # Long-Term
        self.tableWidgetBkdO.setColumnWidth(0, 120)               
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        self.tableWidgetBkdO.setHorizontalHeaderItem(1, item)     # Item ID
        self.tableWidgetBkdO.setColumnWidth(1, 120)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        self.tableWidgetBkdO.setHorizontalHeaderItem(2, item)     # Item Name
        self.tableWidgetBkdO.setColumnWidth(2, 530)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        self.tableWidgetBkdO.setHorizontalHeaderItem(3, item)     # Student Name
        self.tableWidgetBkdO.setColumnWidth(3, 260)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        self.tableWidgetBkdO.setHorizontalHeaderItem(4, item)     # Student Email
        self.tableWidgetBkdO.setColumnWidth(4, 235)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        self.tableWidgetBkdO.setHorizontalHeaderItem(5, item)     # Date Booked Out
        self.tableWidgetBkdO.setColumnWidth(5, 260)
        self.tableWidgetBkdO.verticalHeader().setVisible(True)
        self.tableWidgetBkdO.verticalHeader().setHighlightSections(True)
        self.pushButtonBkdOExport = QtWidgets.QPushButton(self.groupBoxBkdO, clicked = lambda: self.exportBooked())
        self.pushButtonBkdOExport.setGeometry(QtCore.QRect(20, 790, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonBkdOExport.setFont(font)
        self.pushButtonBkdOExport.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonBkdOExport.setObjectName("pushButtonBkdOExport")


        # History
        self.groupBoxHist = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxHist.setGeometry(QtCore.QRect(20, 100, 1761, 871))
        self.groupBoxHist.setStyleSheet("background-color: #181e23; border: 0px solid #000;")
        self.groupBoxHist.setTitle("")
        self.groupBoxHist.setObjectName("groupBoxHist")
        self.tableWidgetHist = QtWidgets.QTableWidget(self.groupBoxHist)
        self.tableWidgetHist.setGeometry(QtCore.QRect(190, 90, 1561, 771))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetHist.sizePolicy().hasHeightForWidth())
        self.listWidgetHistName = QtWidgets.QListWidget(self.groupBoxHist)
        self.listWidgetHistName.itemClicked.connect(self.listItemHistClicked)         #itemDoubleClicked.connect
        self.listWidgetHistName.setGeometry(QtCore.QRect(670, 70, 421, 351))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.listWidgetHistName.setFont(font)
        self.listWidgetHistName.setStyleSheet("color: white; border: 1px solid grey;")
        self.listWidgetHistName.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.listWidgetHistName.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.listWidgetHistName.setObjectName("listWidgetHistName")
        self.listWidgetHistName.hide()
        self.tableWidgetHist.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
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
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        self.tableWidgetHist.setHorizontalHeaderItem(0, item)
        self.tableWidgetHist.setColumnWidth(0, 100)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        self.tableWidgetHist.setHorizontalHeaderItem(1, item)
        self.tableWidgetHist.setColumnWidth(1, 630)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        self.tableWidgetHist.setHorizontalHeaderItem(2, item)
        self.tableWidgetHist.setColumnWidth(2, 260)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        self.tableWidgetHist.setHorizontalHeaderItem(3, item)   # Email
        self.tableWidgetHist.setColumnWidth(3, 255)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        self.tableWidgetHist.setHorizontalHeaderItem(4, item)
        self.tableWidgetHist.setColumnWidth(4, 140)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        self.tableWidgetHist.setHorizontalHeaderItem(5, item)
        self.tableWidgetHist.setColumnWidth(5, 140)
        self.tableWidgetHist.verticalHeader().setVisible(True)
        self.tableWidgetHist.verticalHeader().setHighlightSections(True)
        self.pushButtonHistClear = QtWidgets.QPushButton(self.groupBoxHist, clicked = lambda: self.clearHist())
        self.pushButtonHistClear.setGeometry(QtCore.QRect(20, 230, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonHistClear.setFont(font)
        self.pushButtonHistClear.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonHistClear.setObjectName("pushButtonHistClear")
        self.pushButtonHistExport = QtWidgets.QPushButton(self.groupBoxHist, clicked = lambda: self.exportHistory())
        self.pushButtonHistExport.setGeometry(QtCore.QRect(20, 790, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonHistExport.setFont(font)
        self.pushButtonHistExport.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonHistExport.setObjectName("pushButtonHistExport")
        self.lineEditHistStudentID = QtWidgets.QLineEdit(self.groupBoxHist)
        self.lineEditHistStudentID.returnPressed.connect(lambda: self.getUserFromID(0))
        self.lineEditHistStudentID.setGeometry(QtCore.QRect(240, 30, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.lineEditHistStudentID.setFont(font)
        self.lineEditHistStudentID.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px; color: #ffffff;")
        self.lineEditHistStudentID.setText("")
        self.lineEditHistStudentID.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditHistStudentID.setObjectName("lineEditHistStudentID")
        self.lineEditHistStudentName = QtWidgets.QLineEdit(self.groupBoxHist)
        self.lineEditHistStudentName.returnPressed.connect(lambda: self.getUserFromName(-1))
        self.lineEditHistStudentName.setGeometry(QtCore.QRect(660, 30, 441, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.lineEditHistStudentName.setFont(font)
        self.lineEditHistStudentName.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px; color: #ffffff;")
        self.lineEditHistStudentName.setText("")
        self.lineEditHistStudentName.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditHistStudentName.setObjectName("lineEditHistStudentName")
        self.lineEditHistItemID = QtWidgets.QLineEdit(self.groupBoxHist)
        self.lineEditHistItemID.returnPressed.connect(lambda: self.getItemFromID())
        self.lineEditHistItemID.setGeometry(QtCore.QRect(20, 120, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.lineEditHistItemID.setFont(font)
        self.lineEditHistItemID.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px; color: #ffffff;")
        self.lineEditHistItemID.setText("")
        self.lineEditHistItemID.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditHistItemID.setObjectName("lineEditHistItemID")
        self.labelHistItemID = QtWidgets.QLabel(self.groupBoxHist)
        self.labelHistItemID.setGeometry(QtCore.QRect(20, 90, 200, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelHistItemID.setFont(font)
        self.labelHistItemID.setAutoFillBackground(False)
        self.labelHistItemID.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelHistItemID.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelHistItemID.setObjectName("labelHistItemID")
        self.labelHistStudentID = QtWidgets.QLabel(self.groupBoxHist)
        self.labelHistStudentID.setGeometry(QtCore.QRect(240, 0, 200, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelHistStudentID.setFont(font)
        self.labelHistStudentID.setAutoFillBackground(False)
        self.labelHistStudentID.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelHistStudentID.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelHistStudentID.setObjectName("labelHistStudentID")
        self.labelHistStudentName = QtWidgets.QLabel(self.groupBoxHist)
        self.labelHistStudentName.setGeometry(QtCore.QRect(660, 0, 200, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelHistStudentName.setFont(font)
        self.labelHistStudentName.setAutoFillBackground(False)
        self.labelHistStudentName.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelHistStudentName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelHistStudentName.setObjectName("labelHistStudentName")
        self.lineEditHistStudentEmail = QtWidgets.QLineEdit(self.groupBoxHist)
        self.lineEditHistStudentEmail.returnPressed.connect(lambda: self.getUserFromEmail(-1))
        self.lineEditHistStudentEmail.setGeometry(QtCore.QRect(1290, 30, 461, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.lineEditHistStudentEmail.setFont(font)
        self.lineEditHistStudentEmail.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px; color: #ffffff;")
        self.lineEditHistStudentEmail.setText("")
        self.lineEditHistStudentEmail.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditHistStudentEmail.setObjectName("lineEditHistStudentEmail")
        self.listWidgetHistEmail = QtWidgets.QListWidget(self.groupBoxHist)
        self.listWidgetHistEmail.itemClicked.connect(self.listItemEmailHistClicked)         #itemDoubleClicked.connect
        self.listWidgetHistEmail.setGeometry(QtCore.QRect(1310, 70, 421, 351))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.listWidgetHistEmail.setFont(font)
        self.listWidgetHistEmail.setStyleSheet("color: white; border: 1px solid grey;")
        self.listWidgetHistEmail.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.listWidgetHistEmail.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.listWidgetHistEmail.setObjectName("listWidgetHistEmail")
        self.listWidgetHistEmail.hide()
        self.labelHistStudentEmail = QtWidgets.QLabel(self.groupBoxHist)
        self.labelHistStudentEmail.setGeometry(QtCore.QRect(1290, 0, 200, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelHistStudentEmail.setFont(font)
        self.labelHistStudentEmail.setAutoFillBackground(False)
        self.labelHistStudentEmail.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelHistStudentEmail.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelHistStudentEmail.setObjectName("labelHistStudentEmail")
        self.lineEditHistMessage = QtWidgets.QLineEdit(self.groupBoxHist)
        self.lineEditHistMessage.setReadOnly(True)
        self.lineEditHistMessage.setGeometry(QtCore.QRect(20, 30, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.lineEditHistMessage.setFont(font)
        self.lineEditHistMessage.setStyleSheet("color: #ffffff;")
        self.lineEditHistMessage.setText("")
        self.lineEditHistMessage.setFrame(False)
        self.lineEditHistMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditHistMessage.setObjectName("lineEditHistMessage")
        currentDate = QtCore.QDate.currentDate()
        self.dateEditFrom = QtWidgets.QDateEdit(self.groupBoxHist, calendarPopup=True)
        self.dateEditFrom.setGeometry(QtCore.QRect(10, 390, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(20)
        self.dateEditFrom.setFont(font)
        self.dateEditFrom.setStyleSheet("color: white; background-color: #444;border: 2px solid grey; border-radius: 5px;")
        self.dateEditFrom.setObjectName("dateEditFrom")
        self.dateEditFrom.setDate(currentDate.addDays(-28))
        self.dateEditFrom.dateChanged.connect(lambda: self.refreshHistory())
        self.dateEditTo = QtWidgets.QDateEdit(self.groupBoxHist, calendarPopup=True)
        self.dateEditTo.setGeometry(QtCore.QRect(10, 580, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(20)
        self.dateEditTo.setFont(font)
        self.dateEditTo.setStyleSheet("color: white; background-color: #444;border: 2px solid grey; border-radius: 5px;")
        self.dateEditTo.setObjectName("dateEditTo")
        self.dateEditTo.setDate(currentDate)
        self.dateEditTo.dateChanged.connect(lambda: self.refreshHistory())
        self.labelHistDateFrom = QtWidgets.QLabel(self.groupBoxHist)
        self.labelHistDateFrom.setGeometry(QtCore.QRect(20, 360, 200, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelHistDateFrom.setFont(font)
        self.labelHistDateFrom.setAutoFillBackground(False)
        self.labelHistDateFrom.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelHistDateFrom.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelHistDateFrom.setObjectName("labelHistDateFrom")
        self.labelHistDateTo = QtWidgets.QLabel(self.groupBoxHist)
        self.labelHistDateTo.setGeometry(QtCore.QRect(20, 550, 200, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelHistDateTo.setFont(font)
        self.labelHistDateTo.setAutoFillBackground(False)
        self.labelHistDateTo.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelHistDateTo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelHistDateTo.setObjectName("labelHistDateTo")
        self.pushButtonHistResetDate = QtWidgets.QPushButton(self.groupBoxHist, clicked = lambda: self.resetDateHist())
        self.pushButtonHistResetDate.setGeometry(QtCore.QRect(40, 480, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonHistResetDate.setFont(font)
        self.pushButtonHistResetDate.setStyleSheet("border: 4px solid grey; border-radius: 10px;background-color: #804040; color: #ffffff;")
        self.pushButtonHistResetDate.setObjectName("pushButtonHistResetDate")


        # Items
        self.groupBoxItemsOuter = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxItemsOuter.setGeometry(QtCore.QRect(20, 100, 1761, 871))
        self.groupBoxItemsOuter.setStyleSheet("background-color: #181e23; border: 0px solid #000;")
        self.groupBoxItemsOuter.setTitle("")
        self.groupBoxItemsOuter.setObjectName("groupBoxItemsOuter")

        # All Items
        self.groupBoxAllItems = QtWidgets.QGroupBox(self.groupBoxItemsOuter)
        self.groupBoxAllItems.setGeometry(QtCore.QRect(10, 10, 1741, 831))
        self.groupBoxAllItems.setStyleSheet("background-color: #1c2428")
        self.groupBoxAllItems.setTitle("")
        self.groupBoxAllItems.setObjectName("groupBoxAllItems")

        self.pushButtonAllItemsMenu1 = QtWidgets.QPushButton(self.groupBoxAllItems, clicked = lambda: self.openWindowItems())
        self.pushButtonAllItemsMenu1.setGeometry(QtCore.QRect(1300, 10, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonAllItemsMenu1.setFont(font)
        self.pushButtonAllItemsMenu1.setStyleSheet("border: 4px solid #aa3333; background-color: #408040; border-radius: 10px;color: #ffffff;")
        self.pushButtonAllItemsMenu1.setObjectName("pushButtonAllItemsMenu1")
        self.pushButtonAddItemMenu1 = QtWidgets.QPushButton(self.groupBoxAllItems, clicked = lambda: self.openWindowAddItem())
        self.pushButtonAddItemMenu1.setGeometry(QtCore.QRect(1530, 10, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonAddItemMenu1.setFont(font)
        self.pushButtonAddItemMenu1.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px;color: #ffffff;")
        self.pushButtonAddItemMenu1.setObjectName("pushButtonAddItemMenu1")

        self.lineEditAIItemID = QtWidgets.QLineEdit(self.groupBoxAllItems)
        self.lineEditAIItemID.returnPressed.connect(lambda: self.populateAllItems())
        self.lineEditAIItemID.setGeometry(QtCore.QRect(230, 30, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.lineEditAIItemID.setFont(font)
        self.lineEditAIItemID.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px;color: #ffffff;")
        self.lineEditAIItemID.setText("")
        self.lineEditAIItemID.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAIItemID.setObjectName("lineEditAIItemID")
        self.lineEditAIItemSearch = QtWidgets.QLineEdit(self.groupBoxAllItems)
        self.lineEditAIItemSearch.returnPressed.connect(lambda: self.populateAllItems())
        self.lineEditAIItemSearch.setGeometry(QtCore.QRect(650, 30, 441, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.lineEditAIItemSearch.setFont(font)
        self.lineEditAIItemSearch.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px;color: #ffffff;")
        self.lineEditAIItemSearch.setText("")
        self.lineEditAIItemSearch.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAIItemSearch.setObjectName("lineEditAIItemSearch")

        self.tableWidgetAI = QtWidgets.QTableWidget(self.groupBoxAllItems)
        self.tableWidgetAI.setGeometry(QtCore.QRect(190, 90, 1561, 771))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetAI.sizePolicy().hasHeightForWidth())
        self.tableWidgetAI.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.tableWidgetAI.setFont(font)
        self.tableWidgetAI.setAutoFillBackground(False)
        self.tableWidgetAI.setStyleSheet(styleSheet)
        self.tableWidgetAI.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidgetAI.setLineWidth(1)
        self.tableWidgetAI.setMidLineWidth(0)
        self.tableWidgetAI.setAlternatingRowColors(True)
        self.tableWidgetAI.setShowGrid(True)
        self.tableWidgetAI.setRowCount(0)
        self.tableWidgetAI.setObjectName("tableWidgetAI")
        self.tableWidgetAI.setColumnCount(5)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        self.tableWidgetAI.setHorizontalHeaderItem(0, item)
        self.tableWidgetAI.setColumnWidth(0, 100)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidgetAI.setHorizontalHeaderItem(1, item)
        self.tableWidgetAI.setColumnWidth(1, 590)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        self.tableWidgetAI.setHorizontalHeaderItem(2, item)
        self.tableWidgetAI.setColumnWidth(2, 220)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        self.tableWidgetAI.setHorizontalHeaderItem(3, item)
        self.tableWidgetAI.setColumnWidth(3, 320)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        item.setFont(font)
        self.tableWidgetAI.setHorizontalHeaderItem(4, item)
        self.tableWidgetAI.setColumnWidth(4, 260)
        self.tableWidgetAI.verticalHeader().setVisible(True)
        self.tableWidgetAI.verticalHeader().setHighlightSections(True)
        
        self.pushButtonAIClear = QtWidgets.QPushButton(self.groupBoxAllItems)
        self.pushButtonAIClear = QtWidgets.QPushButton(self.groupBoxAllItems, clicked = lambda: self.clearAllItems())
        self.pushButtonAIClear.setGeometry(QtCore.QRect(10, 150, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonAIClear.setFont(font)
        self.pushButtonAIClear.setStyleSheet("border: 4px solid grey; border-radius: 10px;background-color: #804040; color: #ffffff;")
        self.pushButtonAIClear.setObjectName("pushButtonAIClear")
        self.pushButtonAIExport = QtWidgets.QPushButton(self.groupBoxAllItems)
        self.pushButtonAIExport = QtWidgets.QPushButton(self.groupBoxAllItems, clicked = lambda: self.exportItems())
        self.pushButtonAIExport.setGeometry(QtCore.QRect(20, 770, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonAIExport.setFont(font)
        self.pushButtonAIExport.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px;color: #ffffff;")
        self.pushButtonAIExport.setObjectName("pushButtonAIExport")
        self.lineEditAIMessage = QtWidgets.QLineEdit(self.groupBoxAllItems)
        self.lineEditAIMessage.setGeometry(QtCore.QRect(10, 40, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.lineEditAIMessage.setFont(font)
        self.lineEditAIMessage.setStyleSheet("color: #ffffff;")
        self.lineEditAIMessage.setText("")
        self.lineEditAIMessage.setFrame(False)
        self.lineEditAIMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAIMessage.setObjectName("lineEditAIMessage")
        self.labelAIItemiD = QtWidgets.QLabel(self.groupBoxAllItems)
        self.labelAIItemiD.setGeometry(QtCore.QRect(240, 0, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelAIItemiD.setFont(font)
        self.labelAIItemiD.setAutoFillBackground(False)
        self.labelAIItemiD.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAIItemiD.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAIItemiD.setObjectName("labelAIItemiD")
        self.labelAIItemSearch = QtWidgets.QLabel(self.groupBoxAllItems)
        self.labelAIItemSearch.setGeometry(QtCore.QRect(660, 0, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelAIItemSearch.setFont(font)
        self.labelAIItemSearch.setAutoFillBackground(False)
        self.labelAIItemSearch.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAIItemSearch.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAIItemSearch.setObjectName("labelAIItemSearch")
        
        # Add Item
        self.groupBoxAddItem = QtWidgets.QGroupBox(self.groupBoxItemsOuter)
        self.groupBoxAddItem.setGeometry(QtCore.QRect(10, 10, 1741, 831))
        self.groupBoxAddItem.setStyleSheet("background-color: #1c2428")
        self.groupBoxAddItem.setTitle("")
        self.groupBoxAddItem.setObjectName("groupBoxAddItem")

        self.pushButtonAllItemsMenu2 = QtWidgets.QPushButton(self.groupBoxAddItem, clicked = lambda: self.openWindowItems())
        self.pushButtonAllItemsMenu2.setGeometry(QtCore.QRect(1300, 10, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonAllItemsMenu2.setFont(font)
        self.pushButtonAllItemsMenu2.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px;color: #ffffff;")
        self.pushButtonAllItemsMenu2.setObjectName("pushButtonAllItemsMenu2")

        self.pushButtonAddItemMenu2 = QtWidgets.QPushButton(self.groupBoxAddItem, clicked = lambda: self.openWindowAddItem())
        self.pushButtonAddItemMenu2.setGeometry(QtCore.QRect(1530, 10, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonAddItemMenu2.setFont(font)
        self.pushButtonAddItemMenu2.setStyleSheet("border: 4px solid #aa3333; background-color: #408040; border-radius: 10px;color: #ffffff;")
        self.pushButtonAddItemMenu2.setObjectName("pushButtonAddItemMenu2")

        self.lineEditAddItemID = QtWidgets.QLineEdit(self.groupBoxAddItem)
        self.lineEditAddItemID.returnPressed.connect(lambda: self.addItemIDCheck())
        self.lineEditAddItemID.setGeometry(QtCore.QRect(630, 160, 481, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.lineEditAddItemID.setFont(font)
        self.lineEditAddItemID.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px;color: #ffffff;")
        self.lineEditAddItemID.setText("")
        self.lineEditAddItemID.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddItemID.setObjectName("lineEditAddItemID")
        self.lineEditAddItemSerial = QtWidgets.QLineEdit(self.groupBoxAddItem)
        self.lineEditAddItemSerial.returnPressed.connect(lambda: self.addItemSerial())
        self.lineEditAddItemSerial.setGeometry(QtCore.QRect(630, 270, 481, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.lineEditAddItemSerial.setFont(font)
        self.lineEditAddItemSerial.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px;color: #ffffff;")
        self.lineEditAddItemSerial.setText("")
        self.lineEditAddItemSerial.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddItemSerial.setObjectName("lineEditAddItemSerial")
        self.lineEditAddItemName = QtWidgets.QLineEdit(self.groupBoxAddItem)
        self.lineEditAddItemName.returnPressed.connect(lambda: self.addItemName())
        self.lineEditAddItemName.setGeometry(QtCore.QRect(630, 380, 481, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.lineEditAddItemName.setFont(font)
        self.lineEditAddItemName.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px;color: #ffffff;")
        self.lineEditAddItemName.setText("")
        self.lineEditAddItemName.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddItemName.setObjectName("lineEditAddItemName")
        self.lineEditAddItemMake = QtWidgets.QLineEdit(self.groupBoxAddItem)
        self.lineEditAddItemMake.returnPressed.connect(lambda: self.addItemMake())
        self.lineEditAddItemMake.setGeometry(QtCore.QRect(630, 490, 481, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.lineEditAddItemMake.setFont(font)
        self.lineEditAddItemMake.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px;color: #ffffff;")
        self.lineEditAddItemMake.setText("")
        self.lineEditAddItemMake.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddItemMake.setObjectName("lineEditAddItemMake")
        self.lineEditAddItemModel = QtWidgets.QLineEdit(self.groupBoxAddItem)
        self.lineEditAddItemModel.returnPressed.connect(lambda: self.addItemModel())
        self.lineEditAddItemModel.setGeometry(QtCore.QRect(630, 600, 481, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.lineEditAddItemModel.setFont(font)
        self.lineEditAddItemModel.setStyleSheet("border: 4px solid grey; background-color: #111; border-radius: 10px;color: #ffffff;")
        self.lineEditAddItemModel.setText("")
        self.lineEditAddItemModel.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddItemModel.setObjectName("lineEditAddItemModel")
        self.labelAIItemBarcode = QtWidgets.QLabel(self.groupBoxAddItem)
        self.labelAIItemBarcode.setGeometry(QtCore.QRect(640, 130, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelAIItemBarcode.setFont(font)
        self.labelAIItemBarcode.setAutoFillBackground(False)
        self.labelAIItemBarcode.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAIItemBarcode.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAIItemBarcode.setObjectName("labelAIItemBarcode")
        self.labelAIItemSerial = QtWidgets.QLabel(self.groupBoxAddItem)
        self.labelAIItemSerial.setGeometry(QtCore.QRect(640, 240, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelAIItemSerial.setFont(font)
        self.labelAIItemSerial.setAutoFillBackground(False)
        self.labelAIItemSerial.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAIItemSerial.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAIItemSerial.setObjectName("labelAIItemSerial")
        self.labelAIItemName = QtWidgets.QLabel(self.groupBoxAddItem)
        self.labelAIItemName.setGeometry(QtCore.QRect(640, 350, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelAIItemName.setFont(font)
        self.labelAIItemName.setAutoFillBackground(False)
        self.labelAIItemName.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAIItemName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAIItemName.setObjectName("labelAIItemName")
        self.labelAIItemMake = QtWidgets.QLabel(self.groupBoxAddItem)
        self.labelAIItemMake.setGeometry(QtCore.QRect(640, 460, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelAIItemMake.setFont(font)
        self.labelAIItemMake.setAutoFillBackground(False)
        self.labelAIItemMake.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAIItemMake.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAIItemMake.setObjectName("labelAIItemMake")
        self.labelAIItemModel = QtWidgets.QLabel(self.groupBoxAddItem)
        self.labelAIItemModel.setGeometry(QtCore.QRect(640, 570, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelAIItemModel.setFont(font)
        self.labelAIItemModel.setAutoFillBackground(False)
        self.labelAIItemModel.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAIItemModel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAIItemModel.setObjectName("labelAIItemModel")
        self.pushButtonAddItemSave = QtWidgets.QPushButton(self.groupBoxAddItem, clicked = lambda: self.addItemSave())
        self.pushButtonAddItemSave.setGeometry(QtCore.QRect(630, 700, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonAddItemSave.setFont(font)
        self.pushButtonAddItemSave.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px;color: #ffffff;")
        self.pushButtonAddItemSave.setObjectName("pushButtonAddItemSave")
        self.pushButtonAddItemClear = QtWidgets.QPushButton(self.groupBoxAddItem, clicked = lambda: self.addItemClear())
        self.pushButtonAddItemClear.setGeometry(QtCore.QRect(970, 700, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonAddItemClear.setFont(font)
        self.pushButtonAddItemClear.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px;color: #ffffff;")
        self.pushButtonAddItemClear.setObjectName("pushButtonAddItemClear")
        self.lineEditAddItemMessage = QtWidgets.QLineEdit(self.groupBoxAddItem)
        self.lineEditAddItemMessage.setGeometry(QtCore.QRect(10, 40, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.lineEditAddItemMessage.setFont(font)
        self.lineEditAddItemMessage.setStyleSheet("color: #ffffff;")
        self.lineEditAddItemMessage.setText("")
        self.lineEditAddItemMessage.setFrame(False)
        self.lineEditAddItemMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddItemMessage.setObjectName("lineEditAddItemMessage")


        self.groupBoxUsersOuter = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxUsersOuter.setGeometry(QtCore.QRect(20, 100, 1761, 871))
        self.groupBoxUsersOuter.setStyleSheet("background-color: #181e23; border: 0px solid #000;")
        self.groupBoxUsersOuter.setTitle("")
        self.groupBoxUsersOuter.setObjectName("groupBoxUsersOuter")

        self.groupBoxUsers = QtWidgets.QGroupBox(self.groupBoxUsersOuter)
        self.groupBoxUsers.setGeometry(QtCore.QRect(10, 10, 1741, 831))
        self.groupBoxUsers.setStyleSheet("background-color: #1c2428; border: 0px solid #000;")
        self.groupBoxUsers.setTitle("")
        self.groupBoxUsers.setObjectName("groupBoxUsers")

        self.pushButtonAddUser = QtWidgets.QPushButton(self.groupBoxUsers, clicked = lambda: self.openWindowUser())
        self.pushButtonAddUser.setGeometry(QtCore.QRect(1530, 10, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonAddUser.setFont(font)
        self.pushButtonAddUser.setStyleSheet("border: 4px solid #aa3333; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonAddUser.setObjectName("pushButtonAddUser")

        self.lineEditAddUserID = QtWidgets.QLineEdit(self.groupBoxUsers)
        self.lineEditAddUserID.returnPressed.connect(lambda: self.addUserIDCheck())
        self.lineEditAddUserID.setGeometry(QtCore.QRect(610, 170, 361, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.lineEditAddUserID.setFont(font)
        self.lineEditAddUserID.setStyleSheet("border: 4px solid grey;background-color: #111;border-radius: 10px; color: #ffffff;")
        self.lineEditAddUserID.setText("")
        self.lineEditAddUserID.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddUserID.setObjectName("lineEditAddUserID")
        self.lineEditAddUserFirst = QtWidgets.QLineEdit(self.groupBoxUsers)
        self.lineEditAddUserFirst.returnPressed.connect(lambda: self.addUserFirstCheck())
        self.lineEditAddUserFirst.setGeometry(QtCore.QRect(610, 300, 261, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.lineEditAddUserFirst.setFont(font)
        self.lineEditAddUserFirst.setStyleSheet("border: 4px solid grey;background-color: #111;border-radius: 10px; color: #ffffff;")
        self.lineEditAddUserFirst.setText("")
        self.lineEditAddUserFirst.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddUserFirst.setObjectName("lineEditAddUserFirst")
        self.lineEditAddUserLast = QtWidgets.QLineEdit(self.groupBoxUsers)
        self.lineEditAddUserLast.returnPressed.connect(lambda: self.addUserLastCheck())
        self.lineEditAddUserLast.setGeometry(QtCore.QRect(890, 300, 261, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.lineEditAddUserLast.setFont(font)
        self.lineEditAddUserLast.setStyleSheet("border: 4px solid grey;background-color: #111;border-radius: 10px; color: #ffffff;")
        self.lineEditAddUserLast.setText("")
        self.lineEditAddUserLast.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddUserLast.setObjectName("lineEditAddUserLast")
        self.lineEditAddUserEmail = QtWidgets.QLineEdit(self.groupBoxUsers)
        self.lineEditAddUserEmail.returnPressed.connect(lambda: self.addUserEmailCheck())
        self.lineEditAddUserEmail.setGeometry(QtCore.QRect(610, 430, 261, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.lineEditAddUserEmail.setFont(font)
        self.lineEditAddUserEmail.setStyleSheet("border: 4px solid grey;background-color: #111;border-radius: 10px; color: #ffffff;")
        self.lineEditAddUserEmail.setText("")
        self.lineEditAddUserEmail.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddUserEmail.setObjectName("lineEditAddUserEmail")
        self.labelAddUserBarcode = QtWidgets.QLabel(self.groupBoxUsers)
        self.labelAddUserBarcode.setGeometry(QtCore.QRect(620, 140, 200, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelAddUserBarcode.setFont(font)
        self.labelAddUserBarcode.setAutoFillBackground(False)
        self.labelAddUserBarcode.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAddUserBarcode.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAddUserBarcode.setObjectName("labelAddUserBarcode")
        self.labelAddUserFirstName = QtWidgets.QLabel(self.groupBoxUsers)
        self.labelAddUserFirstName.setGeometry(QtCore.QRect(620, 270, 200, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelAddUserFirstName.setFont(font)
        self.labelAddUserFirstName.setAutoFillBackground(False)
        self.labelAddUserFirstName.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAddUserFirstName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAddUserFirstName.setObjectName("labelAddUserFirstName")
        self.labelAddUserLastName = QtWidgets.QLabel(self.groupBoxUsers)
        self.labelAddUserLastName.setGeometry(QtCore.QRect(900, 270, 200, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelAddUserLastName.setFont(font)
        self.labelAddUserLastName.setAutoFillBackground(False)
        self.labelAddUserLastName.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAddUserLastName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAddUserLastName.setObjectName("labelAddUserLastName")
        self.labelAddUserEmail = QtWidgets.QLabel(self.groupBoxUsers)
        self.labelAddUserEmail.setGeometry(QtCore.QRect(620, 400, 200, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.labelAddUserEmail.setFont(font)
        self.labelAddUserEmail.setAutoFillBackground(False)
        self.labelAddUserEmail.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 0);")
        self.labelAddUserEmail.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAddUserEmail.setObjectName("labelAddUserEmail")
        self.pushButtonAddUserSave = QtWidgets.QPushButton(self.groupBoxUsers, clicked = lambda: self.addUserSave())
        self.pushButtonAddUserSave.setGeometry(QtCore.QRect(610, 530, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonAddUserSave.setFont(font)
        self.pushButtonAddUserSave.setStyleSheet("border: 4px solid grey; background-color: #408040;border-radius: 10px; color: #ffffff;")
        self.pushButtonAddUserSave.setObjectName("pushButtonAddUserSave")
        self.pushButtonAddUserClear = QtWidgets.QPushButton(self.groupBoxUsers, clicked = lambda: self.addUserClear())
        self.pushButtonAddUserClear.setGeometry(QtCore.QRect(910, 530, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(24)
        self.pushButtonAddUserClear.setFont(font)
        self.pushButtonAddUserClear.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonAddUserClear.setObjectName("pushButtonAddUserSave")
        self.lineEditAddUserMessage = QtWidgets.QLineEdit(self.groupBoxUsers)
        self.lineEditAddUserMessage.setReadOnly(True)
        self.lineEditAddUserMessage.setGeometry(QtCore.QRect(20, 30, 421, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        self.lineEditAddUserMessage.setFont(font)
        self.lineEditAddUserMessage.setStyleSheet("color: #ffffff;")
        self.lineEditAddUserMessage.setText("")
        self.lineEditAddUserMessage.setFrame(False)
        self.lineEditAddUserMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAddUserMessage.setObjectName("lineEditAddUserMessage")


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
        self.labelHistStudentID.setText(_translate("MainWindow", "Student ID"))
        self.labelHistStudentName.setText(_translate("MainWindow", "Student Name"))
        self.labelHistStudentEmail.setText(_translate("MainWindow", "Student Email"))
        self.labelHistDateFrom.setText(_translate("MainWindow", "From"))
        self.labelHistDateTo.setText(_translate("MainWindow", "To"))


        item = self.tableWidgetAI.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Item ID"))
        item = self.tableWidgetAI.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.tableWidgetAI.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Item Name"))
        item = self.tableWidgetAI.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Item Model"))
        item = self.tableWidgetAI.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Item Serial #"))
        self.pushButtonAllItemsMenu1.setText(_translate("MainWindow", "All Items"))
        self.pushButtonAddItemMenu1.setText(_translate("MainWindow", "Add/Edit Item"))
        self.pushButtonAIClear.setText(_translate("MainWindow", "Clear"))
        self.pushButtonAIExport.setText(_translate("MainWindow", "Export"))
        self.labelAIItemiD.setText(_translate("MainWindow", "Item ID"))
        self.labelAIItemSearch.setText(_translate("MainWindow", "Item Search"))


        self.pushButtonAllItemsMenu2.setText(_translate("MainWindow", "All Items"))
        self.pushButtonAddItemMenu2.setText(_translate("MainWindow", "Add/Edit Item"))
        self.labelAIItemBarcode.setText(_translate("MainWindow", "Item BarCode"))
        self.labelAIItemSerial.setText(_translate("MainWindow", "Item Serial No."))
        self.labelAIItemName.setText(_translate("MainWindow", "Item Name"))
        self.labelAIItemMake.setText(_translate("MainWindow", "Item Make"))
        self.labelAIItemModel.setText(_translate("MainWindow", "Item Model"))
        self.pushButtonAddItemSave.setText(_translate("MainWindow", "Save"))
        self.pushButtonAddItemClear.setText(_translate("MainWindow", "Clear"))


        self.pushButtonAddUser.setText(_translate("MainWindow", "Add/Edit User"))
        self.pushButtonAddUserSave.setText(_translate("MainWindow", "Save"))
        self.pushButtonAddUserClear.setText(_translate("MainWindow", "Clear"))
        self.labelAddUserBarcode.setText(_translate("MainWindow", "User BarCode"))
        self.labelAddUserFirstName.setText(_translate("MainWindow", "User First Name"))
        self.labelAddUserLastName.setText(_translate("MainWindow", "User Last Name"))
        self.labelAddUserEmail.setText(_translate("MainWindow", "User Email"))


        self.show()
        self.groupBoxRe.hide()
        self.groupBoxBkdO.hide()
        self.groupBoxHist.hide()
        self.groupBoxItemsOuter.hide()
        self.groupBoxAllItems.hide()
        self.groupBoxAddItem.hide()
        self.groupBoxUsersOuter.hide()

        self.lineEditBOStudentID.setFocus()

    def onCellChanged(self, row, column):
        global watchCellChange

        if watchCellChange:
            checkBox = self.tableWidgetBkdO.item(row, column)
            currentState = checkBox.checkState()
            if currentState > 0:
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
        self.pushButtonUsers.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.groupBoxBO.show()
        self.groupBoxRe.hide()
        self.groupBoxBkdO.hide()
        self.groupBoxHist.hide()
        self.groupBoxItemsOuter.hide()
        self.groupBoxAllItems.hide()
        self.groupBoxAddItem.hide()
        self.groupBoxUsersOuter.hide()

        self.lineEditBOStudentID.setText("")
        self.lineEditBOStudentName.setText("")
        self.lineEditBOStudentEmail.setText("")

        self.lineEditBOStudentID.setFocus()

    def openWindowReturn(self):
        self.pushButtonBookOut.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonReturn.setStyleSheet("border: 4px solid #aa3333; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonBookedOut.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonHistory.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonUsers.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.groupBoxBO.hide()
        self.groupBoxRe.show()
        self.groupBoxBkdO.hide()
        self.groupBoxHist.hide()
        self.groupBoxItemsOuter.hide()
        self.groupBoxAllItems.hide()
        self.groupBoxAddItem.hide()
        self.groupBoxUsersOuter.hide()
        
        self.tableWidgetRe.setRowCount(0)
        
        self.lineEditReItemID.setFocus()

    def openWindowBookedOut(self):
        self.pushButtonBookOut.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonReturn.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonBookedOut.setStyleSheet("border: 4px solid #aa3333; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonHistory.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonUsers.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.groupBoxBO.hide()
        self.groupBoxRe.hide()
        self.groupBoxBkdO.show()
        self.groupBoxHist.hide()
        self.groupBoxItemsOuter.hide()
        self.groupBoxAllItems.hide()
        self.groupBoxAddItem.hide()
        self.groupBoxUsersOuter.hide()

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
        self.pushButtonUsers.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.groupBoxBO.hide()
        self.groupBoxRe.hide()
        self.groupBoxBkdO.hide()
        self.groupBoxHist.show()
        self.groupBoxItemsOuter.hide()
        self.groupBoxAllItems.hide()
        self.groupBoxAddItem.hide()
        self.groupBoxUsersOuter.hide()

        self.refreshHistory()

    def openWindowItems(self):
        self.pushButtonBookOut.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonReturn.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonBookedOut.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonHistory.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.setStyleSheet("border: 4px solid #aa3333; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonUsers.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.groupBoxBO.hide()
        self.groupBoxRe.hide()
        self.groupBoxBkdO.hide()
        self.groupBoxHist.hide()
        self.groupBoxItemsOuter.show()
        self.groupBoxAllItems.show()
        self.groupBoxAddItem.hide()
        self.groupBoxUsersOuter.hide()

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
        self.pushButtonUsers.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.groupBoxBO.hide()
        self.groupBoxRe.hide()
        self.groupBoxBkdO.hide()
        self.groupBoxHist.hide()
        self.groupBoxItemsOuter.show()
        self.groupBoxAllItems.hide()
        self.groupBoxAddItem.show()
        self.groupBoxUsersOuter.hide()

        self.lineEditAddItemID.setFocus()

    def openWindowUser(self):
        self.pushButtonBookOut.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonReturn.setStyleSheet("border: 4px solid grey; background-color: #405C80; border-radius: 10px; color: #ffffff;")
        self.pushButtonBookedOut.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonHistory.setStyleSheet("border: 4px solid grey; background-color: #804040; border-radius: 10px; color: #ffffff;")
        self.pushButtonItems.setStyleSheet("border: 4px solid grey; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.pushButtonUsers.setStyleSheet("border: 4px solid #aa3333; background-color: #408040; border-radius: 10px; color: #ffffff;")
        self.groupBoxBO.hide()
        self.groupBoxRe.hide()
        self.groupBoxBkdO.hide()
        self.groupBoxHist.hide()
        self.groupBoxItemsOuter.hide()
        self.groupBoxAllItems.hide()
        self.groupBoxAddItem.hide()
        self.groupBoxUsersOuter.show()

        self.lineEditAddUserID.setFocus()


    def getUserFromID(self, userID):
        userEmail = ""
        userName = ""

        if userID == 0:

            if self.groupBoxHist.isHidden():
                userID = self.lineEditBOStudentID.text()
            elif self.groupBoxBO.isHidden():
                userID = self.lineEditHistStudentID.text()

        if len(userID) > 5:
            userID = userID.rstrip(userID[-1])
            foundID = userDB.search(DBquery.userID.search(userID))
            userID = (foundID[0]['userID'])
            
        getUser = (userDB.search(DBquery.userID == userID))                                 # search for user number in item database

        if not getUser:                                                                     # If user not found...                     # Remove text in main page message box after 2 seconds
            self.doMessage("No user found")
            self.lineEditBOStudentID.setText("")

        else:
            userName = (getUser[0]['firstName']) + " " + (getUser[0]['lastName'])
            userEmail = (getUser[0]['email'])
            if self.groupBoxHist.isHidden():
                self.lineEditBOStudentName.setText(userName)
                self.lineEditBOStudentEmail.setText(userEmail)
                self.lineEditBOItemID.setFocus()
            elif self.groupBoxBO.isHidden():
                self.lineEditHistStudentName.setText(userName)
                self.lineEditHistStudentEmail.setText(userEmail)

                self.refreshHistory()

        return userID, userName, userEmail
    
    def getUserFromName(self, nameIndex):
        global userNameList

        userNameList = []
        userID = ""
        userName = ""
        userEmail = ""
        foundNames = ""

        if self.groupBoxHist.isHidden():
            names = self.lineEditBOStudentName.text()

        elif self.groupBoxBO.isHidden():
            names = self.lineEditHistStudentName.text()
            
        names = names.capitalize()

        foundFirstNames = userDB.search(DBquery.firstName.search(names + '+'))
        foundLastNames = userDB.search(DBquery.lastName.search(names + '+'))

        foundNames = foundFirstNames + foundLastNames
        
        if len(foundNames) == 1:
            userID = (foundNames[0]['userID'])
            userName = (foundNames[0]['firstName']) + " " + (foundNames[0]['lastName'])
            userEmail = (foundNames[0]['email'])

            if self.groupBoxHist.isHidden():
                self.lineEditBOStudentID.setText(userID)
                self.lineEditBOStudentName.setText(userName)
                self.lineEditBOStudentEmail.setText(userEmail)

            elif self.groupBoxBO.isHidden():
                self.lineEditHistStudentID.setText(userID)
                self.lineEditHistStudentName.setText(userName)
                self.lineEditHistStudentEmail.setText(userEmail)

        elif len(foundNames) > 1:
            if nameIndex == -1:
                i=0
                while i < len(foundNames):
                    userID = (foundNames[i]['userID'])
                    getUser = (userDB.search(DBquery.userID == userID)) 
                    userName = (getUser[0]['firstName']) + " " + (getUser[0]['lastName'])
                    userNameList.append(userName)
                    i += 1
                
                if self.groupBoxHist.isHidden():
                    self.listWidgetBOName.clear()
                    self.listWidgetBOName.addItems(userNameList)
                    self.listWidgetBOName.show()

                elif self.groupBoxBO.isHidden():
                    self.listWidgetHistName.clear()
                    self.listWidgetHistName.addItems(userNameList)
                    self.listWidgetHistName.show()

            else:
                userID = (foundNames[nameIndex]['userID'])
                getUser = (userDB.search(DBquery.userID == userID)) 
                userName = (getUser[0]['firstName']) + " " + (getUser[0]['lastName'])
                userEmail = (getUser[0]['email'])

                if self.groupBoxHist.isHidden():
                    self.lineEditBOStudentID.setText(userID)
                    self.lineEditBOStudentName.setText(userName)
                    self.lineEditBOStudentEmail.setText(userEmail)
                    self.lineEditBOItemID.setFocus()

                elif self.groupBoxBO.isHidden():
                    self.lineEditHistStudentID.setText(userID)
                    self.lineEditHistStudentName.setText(userName)
                    self.lineEditHistStudentEmail.setText(userEmail)
                    self.lineEditHistItemID.setFocus()

        else:
            self.doMessage("No user found")

            if self.groupBoxHist.isHidden():
                self.lineEditBOStudentName.setText("")

        return userID, userName, userEmail
    
    def getUserFromEmail(self, nameIndex):
        global userEmailList

        userEmailList = []
        userID = ""
        userName = ""
        userEmail = ""
        foundNames = ""

        if self.groupBoxHist.isHidden():
            emails = self.lineEditBOStudentEmail.text()

        elif self.groupBoxBO.isHidden():
            emails = self.lineEditHistStudentEmail.text()

        foundEmails = userDB.search(DBquery.email.search(emails + '+'))
        
        if len(foundEmails) == 1:
            userID = (foundEmails[0]['userID'])
            userName = (foundEmails[0]['firstName']) + " " + (foundEmails[0]['lastName'])
            userEmail = (foundEmails[0]['email'])

            if self.groupBoxHist.isHidden():
                self.lineEditBOStudentID.setText(userID)
                self.lineEditBOStudentName.setText(userName)
                self.lineEditBOStudentEmail.setText(userEmail)

            elif self.groupBoxBO.isHidden():
                self.lineEditHistStudentID.setText(userID)
                self.lineEditHistStudentName.setText(userName)
                self.lineEditHistStudentEmail.setText(userEmail)

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
                
                if self.groupBoxHist.isHidden():
                    self.listWidgetBOEmail.clear()
                    self.listWidgetBOEmail.addItems(userEmailList)
                    self.listWidgetBOEmail.show()

                elif self.groupBoxBO.isHidden():
                    self.listWidgetHistEmail.clear()
                    self.listWidgetHistEmail.addItems(userEmailList)
                    self.listWidgetHistEmail.show()
            
            else:
                userID = (foundEmails[nameIndex]['userID'])
                getUser = (userDB.search(DBquery.userID == userID))
                userName = (getUser[0]['firstName']) + " " + (getUser[0]['lastName'])
                userEmail = (getUser[0]['email'])

                if self.groupBoxHist.isHidden():
                    self.lineEditBOStudentID.setText(userID)
                    self.lineEditBOStudentName.setText(userName)
                    self.lineEditBOStudentEmail.setText(userEmail)
                    self.lineEditBOItemID.setFocus()

                elif self.groupBoxBO.isHidden():
                    self.lineEditHistStudentID.setText(userID)
                    self.lineEditHistStudentName.setText(userName)
                    self.lineEditHistStudentEmail.setText(userEmail)
                    self.lineEditHistItemID.setFocus()
            
        else:
            self.doMessage("No user found")

            if self.groupBoxHist.isHidden():
                self.lineEditBOStudentEmail.setText("")
            elif self.groupBoxBO.isHidden():
                self.lineEditHistStudentEmail.setText("")

        return userID, userName, userEmail

    def getItemFromID(self):
        global historyItemID

        historyItemID = self.lineEditHistItemID.text()
        self.refreshHistory()



    def listItemBOClicked(self, item):
        self.listWidgetBOName.hide()
        nameIndex = self.listWidgetBOName.currentRow()
        self.getUserFromName(nameIndex)

    def listItemEmailBOClicked(self, item):
        self.listWidgetBOEmail.hide()
        nameIndex = self.listWidgetBOEmail.currentRow()
        self.getUserFromEmail(nameIndex)

    def listItemHistClicked(self, item):
        global historyUserEmail
        self.listWidgetHistName.hide()
        nameIndex = self.listWidgetHistName.currentRow()
        self.getUserFromName(nameIndex)

        historyUserEmail = self.lineEditHistStudentEmail.text()
        self.refreshHistory()

    def listItemEmailHistClicked(self, item):
        self.listWidgetHistEmail.hide()
        nameIndex = self.listWidgetHistEmail.currentRow()
        self.getUserFromEmail(nameIndex)
        self.refreshHistory()

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
        self.lineEditHistStudentID.setText("")
        self.lineEditHistStudentName.setText("")
        self.lineEditHistStudentEmail.setText("")
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
        
        #self.tableWidgetBO.setItem(0 , 0, chkBoxItem)
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
        #self.lineEditBkdOMessage.setText(message)
        self.lineEditHistMessage.setText(message)
        self.lineEditAIMessage.setText(message)
        #self.lineEditIAMessage.setText(message)
        self.lineEditAddUserMessage.setText(message)
        self.lineEditAddItemMessage.setText(message)
        QtCore.QTimer.singleShot(2000, self.resetMessage)

    def resetMessage(self):
        self.lineEditBOMessage.setText("")
        self.lineEditReMessage.setText("")
        #self.lineEditBkdOMessage.setText("")
        self.lineEditHistMessage.setText("")
        self.lineEditAIMessage.setText("")
        #self.lineEditIAMessage.setText("")
        self.lineEditAddUserMessage.setText("")
        self.lineEditAddItemMessage.setText("")

    def clearPrev(self):
        self.tableWidgetBO.removeRow(0)

    def clearAll(self):
        self.tableWidgetBO.setRowCount(0)

    def cancelBO(self):
        self.tableWidgetBO.setRowCount(0)
        self.lineEditBOStudentID.setText("")
        self.lineEditBOStudentName.setText("")
        self.lineEditBOStudentEmail.setText("")
        self.lineEditBOStudentID.setFocus()

    def processOutgoing(self):
        userData = self.getUserFromID(self.lineEditBOStudentID.text())
        userID = userData[0]

        if userData[1] == "":
            self.doMessage("No user found")
            QtCore.QTimer.singleShot(2000, self.resetMessage)
            self.lineEditBOStudentID.setText("")
            self.lineEditBOStudentID.setFocus()

        else:
            currentDate = datetime.timestamp(datetime.now())
            listLength = self.tableWidgetBO.rowCount()

            if listLength == 0:
                self.doMessage("List empty")

            elif self.lineEditBOStudentID.text == "":
                self.doMessage("No User selected")

            else:
                i=0
                while i < listLength:
                    lineData = self.tableWidgetBO.model().index(i, 1)
                    itemID = lineData.data()
                    if self.tableWidgetBO.item(i, 0).checkState() == 2:
                        longTerm = "*"
                    else:
                        longTerm = ""

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
                self.lineEditBOStudentID.setText("")
                self.lineEditBOStudentName.setText("")
                self.lineEditBOStudentEmail.setText("")
                self.lineEditBOStudentID.setFocus()
                #while (self.tableWidgetBO.rowCount() > 0):
                #    self.tableWidgetBO.removeRow(0)

    def returnItems(self):
        tempItemInput = self.lineEditReItemID.text()
        #userID = userData[0]

        #tempItemInput = (self.root.get_screen('returns').ids.textInputItem.text)            # get text in inputItem box
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

        watchCellChange = False

        outText = outDB.all()
        DBLength = len(outDB)

        chkBoxItem = QtWidgets.QTableWidgetItem()
        chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
        
        #self.tableWidgetBO.setItem(0 , 0, chkBoxItem)

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
                #self.tableWidgetBkdO.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(longTerm))     # change to checkbox
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
                #self.tableWidgetBkdO.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(longTerm))
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

    def populateAllItems(self):
        global allItemsSearchText
        global allItemsSearchID
        global itemsPath
        
        self.lineEditAIItemSearch.setFocus()

        allItemsSearchText = self.lineEditAIItemSearch.text()
        allItemsSearchID = self.lineEditAIItemID.text()

        if allItemsSearchText != "":
            allItemsText = itemDB.search(DBquery.itemName.search(allItemsSearchText + '+', flags=re.IGNORECASE))
            allItemsText += itemDB.search(DBquery.itemMake.search(allItemsSearchText + '+', flags=re.IGNORECASE))
            allItemsText += itemDB.search(DBquery.itemModel.search(allItemsSearchText + '+', flags=re.IGNORECASE))
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

        self.tableWidgetAI.setRowCount(0)

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
        
            rowPosition = self.tableWidgetAI.rowCount()
            self.tableWidgetAI.insertRow(rowPosition)

            self.tableWidgetAI.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(itemID))
            self.tableWidgetAI.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(itemName))
            self.tableWidgetAI.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(itemMake))
            self.tableWidgetAI.setItem(rowPosition , 3, QtWidgets.QTableWidgetItem(itemModel))
            self.tableWidgetAI.setItem(rowPosition , 4, QtWidgets.QTableWidgetItem(itemSerial))

            i +=1

        pdf.output(itemsPath)

    def clearAllItems(self):
        self.lineEditAIItemSearch.setText("")
        self.lineEditAIItemID.setText("")
        self.populateAllItems()

    def refreshHistory(self):
        global historyPath
        global dateRangeFrom
        global dateRangeTo
        global historyItemID
        global historyUserEmail

        self.tableWidgetHist.setRowCount(0)

        historyUserEmail = self.lineEditHistStudentEmail.text()

        dateRangeFrom = self.dateEditFrom.date()
        dateRangeFrom = str(dateRangeFrom.toPyDate())
        dateRangeFrom = time.mktime(datetime.strptime(dateRangeFrom, "%Y-%m-%d").timetuple())

        dateRangeTo = self.dateEditTo.date()
        dateRangeTo = dateRangeTo.toPyDate()
        dateRangeTo = str(dateRangeTo + timedelta(days=1))
        dateRangeTo = time.mktime(datetime.strptime(dateRangeTo, "%Y-%m-%d").timetuple())

        #print(dateRangeFrom)
        #print(dateRangeTo)
        
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

    def addItemIDCheck(self):
        itemID = self.lineEditAddItemID.text()
        itemIDSearch = (itemDB.search(DBquery.itemID == itemID))
        
        itemName = (itemIDSearch[0]['itemName'])
        itemMake = (itemIDSearch[0]['itemMake'])
        itemModel = (itemIDSearch[0]['itemModel'])
        itemSerial = (itemIDSearch[0]['itemSerial'])

        if itemIDSearch != "":
            self.doMessage("Item ID Already Used")
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
