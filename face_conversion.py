import requests, json
from config import KAKAO_REST_KEY

def detect_face(url):
    API_URL = 'https://kapi.kakao.com/v1/vision/face/detect'
    headers = {'Authorization': 'KakaoAK {}'.format(KAKAO_REST_KEY)}
    data = {'image_url': url}
    response = requests.post(API_URL, data=data, headers=headers)
    print(response.json())

detect_face("https://img.hankyung.com/photo/201912/2019122820250418689-540x360.jpg")    