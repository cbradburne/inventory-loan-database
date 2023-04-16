#macOS
# pip3 install https://github.com/kivy/kivy/archive/master.zip
# pip3 install https://github.com/kivymd/KivyMD/archive/master.zip
# pip3 install pygame
# pip3 install tinydb
# pip3 install FPDF
# pip3 install pyinstaller

#Windows
# python -m pip install https://github.com/kivy/kivy/archive/master.zip
# python -m pip install https://github.com/kivymd/KivyMD/archive/master.zip
# python -m pip install pygame
# python -m pip install tinydb
# python -m pip install FPDF
# python -m pip install pyinstaller

# python -m PyInstaller --onefile --windowed Database.py
# python -m PyInstaller app.spec

from kivy.metrics import dp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivymd.app import MDApp
from kivy.utils import platform
from kivy.uix.button import Button
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.dropdownitem import MDDropDownItem
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.config import Config
from datetime import datetime
from datetime import timedelta
from tinydb import TinyDB
from tinydb import Query
from tinydb import where
from fpdf import FPDF
import shlex
import os, sys
from pathlib import Path
import tempfile
import time
import subprocess

Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'width', '1600')
Config.set('graphics', 'window_state', 'windowed')
Config.set('graphics', 'height', '900')
Config.write()

class MainWindow(Screen):
    pass
class SecondWindow(Screen):
    pass
class ThirdWindow(Screen):
    pass
class FourthWindow(Screen):
    pass
class FifthWindow(Screen):
    pass
class SixthWindow(Screen):
    pass
class WindowManager(ScreenManager):
    pass

itemID = ""
userID = ""
outID = ""
returnID = ""

DBquery = Query()

pdf_filename = ""
runThisTime = True
isWindows = True
dateRangeFrom = 0.0
dateRangeTo = 0.0
showNamesList = False
checkboxState = False
showLongTerm = False
historyItemID = ""
historyUserEmail = ""

if platform == "win32" or platform == "Windows" or platform == "win":                           # Tests if using Windows as different OS has different Printer code
    isWindows = True
    itemDB = TinyDB('C:\\Users\\Public\\Documents\\Database\\itemdb.json')
    userDB = TinyDB('C:\\Users\\Public\\Documents\\Database\\userdb.json')
    outDB = TinyDB('C:\\Users\\Public\\Documents\\Database\\outdb.json')
    historyDB = TinyDB('C:\\Users\\Public\\Documents\\Database\\historydb.json')
    bookedOutPath = 'C:\\Users\\Public\\Documents\\Database\\BookedOut.pdf'
    historyPath = 'C:\\Users\\Public\\Documents\\Database\\History.pdf'
    print("IS Windows")
else:
    isWindows = False
    itemDB = TinyDB('/Users/Shared/Database/itemdb.json')
    userDB = TinyDB('/Users/Shared/Database/userdb.json')
    outDB = TinyDB('/Users/Shared/Database/outdb.json')
    historyDB = TinyDB('/Users/Shared/Database/historydb.json')
    bookedOutPath = '/Users/Shared/Database/BookedOut.pdf'
    historyPath = '/Users/Shared/Database/History.pdf'
    print("is NOT Windows")

