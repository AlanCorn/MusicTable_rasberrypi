# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        self.list = QtWidgets.QListWidget(MainWindow)
        self.list.setGeometry(QtCore.QRect(10, 170, 371, 231))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.list.setFont(font)
        self.list.setObjectName("list")
        self.label = QtWidgets.QLabel(MainWindow)
        self.label.setGeometry(QtCore.QRect(10, 140, 91, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(MainWindow)
        self.label_3.setGeometry(QtCore.QRect(140, 30, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(MainWindow)
        self.label_4.setGeometry(QtCore.QRect(500, 130, 111, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(MainWindow)
        self.label_5.setGeometry(QtCore.QRect(10, 10, 110, 110))
        self.label_5.setMouseTracking(False)
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("../assets/album.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.artist = QtWidgets.QLabel(MainWindow)
        self.artist.setGeometry(QtCore.QRect(140, 70, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.artist.setFont(font)
        self.artist.setText("")
        self.artist.setObjectName("artist")
        self.searchMusicBtn = QtWidgets.QPushButton(MainWindow)
        self.searchMusicBtn.setGeometry(QtCore.QRect(400, 150, 86, 33))
        self.searchMusicBtn.setObjectName("searchMusicBtn")
        self.results = QtWidgets.QListWidget(MainWindow)
        self.results.setGeometry(QtCore.QRect(500, 170, 281, 231))
        self.results.setObjectName("results")
        self.addToList = QtWidgets.QPushButton(MainWindow)
        self.addToList.setGeometry(QtCore.QRect(400, 370, 86, 33))
        self.addToList.setAutoFillBackground(False)
        self.addToList.setObjectName("addToList")
        self.label_6 = QtWidgets.QLabel(MainWindow)
        self.label_6.setGeometry(QtCore.QRect(500, 10, 111, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.avatarLabel = QtWidgets.QLabel(MainWindow)
        self.avatarLabel.setGeometry(QtCore.QRect(500, 40, 81, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.avatarLabel.setFont(font)
        self.avatarLabel.setText("")
        self.avatarLabel.setScaledContents(True)
        self.avatarLabel.setObjectName("avatarLabel")
        self.nicknameLabel = QtWidgets.QLabel(MainWindow)
        self.nicknameLabel.setGeometry(QtCore.QRect(620, 100, 161, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.nicknameLabel.setFont(font)
        self.nicknameLabel.setObjectName("nicknameLabel")
        self.musicProgress = QtWidgets.QProgressBar(MainWindow)
        self.musicProgress.setGeometry(QtCore.QRect(140, 110, 271, 8))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.musicProgress.sizePolicy().hasHeightForWidth())
        self.musicProgress.setSizePolicy(sizePolicy)
        self.musicProgress.setMaximumSize(QtCore.QSize(16777215, 8))
        self.musicProgress.setProperty("value", 0)
        self.musicProgress.setTextVisible(False)
        self.musicProgress.setObjectName("musicProgress")
        self.layoutWidget = QtWidgets.QWidget(MainWindow)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 420, 561, 41))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.prebutton = QtWidgets.QPushButton(self.layoutWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../assets/左.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.prebutton.setIcon(icon)
        self.prebutton.setObjectName("prebutton")
        self.horizontalLayout.addWidget(self.prebutton)
        self.playbutton = QtWidgets.QPushButton(self.layoutWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../assets/暂停.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playbutton.setIcon(icon1)
        self.playbutton.setObjectName("playbutton")
        self.horizontalLayout.addWidget(self.playbutton)
        self.nextbutton = QtWidgets.QPushButton(self.layoutWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../assets/右.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nextbutton.setIcon(icon2)
        self.nextbutton.setObjectName("nextbutton")
        self.horizontalLayout.addWidget(self.nextbutton)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.label_7 = QtWidgets.QLabel(MainWindow)
        self.label_7.setGeometry(QtCore.QRect(420, 100, 71, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setKerning(False)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.loginBtn = QtWidgets.QPushButton(MainWindow)
        self.loginBtn.setGeometry(QtCore.QRect(400, 230, 86, 33))
        self.loginBtn.setObjectName("loginBtn")
        self.closeBtn = QtWidgets.QPushButton(MainWindow)
        self.closeBtn.setGeometry(QtCore.QRect(400, 270, 86, 33))
        self.closeBtn.setObjectName("closeBtn")
        self.clearList = QtWidgets.QPushButton(MainWindow)
        self.clearList.setGeometry(QtCore.QRect(340, 130, 41, 33))
        self.clearList.setObjectName("clearList")
        self.deleteListItem = QtWidgets.QPushButton(MainWindow)
        self.deleteListItem.setGeometry(QtCore.QRect(290, 130, 41, 33))
        self.deleteListItem.setObjectName("deleteListItem")
        self.gesture = QtWidgets.QPushButton(MainWindow)
        self.gesture.setGeometry(QtCore.QRect(400, 190, 86, 33))
        self.gesture.setObjectName("gesture")
        self.volumeValue = QtWidgets.QSlider(MainWindow)
        self.volumeValue.setGeometry(QtCore.QRect(650, 420, 131, 21))
        self.volumeValue.setOrientation(QtCore.Qt.Horizontal)
        self.volumeValue.setObjectName("volumeValue")
        self.label_2 = QtWidgets.QLabel(MainWindow)
        self.label_2.setGeometry(QtCore.QRect(610, 420, 41, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.slienceBtn = QtWidgets.QPushButton(MainWindow)
        self.slienceBtn.setGeometry(QtCore.QRect(400, 310, 86, 33))
        self.slienceBtn.setObjectName("slienceBtn")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "点歌台"))
        self.label.setText(_translate("MainWindow", "播放列表"))
        self.label_3.setText(_translate("MainWindow", "暂无歌曲"))
        self.label_4.setText(_translate("MainWindow", "搜索结果"))
        self.searchMusicBtn.setText(_translate("MainWindow", "语音搜索"))
        self.addToList.setText(_translate("MainWindow", "<<加入列表"))
        self.label_6.setText(_translate("MainWindow", "登录状态"))
        self.nicknameLabel.setText(_translate("MainWindow", "未登录"))
        self.pushButton_2.setText(_translate("MainWindow", "快退5s"))
        self.prebutton.setText(_translate("MainWindow", "上一首"))
        self.playbutton.setText(_translate("MainWindow", "暂停/播放"))
        self.nextbutton.setText(_translate("MainWindow", "下一首"))
        self.pushButton.setText(_translate("MainWindow", "快进5s"))
        self.label_7.setText(_translate("MainWindow", "0:00/0:00"))
        self.loginBtn.setText(_translate("MainWindow", "登录网易云"))
        self.closeBtn.setText(_translate("MainWindow", "关闭窗口"))
        self.clearList.setText(_translate("MainWindow", "清空"))
        self.deleteListItem.setText(_translate("MainWindow", "删除"))
        self.gesture.setText(_translate("MainWindow", "打开手势"))
        self.label_2.setText(_translate("MainWindow", "音量"))
        self.slienceBtn.setText(_translate("MainWindow", "一键静音"))
