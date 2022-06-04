import json
from pprint import pprint
import requests

baseUrl = 'http://116.62.129.37:3000'

search = '/cloudsearch'  # 搜索
playUrl = '/song/url'  # 获取播放url
captchaGet = '/captcha/sent'  # 获取验证码
captchaLogin = '/login/cellphone'  # 使用手机验证码登录
StatusLogin = '/login/status'


# 歌曲搜索
def searchMusic(keywords):
    result = requests.get(baseUrl + search, params={
        'keywords': keywords,
        'type': 1
    }).content
    result = json.loads(str(result, 'utf-8'))
    return result


# 专辑搜索
def searchAlbums():
    pass


# 听歌识曲
def searchSing():
    pass


def getMusicUrl(musicId):
    return requests.get(baseUrl + playUrl, params={
        'id': musicId
    }).content


def getCaptcha(phone):
    result = requests.get(baseUrl + captchaGet, params={
        'phone': phone
    }).content
    result = json.loads(str(result, 'utf-8'))
    return result


def loginCaptcha(phone, captcha):
    print(phone, captcha)
    result = requests.get(baseUrl + captchaLogin, params={
        'phone': phone,
        'password': '123',
        'captcha': captcha
    }).content
    result = json.loads(str(result, 'utf-8'))
    return result


def loginStatus():
    result = requests.get(baseUrl + StatusLogin).content
    result = json.loads(str(result, 'utf-8'))
    return result