KV = '''
#:import NoTransition kivy.uix.screenmanager.NoTransition

WindowManager:
    transition: NoTransition()
    MainWindow:
    SecondWindow:
    ThirdWindow:
    FourthWindow:
    FifthWindow:
    SixthWindow:

<MainWindow>:
    name: 'main'
    MDScreen:
        id: main
        MDFlatButton:
            id: mainScreenButton
            text: "Collect"
            text_color: 0, 0, 1, 1
            line_width: 2.4
            line_color: 1, 0.4, 0.4, 1
            pos_hint: {"center_x": .1, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenMain()

        MDFlatButton:
            id: returnsScreenButton
            text: "Returns"
            text_color: 0, 0, 1, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            pos_hint: {"center_x": .23, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenReturn()

        MDFlatButton:
            id: bookedOutScreenButton
            text: "Booked Out"
            text_color: 0, 0, 1, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            pos_hint: {"center_x": .435, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenbookedOut()

        MDFlatButton:
            id: historyScreenButton
            text: "History"
            text_color: 0, 0, 1, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            pos_hint: {"center_x": .565, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenHistory()

        MDFlatButton:
            id: addUserScreenButton
            text: "Add User"
            text_color: 0, 0, 1, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            pos_hint: {"center_x": .77, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenAddUser()

        MDFlatButton:
            id: addItemScreenButton
            text: "Add Item"
            text_color: 0, 0, 1, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            pos_hint: {"center_x": .9, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenAddItem()

        MDTextField:
            id: textInputUserID
            mode: "rectangle"
            hint_text: "User ID"
            #helper_text: "User ID"
            helper_text_mode: "on_error"
            pos_hint: {"center_x": .2, "center_y": .87}
            size_hint_x: 0.2
            text_color_normal: "white"
        
        MDTextField:
            id: textInputUserName
            mode: "rectangle"
            hint_text: "Name"
            #helper_text: "Name"
            helper_text_mode: "on_error"
            pos_hint: {"center_x": .5, "center_y": .87}
            size_hint_x: 0.3
            text_color_normal: "white"
        
        MDTextField:
            id: textInputUserEmail
            mode: "rectangle"
            hint_text: "Email"
            #helper_text: "Email"
            helper_text_mode: "on_error"
            pos_hint: {"center_x": .8, "center_y": .87}
            size_hint_x: 0.2
            text_color_normal: "white"

        MDTextField:
            id: textInputItem
            mode: "rectangle"
            hint_text: "Item ID Number"
            #helper_text: "Item ID Number"
            helper_text_mode: "on_error"
            pos_hint: {"center_x": .2, "center_y": .77}
            size_hint_x: 0.2
            text_color_normal: "white"

        MDTextField:
            id: textErrorMain
            mode: "rectangle"
            hint_text: "Message Box"
            #helper_text: "Message Box"
            helper_text_mode: "on_error"
            pos_hint: {"center_x": .8, "center_y": .77}
            size_hint_x: 0.2
            text_color_normal: "red"

        Label:
            text: 'LongTerm'
            size_hint_y: None
            size_hint_x: 0.08
            pos_hint: {'center_x': .27, 'center_y': .71}
            text_size: self.width,None
            color: 1,1,1,1

        MDCheckbox:
            id: longTermCheckbox
            size: "48dp", "48dp"
            size_hint: None,None
            pos_hint: {'center_x': .29, 'center_y': .71}
            on_active: app.on_checkbox_active(*args)

        AnchorLayout:
            id: data_layout
            pos_hint: {"center_x": .5, "center_y": .39}

        MDFlatButton:
            id: outButton
            text: "Process"
            text_color: 0, 0, 1, 1
            line_width: 2
            line_color: 0.2, 0.7, 0.2, 1
            pos_hint: {"center_x": .85, "center_y": .05}
            size_hint: (0.1), (0.02)
            font_size: "18sp"
            on_release: app.processOutgoing()

        ScrollView:
            id: userListDD
            #pos_hint: {'x':2, 'y':2}
            pos_hint: {"center_x": 2, "center_y": 2}
            #pos: 1, 1
            size_hint: (0.2), (0.2)
            do_scroll_x: False
            BoxLayout:
                id: box_list
                orientation: 'vertical'
                on_parent: app.uiDict['box_list'] = self
                size: (0.2), (0.6)
                size_hint: None, None
                height: max(self.parent.height, self.minimum_height)

        MDFlatButton:
            id: outClearButton
            text: "Clear"
            text_color: 0, 0, 1, 1
            line_width: 2
            line_color: 0.7, 0.2, 0.2, 1
            pos_hint: {"center_x": .15, "center_y": .05}
            size_hint: (0.1), (0.02)
            font_size: "18sp"
            on_release: app.remove_all_rows()
            
<SecondWindow>:
    name: 'returns'
    MDScreen:
        id: returns
        FloatLayout:
            size_hint: (1), (0.8)
            ScrollView:
                do_scroll_x: False
                do_scroll_y: True
                pos_hint: {'x':0, 'y':0.1}
                BoxLayout:
                    size_hint_y:None
                    height:self.minimum_height
                    Label:
                        id: fillerLeft
                        text: ''
                        size_hint_y: None
                        size_hint_x: 0.02
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

                    Label:
                        id: returnBoxItemID
                        text: ''
                        size_hint_y: None
                        size_hint_x: 0.03
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

                    Label:
                        id: returnBoxItemName
                        text: ''
                        size_hint_y: None
                        size_hint_x: 0.26
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

                    Label:
                        id: returnBoxUserName
                        text: ''
                        size_hint_y: None
                        size_hint_x: 0.15
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

                    Label:
                        id: returnBoxUserEmail
                        text: ''
                        size_hint_y: None
                        size_hint_x: 0.22
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

                    Label:
                        id: returnBoxDate
                        text: ''
                        #pos_hint: {.35, .9}
                        size_hint_y: None
                        size_hint_x: 0.15
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

                    Label:
                        id: fillerRight
                        text: ''
                        size_hint_y: None
                        size_hint_x: 0.02
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

        MDFlatButton:
            id: mainScreenButton
            text: "Collect"
            text_color: 0, 0, 1, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            pos_hint: {"center_x": .1, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenMain()

        MDFlatButton:
            id: returnsScreenButton
            text: "Returns"
            text_color: 0, 0, 1, 1
            line_width: 2.4
            line_color: 1, 0.4, 0.4, 1
            pos_hint: {"center_x": .23, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenReturn()

        MDFlatButton:
            id: bookedOutScreenButton
            text: "Booked Out"
            text_color: 0, 0, 1, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            pos_hint: {"center_x": .435, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenbookedOut()

        MDFlatButton:
            id: historyScreenButton
            text: "History"
            text_color: 0, 0, 1, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            pos_hint: {"center_x": .565, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenHistory()

        MDFlatButton:
            id: addUserScreenButton
            text: "Add User"
            text_color: 0, 0, 1, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            pos_hint: {"center_x": .77, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenAddUser()

        MDFlatButton:
            id: addItemScreenButton
            text: "Add Item"
            text_color: 0, 0, 1, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            pos_hint: {"center_x": .9, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenAddItem()

        MDTextField:
            id: textInputItem
            mode: "rectangle"
            hint_text: "Item ID Number"
            #helper_text: "Item ID Number"
            helper_text_mode: "on_error"
            pos_hint: {"center_x": .2, "center_y": .87}
            size_hint_x: 0.2

        MDTextField:
            id: textErrorReturn
            mode: "rectangle"
            hint_text: "Message Box"
            #helper_text: "Message Box"
            helper_text_mode: "on_error"
            pos_hint: {"center_x": .8, "center_y": .87}
            size_hint_x: 0.2
            text_color_normal: "red"

        AnchorLayout:
            id: data_layout_returns

<ThirdWindow>:
    name: 'bookedout'
    MDScreen:
        id: bookedout
        FloatLayout:
            size_hint: (1), (0.8)
            ScrollView:
                do_scroll_x: False
                do_scroll_y: True
                pos_hint: {'x':0, 'y':0.1}
                BoxLayout:
                    size_hint_y:None
                    height:self.minimum_height
                    Label:
                        id: fillerLeft
                        text: ''
                        size_hint_y: None
                        size_hint_x: 0.02
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

                    Label:
                        id: bookedOutBoxItemID
                        text: ''
                        size_hint_y: None
                        size_hint_x: 0.03
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

                    Label:
                        id: bookedOutBoxItemName
                        text: ''
                        size_hint_y: None
                        size_hint_x: 0.26
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

                    Label:
                        id: bookedOutBoxUserName
                        text: ''
                        size_hint_y: None
                        size_hint_x: 0.15
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

                    Label:
                        id: bookedOutBoxUserEmail
                        text: ''
                        size_hint_y: None
                        size_hint_x: 0.22
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

                    Label:
                        id: bookedOutBoxDate
                        text: ''
                        #pos_hint: {.35, .9}
                        size_hint_y: None
                        size_hint_x: 0.15
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

                    Label:
                        id: fillerRight
                        text: ''
                        size_hint_y: None
                        size_hint_x: 0.02
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

        MDFlatButton:
            id: mainScreenButton
            text: "Collect"
            text_color: 0, 0, 1, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            pos_hint: {"center_x": .1, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenMain()

        MDFlatButton:
            id: returnsScreenButton
            text: "Returns"
            text_color: 0, 0, 1, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            pos_hint: {"center_x": .23, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenReturn()

        MDFlatButton:
            id: bookedOutScreenButton
            text: "Booked Out"
            text_color: 0, 0, 1, 1
            line_width: 2.4
            line_color: 1, 0.4, 0.4, 1
            pos_hint: {"center_x": .435, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenbookedOut()

        MDFlatButton:
            id: historyScreenButton
            text: "History"
            text_color: 0, 0, 1, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            pos_hint: {"center_x": .565, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenHistory()

        MDFlatButton:
            id: addUserScreenButton
            text: "Add User"
            text_color: 0, 0, 1, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            pos_hint: {"center_x": .77, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenAddUser()

        MDFlatButton:
            id: addItemScreenButton
            text: "Add Item"
            text_color: 0, 0, 1, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            pos_hint: {"center_x": .9, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenAddItem()

        Label:
            text: 'Include LongTerm'
            size_hint_y: None
            size_hint_x: 0.12
            pos_hint: {"center_x": .47, "center_y": .91}
            text_size: self.width,None
            color: 1,1,1,1

        MDCheckbox:
            id: includelongTermCheckbox
            size: "48dp", "48dp"
            size_hint: None,None
            pos_hint: {"center_x": .52, "center_y": .91}
            on_active: app.on_checkbox_active_bookedOut(*args)

        MDFlatButton:
            id: exportBooked
            text: "Export"
            text_color: 0, 0, 1, 1
            line_width: 2
            line_color: 0.7, 0.7, 0.2, 1
            pos_hint: {"center_x": .85, "center_y": .05}
            size_hint: (0.1), (0.02)
            font_size: "18sp"
            on_release: app.exportBooked()

<FourthWindow>:
    name: 'history'
    MDScreen:
        id: history
        FloatLayout:
            size_hint: (1), (0.8)
            ScrollView:
                do_scroll_x: False
                do_scroll_y: True
                pos_hint: {'x':0, 'y':0.1}
                BoxLayout:
                    size_hint_y:None
                    height:self.minimum_height
                    Label:
                        id: fillerLeft
                        text: ''
                        size_hint_y: None
                        size_hint_x: 0.02
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

                    Label:
                        id: historyBoxItemID
                        text: ''
                        size_hint_y: None
                        size_hint_x: 0.03
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

                    Label:
                        id: historyBoxItemName
                        text: ''
                        size_hint_y: None
                        size_hint_x: 0.26
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

                    Label:
                        id: historyBoxUserName
                        text: ''
                        size_hint_y: None
                        size_hint_x: 0.15
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

                    Label:
                        id: historyBoxUserEmail
                        text: ''
                        size_hint_y: None
                        size_hint_x: 0.22
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

                    Label:
                        id: historyBoxDateOut
                        text: ''
                        size_hint_y: None
                        size_hint_x: 0.075
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

                    Label:
                        id: historyBoxDateIn
                        text: ''
                        size_hint_y: None
                        size_hint_x: 0.075
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

                    Label:
                        id: fillerRight
                        text: ''
                        size_hint_y: None
                        size_hint_x: 0.02
                        height: 1000
                        text_size: self.width,None
                        color: 1,1,1,1
                        markup: True

        MDFlatButton:
            id: mainScreenButton
            text: "Collect"
            text_color: 0, 0, 1, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            pos_hint: {"center_x": .1, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenMain()

        MDFlatButton:
            id: returnsScreenButton
            text: "Returns"
            text_color: 0, 0, 1, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            pos_hint: {"center_x": .23, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenReturn()

        MDFlatButton:
            id: bookedOutScreenButton
            text: "Booked Out"
            text_color: 0, 0, 1, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            pos_hint: {"center_x": .435, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenbookedOut()

        MDFlatButton:
            id: historyScreenButton
            text: "History"
            text_color: 0, 0, 1, 1
            line_width: 2.4
            line_color: 1, 0.4, 0.4, 1
            pos_hint: {"center_x": .565, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenHistory()

        MDFlatButton:
            id: addUserScreenButton
            text: "Add User"
            text_color: 0, 0, 1, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            pos_hint: {"center_x": .77, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenAddUser()

        MDFlatButton:
            id: addItemScreenButton
            text: "Add Item"
            text_color: 0, 0, 1, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            pos_hint: {"center_x": .9, "center_y": .97}
            size_hint: (0.1), (0.01)
            font_size: "18sp"
            on_release: app.goToScreenAddItem()

        MDTextField:
            id: textInputHistoryItemID
            mode: "rectangle"
            hint_text: "Item ID"
            helper_text_mode: "on_error"
            pos_hint: {"center_x": .1, "center_y": .915}
            size_hint_x: 0.1
            text_color_normal: "white"
            text: ""

        MDTextField:
            id: textInputhistoryUserEmail
            mode: "rectangle"
            hint_text: "Email"
            helper_text_mode: "on_error"
            pos_hint: {"center_x": .2, "center_y": .915}
            size_hint_x: 0.1
            text_color_normal: "white"
            text: ""         

        MDFlatButton:
            id: historyDatePickerButton
            text: "Date Range"
            text_color: 1, 1, 1, 1
            line_width: 1.2
            line_color: 0.1, 0.5, 0.5, 1
            size_hint: (0.1), (0.01)
            pos_hint: {"center_x": .33, "center_y": .91}
            font_size: "18sp"
            on_release: app.historyDatePicker()

        MDFlatButton:
            id: historyFromDatePicker
            text: "-"
            text_color: 1, 1, 1, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            size_hint: (0.1), (0.01)
            pos_hint: {"center_x": .445, "center_y": .91}
            font_size: "18sp"

        MDFlatButton:
            id: historyToDatePicker
            text: "-"
            text_color: 0.5, 0.5, 0.5, 1
            line_width: 1.2
            line_color: 0.4, 0.4, 0.4, 1
            size_hint: (0.1), (0.01)
            pos_hint: {"center_x": .555, "center_y": .91}
            font_size: "18sp"

        MDFlatButton:
            id: historyDateResetButton
            text: "Reset Range"
            text_color: 1, 1, 1, 1
            line_width: 1.2
            line_color: 0.1, 0.5, 0.5, 1
            size_hint: (0.1), (0.01)
            pos_hint: {"center_x": .67, "center_y": .91}
            font_size: "18sp"
            on_release: app.historyDateReset()

        MDFlatButton:
            id: exportHistory
            text: "Export"
            text_color: 0, 0, 1, 1
            line_width: 2
            line_color: 0.7, 0.7, 0.2, 1
            pos_hint: {"center_x": .85, "center_y": .05}
            size_hint: (0.1), (0.02)
            font_size: "18sp"
            on_release: app.exportHistory()

<FifthWindow>:
    name: 'addUser'
    MDScreen:
        id: addUser
        MDFloatLayout:
            MDFlatButton:
                id: mainScreenButton
                text: "Collect"
                text_color: 0, 0, 1, 1
                line_width: 1.2
                line_color: 0.4, 0.4, 0.4, 1
                pos_hint: {"center_x": .1, "center_y": .97}
                size_hint: (0.1), (0.01)
                font_size: "18sp"
                on_release: app.goToScreenMain()

            MDFlatButton:
                id: returnsScreenButton
                text: "Returns"
                text_color: 0, 0, 1, 1
                line_width: 1.2
                line_color: 0.4, 0.4, 0.4, 1
                pos_hint: {"center_x": .23, "center_y": .97}
                size_hint: (0.1), (0.01)
                font_size: "18sp"
                on_release: app.goToScreenReturn()

            MDFlatButton:
                id: bookedOutScreenButton
                text: "Booked Out"
                text_color: 0, 0, 1, 1
                line_width: 1.2
                line_color: 0.4, 0.4, 0.4, 1
                pos_hint: {"center_x": .435, "center_y": .97}
                size_hint: (0.1), (0.01)
                font_size: "18sp"
                on_release: app.goToScreenbookedOut()

            MDFlatButton:
                id: historyScreenButton
                text: "History"
                text_color: 0, 0, 1, 1
                line_width: 1.2
                line_color: 0.4, 0.4, 0.4, 1
                pos_hint: {"center_x": .565, "center_y": .97}
                size_hint: (0.1), (0.01)
                font_size: "18sp"
                on_release: app.goToScreenHistory()

            MDFlatButton:
                id: addUserScreenButton
                text: "Add User"
                text_color: 0, 0, 1, 1
                line_width: 2.4
                line_color: 1, 0.4, 0.4, 1
                pos_hint: {"center_x": .77, "center_y": .97}
                size_hint: (0.1), (0.01)
                font_size: "18sp"
                on_release: app.goToScreenAddUser()

            MDFlatButton:
                id: addItemScreenButton
                text: "Add Item"
                text_color: 0, 0, 1, 1
                line_width: 1.2
                line_color: 0.4, 0.4, 0.4, 1
                pos_hint: {"center_x": .9, "center_y": .97}
                size_hint: (0.1), (0.01)
                font_size: "18sp"
                on_release: app.goToScreenAddItem()

            MDTextField:
                id: textInputAddUserID
                mode: "rectangle"
                hint_text: "User ID"
                #helper_text: "User ID"
                helper_text_mode: "on_error"
                pos_hint: {"center_x": .3, "center_y": .8}
                size_hint_x: 0.2
                text_color_normal: "white"

            MDTextField:
                id: textInputAddUserFirstName
                mode: "rectangle"
                hint_text: "First Name"
                #helper_text: "Fisrt Name"
                helper_text_mode: "on_error"
                pos_hint: {"center_x": .3, "center_y": .7}
                size_hint_x: 0.2
                text_color_normal: "white"

            MDTextField:
                id: textInputAddUserLastName
                mode: "rectangle"
                hint_text: "Last name"
                #helper_text: "Last name"
                helper_text_mode: "on_error"
                pos_hint: {"center_x": .3, "center_y": .6}
                size_hint_x: 0.2
                text_color_normal: "white"

            MDTextField:
                id: textInputAddUserEmail
                mode: "rectangle"
                hint_text: "User Email"
                #helper_text: "User Email"
                helper_text_mode: "on_error"
                pos_hint: {"center_x": .3, "center_y": .5}
                size_hint_x: 0.2
                text_color_normal: "white"

            MDTextField:
                id: textErrorAddUser
                mode: "rectangle"
                hint_text: "Message Box"
                #helper_text: "Message Box"
                helper_text_mode: "on_error"
                pos_hint: {"center_x": .75, "center_y": .8}
                size_hint_x: 0.2
                text_color_normal: "red"

            MDFlatButton:
                id: addUserSaveButton
                text: "Save User"
                text_color: 0, 0, 1, 1
                line_width: 2.4
                line_color: 0.2, 0.7, 0.2, 1
                pos_hint: {"center_x": .7, "center_y": .3}
                size_hint: (0.1), (0.01)
                font_size: "18sp"
                on_release: app.addUserSave()

<SixthWindow>:
    name: 'addItem'
    MDScreen:
        id: addItem
        MDFloatLayout:
            MDFlatButton:
                id: mainScreenButton
                text: "Collect"
                text_color: 0, 0, 1, 1
                line_width: 1.2
                line_color: 0.4, 0.4, 0.4, 1
                pos_hint: {"center_x": .1, "center_y": .97}
                size_hint: (0.1), (0.01)
                font_size: "18sp"
                on_release: app.goToScreenMain()

            MDFlatButton:
                id: returnsScreenButton
                text: "Returns"
                text_color: 0, 0, 1, 1
                line_width: 1.2
                line_color: 0.4, 0.4, 0.4, 1
                pos_hint: {"center_x": .23, "center_y": .97}
                size_hint: (0.1), (0.01)
                font_size: "18sp"
                on_release: app.goToScreenReturn()

            MDFlatButton:
                id: bookedOutScreenButton
                text: "Booked Out"
                text_color: 0, 0, 1, 1
                line_width: 1.2
                line_color: 0.4, 0.4, 0.4, 1
                pos_hint: {"center_x": .435, "center_y": .97}
                size_hint: (0.1), (0.01)
                font_size: "18sp"
                on_release: app.goToScreenbookedOut()

            MDFlatButton:
                id: historyScreenButton
                text: "History"
                text_color: 0, 0, 1, 1
                line_width: 1.2
                line_color: 0.4, 0.4, 0.4, 1
                pos_hint: {"center_x": .565, "center_y": .97}
                size_hint: (0.1), (0.01)
                font_size: "18sp"
                on_release: app.goToScreenHistory()

            MDFlatButton:
                id: addUserScreenButton
                text: "Add User"
                text_color: 0, 0, 1, 1
                line_width: 1.2
                line_color: 0.4, 0.4, 0.4, 1
                pos_hint: {"center_x": .77, "center_y": .97}
                size_hint: (0.1), (0.01)
                font_size: "18sp"
                on_release: app.goToScreenAddUser()

            MDFlatButton:
                id: addItemScreenButton
                text: "Add Item"
                text_color: 0, 0, 1, 1
                line_width: 2.4
                line_color: 1, 0.4, 0.4, 1
                pos_hint: {"center_x": .9, "center_y": .97}
                size_hint: (0.1), (0.01)
                font_size: "18sp"
                on_release: app.goToScreenAddItem()

            MDTextField:
                id: textInputAddItemID
                mode: "rectangle"
                hint_text: "Item ID"
                #helper_text: "Item ID"
                helper_text_mode: "on_error"
                pos_hint: {"center_x": .3, "center_y": .8}
                size_hint_x: 0.2
                text_color_normal: "white"

            MDTextField:
                id: textInputAddItemSerialNo
                mode: "rectangle"
                hint_text: "Serial No"
                #helper_text: "Serial No"
                helper_text_mode: "on_error"
                pos_hint: {"center_x": .3, "center_y": .7}
                size_hint_x: 0.2
                text_color_normal: "white"

            MDTextField:
                id: textInputAddItemName
                mode: "rectangle"
                hint_text: "Item Name"
                #helper_text: "Item Name"
                helper_text_mode: "on_error"
                pos_hint: {"center_x": .3, "center_y": .6}
                size_hint_x: 0.2
                text_color_normal: "white"

            MDTextField:
                id: textInputAddItemMake
                mode: "rectangle"
                hint_text: "Item Manufacturer"
                #helper_text: "Item Manufacturer"
                helper_text_mode: "on_error"
                pos_hint: {"center_x": .3, "center_y": .5}
                size_hint_x: 0.2
                text_color_normal: "white"

            MDTextField:
                id: textInputAddItemModel
                mode: "rectangle"
                hint_text: "Item Model"
                #helper_text: "Item Model"
                helper_text_mode: "on_error"
                pos_hint: {"center_x": .3, "center_y": .4}
                size_hint_x: 0.2
                text_color_normal: "white"

            MDTextField:
                id: textErrorAddItem
                mode: "rectangle"
                hint_text: "Message Box"
                #helper_text: "Message Box"
                helper_text_mode: "on_error"
                pos_hint: {"center_x": .75, "center_y": .8}
                size_hint_x: 0.2
                text_color_normal: "red"

            MDFlatButton:
                id: addItemClearButton
                text: "Clear"
                text_color: 0, 0, 1, 1
                line_width: 2
                line_color: 0.7, 0.2, 0.2, 1
                pos_hint: {"center_x": .15, "center_y": .3}
                size_hint: (0.1), (0.01)
                font_size: "18sp"
                on_release: app.addItemClear(0)

            MDFlatButton:
                id: addItemSaveButton
                text: "Save Item"
                text_color: 0, 0, 1, 1
                line_width: 2.4
                line_color: 0.2, 0.7, 0.2, 1
                pos_hint: {"center_x": .7, "center_y": .3}
                size_hint: (0.1), (0.01)
                font_size: "18sp"
                on_release: app.addItemSave()
'''

