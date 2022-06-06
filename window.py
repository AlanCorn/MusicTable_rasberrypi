import sys
from operator import mod
from pprint import pprint

import requests
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer, QCoreApplication
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget

from api import getCaptcha, loginCaptcha, music_list
from player import Player
from record import ASR as listenASR
from ui.loginDialog import Ui_Dialog as Ui_LoginDialog
from ui.ui import Ui_MainWindow


# 主窗口类
class myWindow(Ui_MainWindow):
    def __init__(self, Dialog):
        self.musicResultsList = []  # 搜索结果
        self.currentPlaying = -1  # 正在播放
        self.currentPosition = 0
        self.musicPlaylists = [{'name': '海阔天空',
                                'singer': 'Beyond',
                                'song_url': 'http://m8.music.126.net/20220606105627/2f1d8f15c3fa32575f39ca8748838ef5/ymusic/7cbb/a3a8/58c3/bc8284e8ee123ec77f4b1c0918579dbb.mp3',
                                'picurl': 'http://p4.music.126.net/t40uccdajHS_-KkUHm_aEA==/109951166888743768.jpg'
                                },
                               {'name': '晴天',
                                'singer': '拾七',
                                'song_url': 'http://m801.music.126.net/20220606103322/4df0adb40cad2d2048a86ad3d421644e/jdymusic/obj/wo3DlMOGwrbDjj7DisKw/9519144606/afb7/7b58/d442/e182958cf0c618e2eff359204d971b80.mp3',
                                'picurl': 'http://p3.music.126.net/yXxROcrQ_CLI7AOo3DrbDA==/109951166115397076.jpg'
                                }]  # 播放列表

        super().setupUi(Dialog)
        # 实例化播放器
        self.mediaPlayer = Player()
        self.loginDialog = LoginDialog()
        # 播放列表操作按钮
        self.clearList.clicked.connect(self.clearPlayList)
        self.deleteListItem.clicked.connect(self.deletePlayListItem)
        # 媒体控制按钮
        self.playbutton.clicked.connect(self.playCurrentMusic)
        self.prebutton.clicked.connect(self.playPreMusic)
        self.nextbutton.clicked.connect(self.playNextMusic)
        # 添加到播放列表
        self.addToList.clicked.connect(self.addToMusicPlaylists)
        self.searchMusicBtn.clicked.connect(self.searchMusicName)
        # 登录与关闭
        self.loginBtn.clicked.connect(self.showDialog)
        self.closeBtn.clicked.connect(QCoreApplication.instance().quit)
        # 每秒刷新进度条
        progressBar_Slot = QTimer(MainWindow)
        progressBar_Slot.timeout.connect(self.reloadProgressBar)
        progressBar_Slot.start(1000)
        self.reloadPlayList()

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
        if self.currentPlaying != -1:
            url = self.musicPlaylists[self.currentPlaying]['picurl']
            res = requests.get(url)
            img = QImage.fromData(res.content)
            self.label_5.setPixmap(QPixmap.fromImage(img))
            self.label_3.setText(self.musicPlaylists[self.currentPlaying]['name'])
            self.artist.setText(self.musicPlaylists[self.currentPlaying]['singer'])

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
        self.musicResultsList = result
        myWindowObj.addItemToResults()

    def playCurrentMusic(self):
        if self.list.count() > 0:
            if self.currentPlaying == -1 or self.currentPlaying >= self.list.count():
                self.currentPlaying = 0  # 超出范围,跳到第一首
        else:
            self.currentPlaying = -1
        if self.currentPlaying != -1:
            print("get_state", self.mediaPlayer.get_state())
            print("is_playing", self.mediaPlayer.is_playing())
            if self.mediaPlayer.get_state() == 0:
                self.mediaPlayer.play()
            elif self.mediaPlayer.get_state() == 1:
                self.mediaPlayer.pause()
            else:
                self.mediaPlayer.set_uri(self.musicPlaylists[self.currentPlaying]['song_url'])
                self.mediaPlayer.play()

    def playPreMusic(self):
        if self.currentPlaying != -1:
            self.mediaPlayer.release()
            self.currentPlaying = mod(self.currentPlaying + self.list.count() - 1,
                                      self.list.count())  # 上一首，如果没有上一首就是最后一首，循环
            self.playCurrentMusic()

    def playNextMusic(self):
        if self.currentPlaying != -1:
            self.mediaPlayer.release()
            self.currentPlaying = mod(self.currentPlaying + self.list.count() + 1, self.list.count())  # 同理
            self.playCurrentMusic()

    def jumpPre5s(self):
        self.mediaPlayer.set_time(self.mediaPlayer.get_time() - 5000)

    def jumpNext5s(self):
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    myWindowObj = myWindow(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
