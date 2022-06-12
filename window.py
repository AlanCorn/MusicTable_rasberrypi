import ctypes
import sys
from asyncio import run
from operator import mod
from pprint import pprint
import threading

import requests
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer, QCoreApplication
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget

from api import getCaptcha, loginCaptcha, music_list
from player import VlcPlayer
from record import ASR as listenASR
from gesture import gesture_recognition
from ui.loginDialog import Ui_Dialog as Ui_LoginDialog
from ui.ui import Ui_MainWindow


# 主窗口类
class myWindow(Ui_MainWindow):
    def __init__(self, Dialog):
        self.gestureThread = None
        super().setupUi(Dialog)
        self.musicResultsList = []  # 搜索结果
        self.currentPlaying = -1  # 正在播放
        self.currentPosition = 0  # 播放列表控件中的位置
        self.volume = 100  # 音量
        self.musicPlaylists = []  # 播放列表
        # 实例化VLC播放器
        self.mediaPlayer = VlcPlayer()
        self.mediaPlayer.set_volume(self.volume)
        # 实例化登录对话框
        self.loginDialog = LoginDialog()
        # 播放列表操作按钮点击事件监听
        self.clearList.clicked.connect(self.clearPlayList)
        self.deleteListItem.clicked.connect(self.deletePlayListItem)
        # 媒体控制按钮点击事件监听
        self.playbutton.clicked.connect(self.playCurrentMusic)
        self.prebutton.clicked.connect(self.playPreMusic)
        self.nextbutton.clicked.connect(self.playNextMusic)
        self.pushButton.clicked.connect(self.jumpNext5s)
        self.pushButton_2.clicked.connect(self.jumpPre5s)
        # 添加到播放列表按钮点击事件监听
        self.addToList.clicked.connect(self.addToMusicPlaylists)
        self.searchMusicBtn.clicked.connect(self.searchMusicName)
        # 登录与关闭按钮
        self.loginBtn.clicked.connect(self.showDialog)
        self.closeBtn.clicked.connect(QCoreApplication.instance().quit)
        # 打开手势按钮
        self.gestureBtn.clicked.connect(self.gestureChanged)
        # 每100毫秒刷新进度条
        progressBar_Slot = QTimer(MainWindow)
        progressBar_Slot.timeout.connect(self.reloadProgressBar)
        progressBar_Slot.start(100)
        # 静音按钮
        self.slienceBtn.clicked.connect(self.setSilence)
        # 音量滑块设置
        self.volumeValue.setMinimum(0)
        self.volumeValue.setMaximum(100)
        self.volumeValue.setValue(100)
        # 音量滑块变动信号监听
        self.volumeValue.valueChanged.connect(self.volumeChanged)

    def volumeChanged(self):
        self.volume = self.volumeValue.value()
        self.mediaPlayer.set_volume(self.volume)

    def setSilence(self):
        self.volume = 0
        self.volumeValue.setValue(self.volume)
        self.mediaPlayer.set_volume(self.volume)

    def gestureChanged(self):
        if self.gestureBtn.text() == "打开手势":
            print("### 打开手势操作 ###")
            self.gestureBtn.setText("关闭手势")
            self.gestureThread = gestureThread()
            self.gestureThread.start()
        else:
            print("### 关闭手势操作 ###")
            self.gestureThread.setStopFlag()
            self.gestureBtn.setText("打开手势")

    def reloadProgressBar(self):
        if self.mediaPlayer.get_state() == 1:
            wholeTime = self.mediaPlayer.get_length() / 1000
            nowTime = self.mediaPlayer.get_time() / 1000
            nowMin = int(nowTime / 60)
            nowSec = int(mod(nowTime, 60))
            wholeMin = int(wholeTime / 60)
            wholeSec = int(mod(wholeTime, 60))
            position = self.mediaPlayer.get_position()
            self.musicProgress.setValue(int(position * 100))
            self.currentPosition = self.mediaPlayer.get_position()
            self.label_7.setText(
                str(nowMin) + ":" + str(nowSec).zfill(2) + "/" + str(wholeMin) + ":" + str(wholeSec).zfill(2))

    def reloadPlayList(self):
        self.list.clear()
        for each in self.musicPlaylists:
            tmpStr = each['name'] + '-' + each['singer']
            self.list.addItem(tmpStr)

    def addItemToResults(self):
        # 清除搜索列表
        self.results.clear()
        for each in self.musicResultsList:
            tmpStr = each['name'] + '-' + each['singer']
            item = QtWidgets.QListWidgetItem()
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setText(tmpStr)
            self.results.addItem(item)

    def addToMusicPlaylists(self):
        # 将勾选的的搜索结果添加到播放队列中
        for i in range(self.results.count()):
            print(self.results.item(i).checkState())  # 2 是被选中
            if self.results.item(i).checkState() == 2:
                self.musicPlaylists.append(self.musicResultsList[i])
                self.results.item(i).setCheckState(QtCore.Qt.Unchecked)
        self.reloadPlayList()

    def showDialog(self):
        self.loginDialog.show()

    def searchMusicName(self):
        name = listenASR()
        print("识别到的音乐名", name)
        result = music_list(name)
        # 将搜索结果加入 musicResultsList
        if name != "3307":
            self.musicResultsList = result
            myWindowObj.addItemToResults()
        else:
            self.nicknameLabel.setText("识别失败")

    def playCurrentMusic(self):
        if self.list.count() > 0:
            if self.currentPlaying == -1 or self.currentPlaying >= self.list.count():
                self.currentPlaying = 0  # 超出范围,跳到第一首
        else:
            self.currentPlaying = -1
        if self.currentPlaying != -1:
            if self.mediaPlayer.get_state() == 0:
                self.mediaPlayer.play()
            elif self.mediaPlayer.get_state() == 1:
                self.mediaPlayer.pause()
            else:
                url = self.musicPlaylists[self.currentPlaying]['picurl']
                res = requests.get(url)
                img = QImage.fromData(res.content)
                self.label_5.setPixmap(QPixmap.fromImage(img))
                self.label_3.setText(self.musicPlaylists[self.currentPlaying]['name'])
                self.artist.setText(self.musicPlaylists[self.currentPlaying]['singer'])
                self.mediaPlayer.set_uri(self.musicPlaylists[self.currentPlaying]['song_url'])
                self.mediaPlayer.play()

    def playPreMusic(self):
        if self.currentPlaying != -1:
            self.mediaPlayer.release()
            self.currentPlaying = mod(self.currentPlaying + self.list.count() - 1,
                                      self.list.count())  # 上一首，如果没有上一首就是最后一首，循环

            self.mediaPlayer = VlcPlayer()
            self.mediaPlayer.set_volume(self.volume)
            # self.mediaPlayer.set_uri(self.musicPlaylists[self.currentPlaying]['song_url'])
            self.playCurrentMusic()
        if self.currentPlaying != -1:
            url = self.musicPlaylists[self.currentPlaying]['picurl']
            res = requests.get(url)
            img = QImage.fromData(res.content)
            self.label_5.setPixmap(QPixmap.fromImage(img))
            self.label_3.setText(self.musicPlaylists[self.currentPlaying]['name'])
            self.artist.setText(self.musicPlaylists[self.currentPlaying]['singer'])

    def playNextMusic(self):
        if self.currentPlaying != -1:
            self.mediaPlayer.release()
            self.currentPlaying = mod(self.currentPlaying + self.list.count() + 1, self.list.count())  # 同理
            # self.mediaPlayer.set_uri(self.musicPlaylists[self.currentPlaying]['song_url'])
            self.mediaPlayer = VlcPlayer()
            self.mediaPlayer.set_volume(self.volume)
            self.playCurrentMusic()
        if self.currentPlaying != -1:
            url = self.musicPlaylists[self.currentPlaying]['picurl']
            res = requests.get(url)
            img = QImage.fromData(res.content)
            self.label_5.setPixmap(QPixmap.fromImage(img))
            self.label_3.setText(self.musicPlaylists[self.currentPlaying]['name'])
            self.artist.setText(self.musicPlaylists[self.currentPlaying]['singer'])

    def jumpPre5s(self):
        if self.mediaPlayer.is_playing() == 1:
            self.mediaPlayer.set_time(self.mediaPlayer.get_time() - 5000)

    def jumpNext5s(self):
        if self.mediaPlayer.is_playing() == 1:
            self.mediaPlayer.set_time(self.mediaPlayer.get_time() + 5000)

    def clearPlayList(self):
        self.list.clear()

    def deletePlayListItem(self):
        print("删除行", self.list.currentRow())
        self.list.takeItem(self.list.currentRow())


