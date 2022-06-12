import cv2
from aip import AipBodyAnalysis

APP_ID = '26426973'
API_KEY = 'QzdYvxkeL4jGZf7pYm2wofx4'
SECRET_KEY = 'Ul1Qe2h96omGBAi9LWMnTyioC8Ng2wEF'

hand = {'One': '数字1', 'Five': '数字5', 'Fist': '拳头', 'Ok': 'OK',
        'Prayer': '祈祷', 'Congratulation': '作揖', 'Honour': '作别',
        'Heart_single': '比心心', 'Thumb_up': '点赞', 'Thumb_down': 'Diss',
        'ILY': '我爱你', 'Palm_up': '掌心向上', 'Heart_1': '双手比心1',
        'Heart_2': '双手比心2', 'Heart_3': '双手比心3', 'Two': '数字2',
        'Three': '数字3', 'Four': '数字4', 'Six': '数字6', 'Seven': '数字7',
        'Eight': '数字8', 'Nine': '数字9', 'Rock': 'Rock', 'Insult': '竖中指', 'Face': '脸'}

gesture_client = AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)  # 手势识别
capture = cv2.VideoCapture(0)  # 0为默认摄像头


def gesture_recognition():
    resultList = []
    # 第一个参数ret 为True 或者False,代表有没有读取到图片
    # 第二个参数frame表示截取到一帧的图片
    for i in range(10):
        try:
            ret, frame = capture.read()
            # 图片格式转换
            image = cv2.imencode('.jpg', frame)[1]

            gesture = gesture_client.gesture(image)  # AipBodyAnalysis内部函数
            words = gesture['result'][0]['classname']
            if hand[words] != "脸":
                resultList.append(hand[words])
            print(hand[words])
        except:
            print('未检测到识别对象')
    if len(resultList) != 0:
        result = max(resultList, key=resultList.count)
        if resultList.count(result) > 2:
            return result
        else:
            return "识别失败"
    else:
        return "识别失败"

