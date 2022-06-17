# MusicTable_rasberrypi
## 基于百度智能云、网易云API的树莓派家庭桌面语音点歌台  
> 嵌入式大作业
## 🎼 项目简介

本项目通过树莓派Raspberry  Pi、摄像头、USB麦克风、HDMI显示屏，来实现家庭点歌台的实现，可以实现对歌曲的播放暂停以及切换歌曲还有快进快退的操作，并在此基础上嵌入了语音识别搜索歌曲功能，另外还加入了手势识别，可以让使用者隔空进行对播放的操作。并且配备了精美简洁的GUI界面，可以让使用者触屏操作，方便使用者，并给予实时的反馈。

## ⚙️ 硬件模块

- 树莓派Raspberry Pi
- 摄像头 
- USB麦克风  
- HDMI显示屏(800*400)

## 📖 运行环境

```shell
# python库
pip install baidu-aip
pip install PyQt5
pip install PyAudio
pip install python-vlc
pip install requests
# vlc
sudo apt install vlc
```