class LoginDialog(QWidget, Ui_LoginDialog):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        # 设置正在编辑的edit框
        self.editing = self.phone
        self.buttonGetCode.setEnabled(True)
        # 数字虚拟键盘列表
        btnlist = [self.pushButton_0,
                   self.pushButton_1,
                   self.pushButton_2,
                   self.pushButton_3,
                   self.pushButton_4,
                   self.pushButton_5,
                   self.pushButton_6,
                   self.pushButton_7,
                   self.pushButton_8,
                   self.pushButton_9]
        for each in btnlist:
            each.clicked.connect(self.input)

        self.pushButton_x.clicked.connect(self.delete)
        self.buttonGetCode.clicked.connect(self.getCode)

    def accept(self):
        phone = self.phone.text()
        captcha = self.code.text()
        res = loginCaptcha(phone.strip(), captcha.strip())
        pprint(res)
        url = res['profile']['avatarUrl']
        res2 = requests.get(url)
        img = QImage.fromData(res2.content)
        myWindowObj.avatarLabel.setPixmap(QPixmap.fromImage(img))
        myWindowObj.nicknameLabel.setText(res['profile']['nickname'])
        self.hide()
        print("accepted")

    def reject(self):
        self.hide()
        print("rejected")

    def input(self):
        num = 0
        sender = self.sender()
        if sender == self.pushButton_0:
            num = 0
        elif sender == self.pushButton_1:
            num = 1
        elif sender == self.pushButton_2:
            num = 2
        elif sender == self.pushButton_3:
            num = 3
        elif sender == self.pushButton_4:
            num = 4
        elif sender == self.pushButton_5:
            num = 5
        elif sender == self.pushButton_6:
            num = 6
        elif sender == self.pushButton_7:
            num = 7
        elif sender == self.pushButton_8:
            num = 8
        elif sender == self.pushButton_9:
            num = 9
        self.editing.setText(self.editing.text() + str(num))

    def delete(self):
        self.editing.setText(self.editing.text()[0:-1])

    def focusInEvent(self, QFocusEvent):
        print(self.sender() == self.phone)

    def focusOutEvent(self, QFocusEvent):
        self.sender()

    def getCode(self):
        # 调用获取验证码Api
        phone = self.phone.text()
        pprint(getCaptcha(phone.strip()))
        print("phone", phone)
        self.buttonGetCode.setEnabled(False)
        self.editing = self.code


class gestureThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        self.stopFlag = 0

    def run(self):
        try:
            while self.stopFlag == 0:
                result = gesture_recognition()
                print("# 手势识别结果：", result)
                if self.stopFlag == 0:
                    if result == "比心心":
                        myWindowObj.addItemToResults()
                    elif result == "数字1":
                        myWindowObj.jumpPre5s()
                    elif result == "数字2":
                        myWindowObj.playPreMusic()
                    elif result == "数字3":
                        myWindowObj.playCurrentMusic()
                    elif result == "数字4":
                        myWindowObj.playNextMusic()
                    elif result == "数字5":
                        myWindowObj.jumpNext5s()
                    elif result == "Fist":
                        myWindowObj.setSilence()
                    elif result == "Fist":
                        myWindowObj.setSilence()
                    else:
                        pass
        finally:
            print("线程关闭")

    def setStopFlag(self):
        self.stopFlag = 1




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    myWindowObj = myWindow(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
