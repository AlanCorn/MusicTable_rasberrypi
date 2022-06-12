import json
from pprint import pprint
import requests

baseUrl = 'http://116.62.129.37:3000'

search = '/cloudsearch'  # 搜索
playUrl = '/song/url'  # 获取播放url
captchaGet = '/captcha/sent'  # 获取验证码
captchaLogin = '/login/cellphone'  # 使用手机验证码登录
StatusLogin = '/login/status'
Detail = '/user/detail'


# 歌曲搜索
def searchMusic(keywords):
    result = requests.get(baseUrl + search, params={
        'keywords': keywords,
        'type': 1
    }).content
    result = json.loads(str(result, 'utf-8'))
    # pprint(result)
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
    pprint(result)
    return result


def userDetail(id):
    result = requests.get(baseUrl + search, params={
        'uid': id,
    }).content
    result = json.loads(str(result, 'utf-8'))
    pprint(result)
    return result


def music_list(song_name):
    result_song_list = []
    songlist = searchMusic(song_name)
    song_list = songlist['result']['songs']
    for i, item in enumerate(song_list):
        item = json.dumps(item)
        id = json.loads(str(item))['id']
        musicurl = json.loads(str(getMusicUrl(id), 'utf-8'))['data'][0]['url']
        result_song_list.append(
            dict(name=json.loads(str(item))['name'], singer=json.loads(str(item))['ar'][0]['name'], song_url=musicurl,
                 picurl=json.loads(str(item))['al']['picUrl']))
    for i in result_song_list:
        print(i)
    return result_song_list


# music_list("海阔天空")