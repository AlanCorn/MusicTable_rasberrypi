import wave
import pyaudio
from aip import AipSpeech


def record():
    # 定义数据流块
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    # 想要百度识别，下面这两参数必须这样设置，使得比特率为256kbps
    CHANNELS = 1
    RATE = 16000
    # 录音时间
    RECORD_SECONDS = 5
    # 要写入的文件名
    WAVE_OUTPUT_FILENAME = "output.wav"
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
    wf.writeframes(b''.join(frames))
    wf.close()


def ASR():
    # 录音
    record()

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
    res = client.asr(get_file_content('output.wav'), 'wav', 16000, {
        'dev_pid': 1536,
    })

    if not res.get("err_no"):
        print(res)
        return res.get("result")[0]
    return res.get("err_no")


if __name__ == '__main__':
    result = ASR()
