# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/amalik/Documents/listener/src/python/mainGUI.ui',
# licensing of '/home/amalik/Documents/listener/src/python/mainGUI.ui' applies.
#
# Created: Fri Apr 16 12:15:45 2021
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1060, 810)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 810))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.view3d = QtWidgets.QWidget(self.centralwidget)
        self.view3d.setGeometry(QtCore.QRect(530, 70, 511, 421))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.view3d.sizePolicy().hasHeightForWidth())
        self.view3d.setSizePolicy(sizePolicy)
        self.view3d.setObjectName("view3d")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(430, 10, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 610, 1031, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(430, 650, 141, 61))
        self.lcdNumber.setDigitCount(6)
        self.lcdNumber.setObjectName("lcdNumber")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(430, 630, 191, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(550, 510, 291, 16))
        self.label_3.setObjectName("label_3")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 30, 511, 571))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.ip = QtWidgets.QLineEdit(self.tab)
        self.ip.setGeometry(QtCore.QRect(50, 450, 301, 21))
        self.ip.setObjectName("ip")
        self.port = QtWidgets.QLineEdit(self.tab)
        self.port.setGeometry(QtCore.QRect(50, 490, 301, 21))
        self.port.setObjectName("port")
        self.connect = QtWidgets.QPushButton(self.tab)
        self.connect.setGeometry(QtCore.QRect(380, 450, 80, 23))
        self.connect.setObjectName("connect")
        self.Quit = QtWidgets.QPushButton(self.tab)
        self.Quit.setGeometry(QtCore.QRect(380, 490, 80, 23))
        self.Quit.setObjectName("Quit")
        self.liveStr = QtWidgets.QWidget(self.tab)
        self.liveStr.setGeometry(QtCore.QRect(10, 10, 491, 421))
        self.liveStr.setObjectName("liveStr")
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(10, 450, 21, 20))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.tab)
        self.label_6.setGeometry(QtCore.QRect(10, 490, 41, 16))
        self.label_6.setObjectName("label_6")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(30, 510, 301, 21))
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(self.tab_2)
        self.pushButton.setGeometry(QtCore.QRect(350, 510, 141, 21))
        self.pushButton.setObjectName("pushButton")
        self.MplGraphics = MplGraphics(self.tab_2)
        self.MplGraphics.setGeometry(QtCore.QRect(10, 10, 491, 421))
        self.MplGraphics.setObjectName("MplGraphics")
        self.ip2 = QtWidgets.QLineEdit(self.tab_2)
        self.ip2.setGeometry(QtCore.QRect(60, 440, 271, 23))
        self.ip2.setObjectName("ip2")
        self.port2 = QtWidgets.QLineEdit(self.tab_2)
        self.port2.setGeometry(QtCore.QRect(60, 470, 271, 23))
        self.port2.setObjectName("port2")
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setGeometry(QtCore.QRect(10, 450, 21, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.tab_2)
        self.label_8.setGeometry(QtCore.QRect(10, 470, 31, 16))
        self.label_8.setObjectName("label_8")
        self.startCol = QtWidgets.QPushButton(self.tab_2)
        self.startCol.setGeometry(QtCore.QRect(360, 440, 111, 23))
        self.startCol.setObjectName("startCol")
        self.stopCol = QtWidgets.QPushButton(self.tab_2)
        self.stopCol.setGeometry(QtCore.QRect(360, 470, 111, 23))
        self.stopCol.setObjectName("stopCol")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1060, 20))
        self.menubar.setObjectName("menubar")
        self.menuGUI = QtWidgets.QMenu(self.menubar)
        self.menuGUI.setObjectName("menuGUI")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuGUI.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Clarius User Interface", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Current Encoder Reading", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "Image in 3D space with angle orientation", None, -1))
        self.connect.setText(QtWidgets.QApplication.translate("MainWindow", "Connect", None, -1))
        self.Quit.setText(QtWidgets.QApplication.translate("MainWindow", "Quit", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("MainWindow", "IP", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("MainWindow", "Port", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtWidgets.QApplication.translate("MainWindow", "Tab 1", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("MainWindow", "View Offline Data by clicking Open SliceViewer", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("MainWindow", "Open SliceViewer", None, -1))
        self.label_7.setText(QtWidgets.QApplication.translate("MainWindow", "IP", None, -1))
        self.label_8.setText(QtWidgets.QApplication.translate("MainWindow", "Port", None, -1))
        self.startCol.setText(QtWidgets.QApplication.translate("MainWindow", "Start Collection", None, -1))
        self.stopCol.setText(QtWidgets.QApplication.translate("MainWindow", "Stop Collection", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtWidgets.QApplication.translate("MainWindow", "Tab 2", None, -1))
        self.menuGUI.setTitle(QtWidgets.QApplication.translate("MainWindow", "GUI", None, -1))

from clariusGUI import MplGraphics

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