class MainApp(MDApp):
    def build(self):
        self.title = 'Database'
        self.icon = 'dbIcon.png'
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"
        self.uiDict = {}
        Window.bind(on_key_down = self.keyDown)
        Clock.schedule_once(self.add_datatable, 0)                                              # Clock.schedule_one runs the function after "0" seconds (ie next program cycle)
        Clock.schedule_once(self.resetTextInputItemMain, 0)                                     # Sets the "focused" text box
        return Builder.load_string(KV)
    
    def add_datatable(self, dt):
        self.data_tables = MDDataTable(
            size_hint=(0.8, 0.6),
            check=True,
            rows_num=20,
            column_data=[
                ("Item ID", dp(50)),
                ("Item Name", dp(150)),
                ("Long Term", dp(30)),
                ("No.", dp(13))
            ])
        
        #.data_tables.bind(on_row_presss=self.on_row_press)
        self.data_tables.bind(on_check_press=self.on_check_press)                               # Binds the check box mouse click to the function "on_check_press"
        self.root.get_screen('main').ids.data_layout.add_widget(self.data_tables)               # Adds the DataTable to the GUI

    def add_row(self, tempItemInput, tempItemName, longTerm) -> None:                           # Adds an item to the DataTable
        if len(self.data_tables.row_data) == 0:                                                 # If there are NO rows - no need to sort rows when there's only 1 row
            self.data_tables.add_row((tempItemInput, tempItemName, longTerm, (len(self.data_tables.row_data) + 1)))       # Add row with sorting number one more than the number of rows
        else:    
            self.data_tables.add_row((tempItemInput, tempItemName, longTerm, (len(self.data_tables.row_data) + 1)))       # Add row with sorting number one more than the number of rows
            sortedData = sorted(self.data_tables.row_data, key = lambda x: x[3], reverse=True)  # Sort data so last item it top
            self.data_tables.row_data = sortedData                                              # Replace data with sorted data

    def remove_all_rows(self):                                                                  # Removes all rows from DataTable
        while len(self.data_tables.row_data) > 0:                                               # Finds the current number of rows in the DataTable
            self.data_tables.remove_row(self.data_tables.row_data[-1])                          # Removes the correct number of rows in the DataTable
        
        Clock.schedule_once(self.resetTextInputItemMain, 0)                                     # run "clearTextInputItemMain" on next cycle

    def on_check_press(self, instance_table, current_row):                                      # Mouse cliked a Check Mark in the DataTable
        global runThisTime                                                                      # Check marks don't automatically get removed after the row is removed, when check marks are removed, it runs this code again, therefore needs to be bypassed when that happens.
        
        listLength = len(self.data_tables.row_data)                                             # Store number of dataTable rows
        listLengthOG = len(self.data_tables.row_data)

        i=0
        if runThisTime:                                                                         # Bypass setup for repeat *see above
            runThisTime = False
            while i < listLength:                                                               # Iterate through rows
                if self.data_tables.row_data[i][0] == current_row[0]:                           # Compare row i itemID to the row checked itemID to find which row has been clicked
                    self.data_tables.table_data.select_all("normal")                            # Remove all check marks from DataTable
                    self.data_tables.remove_row(self.data_tables.row_data[i])                   # If they equal, remove the current row iteration
                    listLength -= 1                                                             # minus 1 from the length of the list as we've just removed a row

                else:
                    self.data_tables.update_row(
                        self.data_tables.row_data[i],                                           # For row i
                        [self.data_tables.row_data[i][0],                                       # Old row data - itemID
                        self.data_tables.row_data[i][1],                                        # Old row data - itemName
                        self.data_tables.row_data[i][2],                                        # Old row data - longTerm
                        (listLengthOG - i -1)])                                                 # New row data
                                                                                                
                i +=1
        else:                                                                                   # Increment i
            runThisTime = True
            Clock.schedule_once(self.clearTextInputItemMain, 0)
    
    def on_row_press(self, instance_table, instance_row):
        row_num = int(instance_row.index/len(instance_table.column_data))
        row_data = instance_table.row_data[row_num]
        
        if row_data['longTerm'] == "*":
            self.data_tables.update_row(
                self.data_tables.row_data[i],                                                   # For row i
                [self.data_tables.row_data[i][0],                                               # Old row data - itemID
                self.data_tables.row_data[i][1],                                                # Old row data - itemName
                "",                                                                             # New row data - longTerm
                self.data_tables.row_data[i][3]])                                               # New row data
        else:
            self.data_tables.update_row(
                self.data_tables.row_data[i],                                                   # For row i
                [self.data_tables.row_data[i][0],                                               # Old row data - itemID
                self.data_tables.row_data[i][1],                                                # Old row data - itemName
                "*",                                                                            # New row data - longTerm
                self.data_tables.row_data[i][3]])                                               # New row data

        print (row_data)

    def on_checkbox_active(self, checkbox, value):
        global checkboxState

        if value:
            #print('The checkbox', checkbox, 'is active', 'and', checkbox.state, 'state')
            if checkbox.state == "normal":
                checkboxState = False
            elif checkbox.state == "down":
                checkboxState = True

        else:
            checkboxState = False

    def on_checkbox_active_bookedOut(self, checkbox, value):
        global showLongTerm

        if value:
            #print('The checkbox', checkbox, 'is active', 'and', checkbox.state, 'state')
            if checkbox.state == "normal":
                showLongTerm = False
                self.goToScreenbookedOut()
                
            elif checkbox.state == "down":
                showLongTerm = True
                self.goToScreenbookedOut()
        else:
            showLongTerm = False
            self.goToScreenbookedOut()

    def set_item(self, text_item):
        self.screen.ids.drop_item.set_item(text_item)
        self.menu.dismiss()

    def keyDown(self, instance, keyboard, keycode, text, modifiers):                            # Activates everytime a key pressed
        global userID
        global checkboxState
        global historyItemID
        global historyUserEmail

        if keycode == 40 or keycode == 88:                                                      # on "return" key pressed

            # BOOKING - userID input

            if self.root.get_screen('main').ids.textInputUserID.focus == True:                  # If "userID" input box on the main page has keyboard focus
                userID = (self.root.get_screen('main').ids.textInputUserID.text)                # Get the text of the "userID" input box on the main page
                if len(userID) > 5:
                    userID = userID.rstrip(userID[-1])
                    foundID = userDB.search(where('userID').matches(userID + '.*'))
                    userID = (foundID[0]['userID'])

                getUser = (userDB.search(DBquery.userID == userID))                             # search for user number in item database
                
                if not getUser:                                                                 # If user not found...
                    self.root.get_screen('main').ids.textErrorMain.text = "No user found"       # Add text to main page message box
                    Clock.schedule_once(self.resetTextErrorAll, 2)                              # Remove text in main page message box after 2 seconds
                    Clock.schedule_once(self.resetTextInputItemMain, 0)

                else:
                    userName = (getUser[0]['firstName']) + " " + (getUser[0]['lastName'])
                    userEmail = (getUser[0]['email'])

                    self.root.get_screen('main').ids.textInputUserName.text = userName
                    self.root.get_screen('main').ids.textInputUserEmail.text = userEmail

                    Clock.schedule_once(self.clearTextInputItemMain, 0)

            # BOOKING - userName input

            elif self.root.get_screen('main').ids.textInputUserName.focus == True:
                foundNames = userDB.search((where('lastName').matches( self.root.get_screen('main').ids.textInputUserName.text.capitalize() + '.*')) & (DBquery.userID != ""))
                if len(foundNames) == 1:

                    userID = (foundNames[0]['userID'])
                    userName = (foundNames[0]['firstName']) + " " + (foundNames[0]['lastName'])
                    userEmail = (foundNames[0]['email'])

                    self.root.get_screen('main').ids.textInputUserID.text = userID
                    self.root.get_screen('main').ids.textInputUserName.text = userName
                    self.root.get_screen('main').ids.textInputUserEmail.text = userEmail

                    Clock.schedule_once(self.clearTextInputItemMain, 0)

                elif len(foundNames) > 1:
                    userNameList = []
                    i=0
                    while i < len(foundNames):
                        userID = (foundNames[i]['userID'])
                        getUser = (userDB.search(DBquery.userID == userID)) 
                        userName = (getUser[0]['firstName']) + " " + (getUser[0]['lastName'])
                        userNameList.append(userName)

                        i += 1

                    self.showNamesList(userNameList)

                else:
                    self.root.get_screen('main').ids.textErrorMain.text = "No user found"
                    Clock.schedule_once(self.resetTextErrorAll, 2)
                    Clock.schedule_once(self.resetTextInputItemMain, 0)

            # BOOKING - userEmail input

            elif self.root.get_screen('main').ids.textInputUserEmail.focus == True:
                userEmail = (self.root.get_screen('main').ids.textInputUserEmail.text)
                getUser = (userDB.search(DBquery.email == userEmail))                           # search for email address in item database

                if not getUser:
                    self.root.get_screen('main').ids.textErrorMain.text = "No user found"
                    Clock.schedule_once(self.resetTextErrorAll, 2)
                    Clock.schedule_once(self.resetTextInputItemMain, 0)
                else:
                    userID = (getUser[0]['userID'])
                    userName = (getUser[0]['firstName']) + " " + (getUser[0]['lastName'])

                    self.root.get_screen('main').ids.textInputUserID.text = userID
                    self.root.get_screen('main').ids.textInputUserName.text = userName

                    Clock.schedule_once(self.clearTextInputItemMain, 0)

            # BOOKING - itemID input

            elif self.root.get_screen('main').ids.textInputItem.focus == True:                  # If enter pressed inside main screen inputItem box
                tempItemInput = (self.root.get_screen('main').ids.textInputItem.text)           # Get text in inputItem box
                listLength = len(self.data_tables.row_data)
                
                if listLength > 0:
                    i=0
                    while i < listLength:                                                       # Iterate through rows
                        lineData = self.data_tables.row_data[i]
                        itemID = lineData[0]                                                
        
                        if itemID == tempItemInput:                                             # If itemID found in list
                            self.root.get_screen('main').ids.textErrorMain.text = "Duplicate item"                  # Set message box
                            Clock.schedule_once(self.resetTextErrorAll, 2)                      # Clear message box after 2 seconds
                            Clock.schedule_once(self.clearTextInputItemMain, 0)                 # Clear return text input box and re-focus   
                            return                                                              # Cancel adding to list
                        i +=1                                                                   # Iterate i

                tempItemName = (itemDB.search(DBquery.itemID == tempItemInput))                 # search for item number in item database
                if tempItemName == "" or tempItemName == []:                                    # If text input blank
                    self.root.get_screen('main').ids.textErrorMain.text = "Item not found"      # Set message box
                    Clock.schedule_once(self.resetTextErrorAll, 2)                              # Clear message box after 2 seconds
                    Clock.schedule_once(self.clearTextInputItemMain, 0)                         # Clear item input text box

                else:
                    if checkboxState == False:
                        self.add_row(tempItemInput, tempItemName[0]['itemName'], '')            # add row to dataTable

                    elif checkboxState == True:
                        self.add_row(tempItemInput, tempItemName[0]['itemName'], '*')           # add row to dataTable
                        self.root.get_screen('main').ids.longTermCheckbox.state = "normal"
                        checkboxState = False

                    Clock.schedule_once(self.clearTextInputItemMain, 0)                         # run "clearTextInputItemMain" on next cycle

            # RETURNS - itemID input

            elif self.root.get_screen('returns').ids.textInputItem.focus == True:               # If enter pressed on 'Returns' screen item input box: 
                tempItemInput = (self.root.get_screen('returns').ids.textInputItem.text)        # get text in inputItem box
                tempItemName = (itemDB.search(DBquery.itemID == tempItemInput))                 # Check item number is in item database

                if tempItemName == "" or tempItemName == []:                                    # If item not in item DB
                    self.root.get_screen('returns').ids.textErrorReturn.text = "Item doesn't exist"                 # Set message box
                    Clock.schedule_once(self.resetTextErrorAll, 2)                              # Clear message box after 2 seconds
                    Clock.schedule_once(self.clearTextInputItemReturn, 0)                       # Clear return text input box and re-focus   

                else:
                    tempRead = (outDB.search(DBquery.itemID == tempItemInput))                  # Fine and store item from outDB
                    if tempRead == "" or tempRead == []:                                        # If item not in booked out DB
                        self.root.get_screen('returns').ids.textErrorReturn.text = "Item not booked out"            # Set message box
                        Clock.schedule_once(self.resetTextErrorAll, 2)                          # Clear message box after 2 seconds
                        Clock.schedule_once(self.clearTextInputItemReturn, 0)                   # Clear return text input box and re-focus

                    else:
                        tempStartDateTS = (tempRead[0]['dateID'])                               # Store date item was booked out
                        userID = (tempRead[0]['userID'])                                        # Store userID item was booked out to
                        
                        getUser = (userDB.search(DBquery.userID == userID))
                        userFirst = (getUser[0]['firstName'])
                        userLast = (getUser[0]['lastName'])
                        userName = (userFirst + " " + userLast)
                        userEmail = (getUser[0]['email'])

                        getItem = (itemDB.search(DBquery.itemID == tempItemInput)) 
                        itemName = (getItem[0]['itemName'])

                        tempStartDate = datetime.utcfromtimestamp(tempStartDateTS).strftime('%Y-%m-%d - %H:%M:%S')

                        outDB.remove(where('itemID') == tempItemInput)                          # Remove item from outDB
                        historyDB.insert({'itemID': tempItemInput,                              # Insert returned item to historyDB
                                        'userID': userID, 
                                        'userFirst': userFirst,                                 # Store name & email in case they're later removed from userDB
                                        'userLast': userLast, 
                                        'email': userEmail,
                                        'startDate': tempStartDateTS, 
                                        'returnDate': datetime.timestamp(datetime.now())})

                        self.root.get_screen('returns').ids.returnBoxItemID.text += tempItemInput + "\n"
                        self.root.get_screen('returns').ids.returnBoxItemName.text += itemName + "\n"
                        self.root.get_screen('returns').ids.returnBoxUserName.text += userName + "\n"
                        self.root.get_screen('returns').ids.returnBoxUserEmail.text += userEmail + "\n"
                        self.root.get_screen('returns').ids.returnBoxDate.text += tempStartDate + "\n"

                        Clock.schedule_once(self.clearTextInputItemReturn, 0)                   # Clear return text input box and re-focus
            
            # ADD USER - userID input

            elif self.root.get_screen('addUser').ids.textInputAddUserID.focus == True:
                tempUserInput = self.root.get_screen('addUser').ids.textInputAddUserID.text
                tempUserID = (userDB.search(DBquery.userID == tempUserInput))

                if tempUserID:
                    self.root.get_screen('addUser').ids.textErrorAddUser.text = "User ID already exists"
                    Clock.schedule_once(self.resetTextErrorAll, 2)
                    Clock.schedule_once(self.addUserClear, 0)

                else:
                    Clock.schedule_once(self.addUserToUserFirstName, 0)

            # ADD USER - userFirstName input

            elif self.root.get_screen('addUser').ids.textInputAddUserFirstName.focus == True:
                Clock.schedule_once(self.addUserToUserLastName, 0)

            # ADD USER - userLastName input

            elif self.root.get_screen('addUser').ids.textInputAddUserLastName.focus == True:
                Clock.schedule_once(self.addUserToUserEmail, 0)

            # ADD USER - userEmail input

            elif self.root.get_screen('addUser').ids.textInputAddUserEmail.focus == True:
                self.addUserSave()
            
            # ADD ITEM - itemID input

            elif self.root.get_screen('addItem').ids.textInputAddItemID.focus == True:

                tempItemInput = self.root.get_screen('addItem').ids.textInputAddItemID.text
                tempItemID = (itemDB.search(DBquery.itemID == tempItemInput))

                if tempItemID:
                    self.root.get_screen('addItem').ids.textErrorAddItem.text = "Item ID already exists"
                    Clock.schedule_once(self.resetTextErrorAll, 2)
                    Clock.schedule_once(self.addItemClear, 0)

                else:
                    Clock.schedule_once(self.addItemToSerialNo, 0)

            # ADD ITEM - itemSerial input

            elif self.root.get_screen('addItem').ids.textInputAddItemSerialNo.focus == True:
                Clock.schedule_once(self.addItemToItemName, 0)

            # ADD ITEM - itemName input

            elif self.root.get_screen('addItem').ids.textInputAddItemName.focus == True:
                Clock.schedule_once(self.addItemToItemMake, 0)

            # ADD ITEM - itemMake input

            elif self.root.get_screen('addItem').ids.textInputAddItemMake.focus == True:
                Clock.schedule_once(self.addItemToItemModel, 0)

            # ADD ITEM - itemModel input

            #elif self.root.get_screen('addItem').ids.textInputAddItemModel.focus == True:
            #    Clock.schedule_once(self.addItemToSerialNo, 0)

            elif self.root.get_screen('history').ids.textInputHistoryItemID.focus == True:
                historyItemID = self.root.get_screen('history').ids.textInputHistoryItemID.text
                historyUserEmail = ""
                self.root.get_screen('history').ids.textInputhistoryUserEmail.text = ""
                self.goToScreenHistory()

            elif self.root.get_screen('history').ids.textInputhistoryUserEmail.focus == True:
                historyUserEmail = self.root.get_screen('history').ids.textInputhistoryUserEmail.text
                historyItemID = ""
                self.root.get_screen('history').ids.textInputHistoryItemID.text = ""
                self.goToScreenHistory()

        elif keycode == 43:                                                                         # on "tab" key pressed
            if self.root.get_screen('main').ids.textInputUserID.focus == True:
                self.root.get_screen('main').ids.textInputUserName.focus = True
                self.root.get_screen('main').ids.textInputUserName.text = ""
            elif self.root.get_screen('main').ids.textInputUserName.focus == True:
                self.root.get_screen('main').ids.textInputUserEmail.focus = True
                self.root.get_screen('main').ids.textInputUserEmail.text = ""
            elif self.root.get_screen('main').ids.textInputUserEmail.focus == True:
                self.root.get_screen('main').ids.textInputUserID.focus = True
                self.root.get_screen('main').ids.textInputUserID.text = ""
            
            Clock.schedule_once(self.clearInputs, 0)
            
    def clearInputs(self, dt):
        self.root.get_screen('main').ids.textInputUserName.text = ""
        self.root.get_screen('main').ids.textInputUserEmail.text = ""
        self.root.get_screen('main').ids.textInputUserID.text = ""

    def showNamesList(self, userNameList):
        global showNamesList
        longestName = 0

        if not showNamesList:
            showNamesList = True
            self.uiDict['box_list'].clear_widgets()
            
            for userName in userNameList:
                if len(userName) > longestName:
                    longestName = len(userName)

                button = Button(text=userName, size_hint_y=None, height='50dp')
                button.bind(on_release=self.on_btn_user_release)
                self.uiDict['box_list'].add_widget(button)
                
            nameWidth = (14*longestName)
            userNameListLength = len(userNameList)

            if userNameListLength > 10:
                userNameListLength = 10

            self.root.get_screen('main').ids.userListDD.pos_hint={"center_y": (1-(userNameListLength * 0.05)), "center_x": 0.5}
            self.root.get_screen('main').ids.userListDD.size_hint=(0.2, (userNameListLength * 0.08))

            if platform == "win32" or platform == "Windows" or platform == "win":
                self.root.get_screen('main').ids.box_list.size = (nameWidth + 100, 0)
            else:
                self.root.get_screen('main').ids.box_list.size = (nameWidth + 100, 0)
        else:
            showNamesList = False
            self.root.get_screen('main').ids.userListDD.pos_hint={"center_y": 2, "center_x": 20}
            self.uiDict['box_list'].clear_widgets()

    def on_btn_user_release(self, btn):
        global showNamesList

        userName = btn.text
        self.root.get_screen('main').ids.textInputUserName.text = userName
        userNameSplit = userName.split()

        getUser = userDB.search((where('firstName').matches(userNameSplit[0])) & (where('lastName').matches(userNameSplit[-1])))
        
        userID = (getUser[0]['userID'])
        userEmail = (getUser[0]['email'])

        self.root.get_screen('main').ids.textInputUserID.text = userID
        self.root.get_screen('main').ids.textInputUserEmail.text = userEmail

        showNamesList = False
        
        self.root.get_screen('main').ids.userListDD.pos_hint={"center_y": 2, "center_x": 20}
        self.uiDict['box_list'].clear_widgets()
        Clock.schedule_once(self.clearTextInputItemMain, 0)
        #self.root.ids.scroll_view.scroll_y = 0

    def processOutgoing(self):
        global userID

        currentDate = datetime.timestamp(datetime.now())
        listLength = len(self.data_tables.row_data)

        if listLength == 0:
            self.root.get_screen('main').ids.textErrorMain.text = "List empty"

        else:
            i=0
            while i < listLength:
                lineData = self.data_tables.row_data[i]
                itemID = lineData[0]
                longTerm = lineData[2]

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

            self.remove_all_rows()
            Clock.schedule_once(self.resetTextInputItemMain, 0)                                     # run "clearTextInputItemMain" on next cycle

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

    def clearTextInputItemMain(self, dt):
        self.root.get_screen('main').ids.textInputItem.text = ""                                    # clear input item box
        self.root.get_screen('main').ids.textInputItem.focus = True                                 # set focus to input item box
    
    def resetTextInputItemMain(self, dt):
        global showNamesList
        showNamesList = False
        self.root.get_screen('main').ids.textInputUserID.text = ""                                  # clear input item box
        self.root.get_screen('main').ids.textInputItem.text = ""                            
        self.root.get_screen('main').ids.textInputUserName.text = ""
        self.root.get_screen('main').ids.textInputUserEmail.text = ""
        self.root.get_screen('main').ids.textInputUserID.focus = True                               # set focus to input item box
        self.uiDict['box_list'].clear_widgets()

    def resetTextErrorAll(self, dt):
        self.root.get_screen('main').ids.textErrorMain.text = ""                                    # clear input item box
        self.root.get_screen('returns').ids.textErrorReturn.text = ""                               # clear input item box
        self.root.get_screen('addUser').ids.textErrorAddUser.text = ""                              # clear input item box
        self.root.get_screen('addItem').ids.textErrorAddItem.text = ""                              # clear input item box

    def clearTextInputItemReturn(self, dt):
        self.root.get_screen('returns').ids.textInputItem.text = ""                                 # clear input item box
        self.root.get_screen('returns').ids.textInputItem.focus = True                              # set focus to input item box

    def clearAllItemReturn(self, dt):
        self.root.get_screen('returns').ids.textInputItem.text = ""                                 # clear input item box
        self.root.get_screen('returns').ids.returnBoxItemID.text = ""
        self.root.get_screen('returns').ids.returnBoxItemName.text = ""
        self.root.get_screen('returns').ids.returnBoxUserName.text = ""
        self.root.get_screen('returns').ids.returnBoxUserEmail.text = ""
        self.root.get_screen('returns').ids.returnBoxDate.text = ""
        self.root.get_screen('returns').ids.textInputItem.focus = True                              # set focus to input item box

    def goToScreenMain(self):
        global dateRangeFrom
        global dateRangeTo
        global historyItemID
        global historyUserEmail

        historyItemID = ""
        historyUserEmail = ""
        self.root.get_screen('history').ids.textInputhistoryUserEmail.text = ""
        self.root.get_screen('history').ids.textInputHistoryItemID.text = ""
        dateRangeFrom = 0
        dateRangeTo = 0

        self.root.current = "main"
        self.remove_all_rows()
        Clock.schedule_once(self.resetTextInputItemMain, 0)

    def goToScreenReturn(self):
        global dateRangeFrom
        global dateRangeTo
        global historyItemID
        global historyUserEmail

        historyItemID = ""
        historyUserEmail = ""
        self.root.get_screen('history').ids.textInputhistoryUserEmail.text = ""
        self.root.get_screen('history').ids.textInputHistoryItemID.text = ""
        dateRangeFrom = 0
        dateRangeTo = 0

        self.root.current = "returns"
        Clock.schedule_once(self.clearAllItemReturn, 0)

    def goToScreenbookedOut(self):
        global bookedOutPath
        global dateRangeFrom
        global dateRangeTo
        global showLongTerm
        global historyItemID
        global historyUserEmail

        historyItemID = ""
        historyUserEmail = ""
        self.root.get_screen('history').ids.textInputhistoryUserEmail.text = ""
        self.root.get_screen('history').ids.textInputHistoryItemID.text = ""
        dateRangeFrom = 0
        dateRangeTo = 0

        self.root.current = "bookedout"
        outText = outDB.all()
        DBLength = len(outDB)

        pdf = FPDF('P', 'pt', 'A4')
        pdf.add_page()
        pdf.set_font('helvetica', size=7)

        self.root.get_screen('bookedout').ids.fillerLeft.text = ""
        self.root.get_screen('bookedout').ids.bookedOutBoxItemID.text = ""
        self.root.get_screen('bookedout').ids.bookedOutBoxItemName.text = ""
        self.root.get_screen('bookedout').ids.bookedOutBoxUserName.text = ""
        self.root.get_screen('bookedout').ids.bookedOutBoxUserEmail.text = ""
        self.root.get_screen('bookedout').ids.bookedOutBoxDate.text = ""

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

            getUser = (userDB.search(DBquery.userID == userID))
            userName = (getUser[0]['firstName']) + " " + (getUser[0]['lastName'])
            userEmail = (getUser[0]['email'])

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

                self.root.get_screen('bookedout').ids.fillerLeft.text += longTerm + "\n"
                self.root.get_screen('bookedout').ids.bookedOutBoxItemID.text += itemID + "\n"
                self.root.get_screen('bookedout').ids.bookedOutBoxItemName.text += itemName + "\n"
                self.root.get_screen('bookedout').ids.bookedOutBoxUserName.text += userName + "\n"
                self.root.get_screen('bookedout').ids.bookedOutBoxUserEmail.text += userEmail + "\n"
                self.root.get_screen('bookedout').ids.bookedOutBoxDate.text += dateOut + "\n"

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

                self.root.get_screen('bookedout').ids.fillerLeft.text += "\n"
                self.root.get_screen('bookedout').ids.bookedOutBoxItemID.text += itemID + "\n"
                self.root.get_screen('bookedout').ids.bookedOutBoxItemName.text += itemName + "\n"
                self.root.get_screen('bookedout').ids.bookedOutBoxUserName.text += userName + "\n"
                self.root.get_screen('bookedout').ids.bookedOutBoxUserEmail.text += userEmail + "\n"
                self.root.get_screen('bookedout').ids.bookedOutBoxDate.text += dateOut + "\n"

            i +=1
            if flipPDFBackground:
                flipPDFBackground = False
            else:
                flipPDFBackground = True

        pdf.output(bookedOutPath)

    def goToScreenHistory(self):
        global historyPath
        global dateRangeFrom
        global dateRangeTo
        global historyItemID
        global historyUserEmail

        self.root.current = "history"

        if historyItemID == "":
            if historyUserEmail == "":
                if dateRangeFrom > 0:
                    historyText = historyDB.search((DBquery.startDate > dateRangeFrom) & (DBquery.startDate <= dateRangeTo))
                else:
                    dateRangeTo = datetime.timestamp(datetime.now())
                    dateRangeFrom = datetime.timestamp(datetime.now() - timedelta(days=28))
                    historyText = historyDB.search((DBquery.startDate > dateRangeFrom) & (DBquery.startDate <= dateRangeTo))

                    self.root.get_screen('history').ids.historyFromDatePicker.text = datetime.utcfromtimestamp(dateRangeFrom).strftime('%Y-%m-%d')
                    self.root.get_screen('history').ids.historyToDatePicker.text = datetime.utcfromtimestamp(dateRangeTo).strftime('%Y-%m-%d')

            else:
                if dateRangeFrom > 0:
                    historyText = historyDB.search((DBquery.startDate > dateRangeFrom) & (DBquery.startDate <= dateRangeTo) & (DBquery.email == historyUserEmail))
                else:
                    dateRangeTo = datetime.timestamp(datetime.now())
                    dateRangeFrom = datetime.timestamp(datetime.now() - timedelta(days=28))
                    historyText = historyDB.search((DBquery.startDate > dateRangeFrom) & (DBquery.startDate <= dateRangeTo) & (DBquery.email == historyUserEmail))

                    self.root.get_screen('history').ids.historyFromDatePicker.text = datetime.utcfromtimestamp(dateRangeFrom).strftime('%Y-%m-%d')
                    self.root.get_screen('history').ids.historyToDatePicker.text = datetime.utcfromtimestamp(dateRangeTo).strftime('%Y-%m-%d')

        else:
            if dateRangeFrom > 0:
                historyText = historyDB.search((DBquery.startDate > dateRangeFrom) & (DBquery.startDate <= dateRangeTo) & (DBquery.itemID == historyItemID))
            else:
                dateRangeTo = datetime.timestamp(datetime.now())
                dateRangeFrom = datetime.timestamp(datetime.now() - timedelta(days=28))
                historyText = historyDB.search((DBquery.startDate > dateRangeFrom) & (DBquery.startDate <= dateRangeTo) & (DBquery.itemID == historyItemID))

                self.root.get_screen('history').ids.historyFromDatePicker.text = datetime.utcfromtimestamp(dateRangeFrom).strftime('%Y-%m-%d')
                self.root.get_screen('history').ids.historyToDatePicker.text = datetime.utcfromtimestamp(dateRangeTo).strftime('%Y-%m-%d')
            
        DBLength = len(historyText)

        pdf = FPDF('P', 'pt', 'A4')
        pdf.add_page()
        pdf.set_font('helvetica', size=7)

        self.root.get_screen('history').ids.historyBoxItemID.text = ""
        self.root.get_screen('history').ids.historyBoxItemName.text = ""
        self.root.get_screen('history').ids.historyBoxUserName.text = ""
        self.root.get_screen('history').ids.historyBoxUserEmail.text = ""
        self.root.get_screen('history').ids.historyBoxDateOut.text = ""
        self.root.get_screen('history').ids.historyBoxDateIn.text = ""

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
                print("Item not found")
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

            self.root.get_screen('history').ids.historyBoxItemID.text += itemID + "\n"
            self.root.get_screen('history').ids.historyBoxItemName.text += itemName + "\n"
            self.root.get_screen('history').ids.historyBoxUserName.text += userName + "\n"
            self.root.get_screen('history').ids.historyBoxUserEmail.text += userEmail + "\n"
            self.root.get_screen('history').ids.historyBoxDateOut.text += dateOut + "\n"
            self.root.get_screen('history').ids.historyBoxDateIn.text += dateIn + "\n"

            i +=1

        pdf.output(historyPath)

    def goToScreenAddUser(self):
        global dateRangeFrom
        global dateRangeTo
        global historyItemID
        global historyUserEmail

        historyItemID = ""
        historyUserEmail = ""
        self.root.get_screen('history').ids.textInputhistoryUserEmail.text = ""
        self.root.get_screen('history').ids.textInputHistoryItemID.text = ""
        dateRangeFrom = 0
        dateRangeTo = 0

        self.root.current = "addUser"
        self.root.get_screen('addUser').ids.textInputAddUserID.focus = True

    def goToScreenAddItem(self):
        global dateRangeFrom
        global dateRangeTo
        global historyItemID
        global historyUserEmail

        historyItemID = ""
        historyUserEmail = ""
        self.root.get_screen('history').ids.textInputhistoryUserEmail.text = ""
        self.root.get_screen('history').ids.textInputHistoryItemID.text = ""
        dateRangeFrom = 0
        dateRangeTo = 0

        self.root.current = "addItem"
        self.root.get_screen('addItem').ids.textInputAddItemID.focus = True
    
    def addUserToUserFirstName(self, dt):
        self.root.get_screen('addUser').ids.textInputAddUserFirstName.focus = True                  # set focus to 

    def addUserToUserLastName(self, dt):
        self.root.get_screen('addUser').ids.textInputAddUserLastName.focus = True                   # set focus to 

    def addUserToUserEmail(self, dt):
        self.root.get_screen('addUser').ids.textInputAddUserEmail.focus = True                      # set focus to 
    
    def addItemToItemName(self, dt):
        self.root.get_screen('addItem').ids.textInputAddItemName.focus = True                       # set focus to 

    def addItemToItemMake(self, dt):
        self.root.get_screen('addItem').ids.textInputAddItemMake.focus = True                       # set focus to 

    def addItemToItemModel(self, dt):
        self.root.get_screen('addItem').ids.textInputAddItemModel.focus = True                      # set focus to 

    def addItemToSerialNo(self, dt):
        self.root.get_screen('addItem').ids.textInputAddItemSerialNo.focus = True                   # set focus to 
    
    def historyDatePicker(self):
        date_dialog = MDDatePicker(mode="range")
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        global dateRangeFrom
        global dateRangeTo

        lastDateRange = len(date_range) - 1

        drf = date_range[0].timetuple()
        drt = date_range[lastDateRange].timetuple()

        dateRangeFrom = time.mktime(drf)
        dateRangeTo = time.mktime(drt)

        dateRangeFromPlus = (datetime.utcfromtimestamp(dateRangeFrom) + timedelta(days=1)).strftime('%Y-%m-%d')
        dateRangeToPlus = (datetime.utcfromtimestamp(dateRangeTo) + timedelta(days=1)).strftime('%Y-%m-%d')
        
        self.root.get_screen('history').ids.historyFromDatePicker.text = dateRangeFromPlus
        self.root.get_screen('history').ids.historyToDatePicker.text = dateRangeToPlus

        self.goToScreenHistory()

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
    
    def historyDateReset(self):
        global dateRangeFrom
        global dateRangeTo
        
        dateRangeFrom = 0
        dateRangeTo = 0

        self.goToScreenHistory()
    
    def addUserSave(self):
        addUserID = self.root.get_screen('addUser').ids.textInputAddUserID.text
        addUserFirstName = self.root.get_screen('addUser').ids.textInputAddUserFirstName.text
        addUserLastName = self.root.get_screen('addUser').ids.textInputAddUserLastName.text
        addUserEmail = self.root.get_screen('addUser').ids.textInputAddUserEmail.text

        userDB.insert({'userID': addUserID,                                                         # Insert returned item to itemDB
                        'firstName': addUserFirstName, 
                        'lastName': addUserLastName, 
                        'email': addUserEmail})
        
        self.root.get_screen('addUser').ids.textErrorAddUser.text = "User added"
        Clock.schedule_once(self.resetTextErrorAll, 2)
        Clock.schedule_once(self.addUserClear, 0)
        
    def addUserClear(self, dt):
        self.root.get_screen('addUser').ids.textInputAddUserID.text = ""
        self.root.get_screen('addUser').ids.textInputAddUserFirstName.text = ""
        self.root.get_screen('addUser').ids.textInputAddUserLastName.text = ""
        self.root.get_screen('addUser').ids.textInputAddUserEmail.text = ""
        self.root.get_screen('addUser').ids.textInputAddUserID.focus = True
    
    def addItemSave(self):
        addItemID = self.root.get_screen('addItem').ids.textInputAddItemID.text
        addItemName = self.root.get_screen('addItem').ids.textInputAddItemName.text
        addItemMake = self.root.get_screen('addItem').ids.textInputAddItemMake.text
        addItemModel = self.root.get_screen('addItem').ids.textInputAddItemModel.text
        addItemSerial = self.root.get_screen('addItem').ids.textInputAddItemSerialNo.text

        itemDB.insert({'itemID': addItemID,                                                         # Insert returned item to itemDB
                        'itemName': addItemName, 
                        'itemMake': addItemMake, 
                        'itemModel': addItemModel, 
                        'serialNo': addItemSerial})
        
        self.root.get_screen('addItem').ids.textErrorAddItem.text = "Item added"
        Clock.schedule_once(self.resetTextErrorAll, 2)
        Clock.schedule_once(self.addItemClearSome, 0)
        
    def addItemClear(self, dt):
        self.root.get_screen('addItem').ids.textInputAddItemID.text = ""
        self.root.get_screen('addItem').ids.textInputAddItemName.text = ""
        self.root.get_screen('addItem').ids.textInputAddItemMake.text = ""
        self.root.get_screen('addItem').ids.textInputAddItemModel.text = ""
        self.root.get_screen('addItem').ids.textInputAddItemSerialNo.text = ""
        self.root.get_screen('addItem').ids.textInputAddItemID.focus = True
        
    def addItemClearSome(self, dt):
        self.root.get_screen('addItem').ids.textInputAddItemID.text = ""
        self.root.get_screen('addItem').ids.textInputAddItemSerialNo.text = ""
        self.root.get_screen('addItem').ids.textInputAddItemID.focus = True

MainApp().run()