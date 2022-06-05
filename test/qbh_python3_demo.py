from operator import mod
from pprint import pprint

import requests
import base64
import json
import time
import hashlib

#
# class demo:
#     def __init__(self):
#         self.url = "http://webqbh.xfyun.cn/v1/service/v1/qbh"
#         self.AUDIO_URL = AUDIO_URL
#
#     def music_iat(self):
#         # 在控制台获取appid等信息
#         appid = "cafb4a7d"
#         apikey = "a9743f46db3cdfa33be6dede43282e91"
#
#         curtime = str(int(time.time()))
#         print(curtime)
#         # 使用audio_url传输音频数据时，http request body须为空。
#         # 直接把音频二进制数据写入到Http Request Body时，不需要设置audio_url参数
#         param = {
#             "audio_url": self.AUDIO_URL
#         }
#         base64_param = base64.urlsafe_b64encode(json.dumps(param).encode('utf-8'))
#         tt = str(base64_param, 'utf-8')
#         m2 = hashlib.md5()
#         m2.update((apikey + curtime + tt).encode('utf-8'))
#         checksum = m2.hexdigest()
#
#         header = {
#             "X-CurTime": curtime,
#             "X-Param": base64_param,
#             "X-Appid": appid,
#             "X-CheckSum": checksum,
#         }
#
#         res = requests.post(self.url, headers=header)
#         print(res)
#         result = res.content
#         jsonData = json.loads(result.decode("utf-8"))
#         pprint(jsonData)
#
#
#
# if __name__ == "__main__":
#
#     # 音频url地址
#     AUDIO_URL = "https://xfyun-doc.cn-bj.ufileos.com/1537253485018707/qlzw2.wav"
#
#     demo = demo()
#     demo.music_iat()


print(mod(5,3))