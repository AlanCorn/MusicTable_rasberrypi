import wave
from urllib.request import Request

import pyaudio
from aip import AipSpeech
from pprint import pprint

import requests
import base64
import json
import time
import hashlib


def record(sec):
    # 定义数据流块
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    # 想要百度识别，下面这两参数必须这样设置，使得比特率为256kbps
    CHANNELS = 1
    RATE = 16000
    # 录音时间
    RECORD_SECONDS = sec
    # 要写入的文件名
    WAVE_OUTPUT_FILENAME = "./assets/output.wav"
    # 创建PyAudio对象
    p = pyaudio.PyAudio()

    # 打开数据流
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    # 开始录音
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")
    # 停止数据流
    stream.stop_stream()
    stream.close()

    # 关闭PyAudio
    p.terminate()

    # 写入录音文件
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    result = b''.join(frames)
    wf.writeframes(result)
    wf.close()
    return result


# 语音识别
def ASR():
    # 录音5秒，识别出文字
    record(5)

    """ 你的 APPID AK SK """
    APP_ID = '26351908'
    API_KEY = 'OGlQKe5v0iLbL6oCwng18kZC'
    SECRET_KEY = 'AizOlO9rD3UzmdFP9AiPlFf9wlIKaaUr'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # 读取文件
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    # 识别本地文件
    res = client.asr(get_file_content('./assets/output.wav'), 'wav', 16000, {
        'dev_pid': 1536,
    })

    if not res.get("err_no"):
        print(res)
        return res.get("result")[0]
    return res.get("err_no")


# 听歌识曲
def SongReco():
    record(20)
    # 在控制台获取appid等信息
    appid = "cafb4a7d"
    apikey = "a9743f46db3cdfa33be6dede43282e91"

    file = open('./assets/output.wav', 'rb')
    info = file.read()                      # 音频二进制数据


    baseUrl = "http://webqbh.xfyun.cn/v1/service/v1/qbh"
    curtime = str(int(time.time()))
    print(curtime)
    # 使用audio_url传输音频数据时，http request body须为空。
    # 直接把音频二进制数据写入到Http Request Body时，不需要设置audio_url参数
    param = {
        "aue": "raw",
        "sample_rate": "16000"
    }
    base64_param = base64.urlsafe_b64encode(json.dumps(param).encode('utf-8'))
    tt = str(base64_param, 'utf-8')
    m2 = hashlib.md5()
    m2.update((apikey + curtime + tt).encode('utf-8'))
    checksum = m2.hexdigest()

    header = {
        "X-CurTime": curtime,
        "X-Appid": appid,
        "X-CheckSum": checksum,
    }

    res = Request(baseUrl, info, header).data
    print(res)



    # result = res.content
    jsonData = res.decode("utf-8")
    pprint(jsonData)
    # pprint(jsonData)

    # return jsonData


if __name__ == '__main__':
    SongReco()
