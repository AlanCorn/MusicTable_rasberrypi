import sys
from pprint import pprint

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QCoreApplication
from PyQt5.QtWidgets import QWidget, QAction

from api import getCaptcha, loginCaptcha, loginStatus, searchMusic
from player import Player
from record import ASR as listenASR
from ui.loginDialog import Ui_Dialog as Ui_LoginDialog
from ui.ui import Ui_MainWindow


# 主窗口类
class myWindow(Ui_MainWindow):
    def __init__(self, Dialog):
        super().setupUi(Dialog)
        # 实例化播放器
        self.mediaPlayer = Player()
        self.loginDialog = LoginDialog()
        self.mediaPlayer.set_uri("https://music.163.com/song/media/outer/url?id=33894312.mp3")

        self.playbutton.clicked.connect(self.playAndPause)
        self.loginBtn.clicked.connect(self.showDialog)
        self.closeBtn.clicked.connect(QCoreApplication.instance().quit)

        self.searchMusicBtn.clicked.connect(self.searchMusicName)
        # userStatus = QTimer(self.loginDialog)
        # userStatus.timeout.connect(self.flushStatus)
        # userStatus.start(1000)

    def flushStatus(self):
        userid = loginStatus()
        pprint(userid)

    def addItemToResults(self, musicList):
        for each in musicList:
            item = QtWidgets.QListWidgetItem()
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setText(each)
            self.results.addItem(item)

    def playAndPause(self):
        if self.mediaPlayer.is_playing():
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def showDialog(self):
        self.loginDialog.show()

    def searchMusicName(self):
        name = listenASR()
        print("识别到的音乐名", name)
        result = searchMusic(name)
        print("搜索结果", result)
        # 将搜索结果加入 Results
        myWindowObj.addItemToResults(["海阔天空ddddd"])


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
        myWindowObj.avatarLabel.setPixmap(QtGui.QPixmap(res['profile']['avatarUrl']))
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
