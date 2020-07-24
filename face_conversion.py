import requests, json
from config import KAKAO_REST_KEY
import time
import random

'''
Returns a json object that contains the face infos in image.
Refer https://developers.kakao.com/docs/latest/ko/vision/dev-guide#recog-face
for more details.
'''
def detect_face(url):
    API_URL = 'https://kapi.kakao.com/v1/vision/face/detect'
    headers = {'Authorization': 'KakaoAK {}'.format(KAKAO_REST_KEY)}
    data = {'image_url': url}
    response = requests.post(API_URL, data=data, headers=headers)
    return (response.json())

'''
Downloads an image from url and returns the random-generated image name.
If url has no image or access is invalid, return None.
'''
def download_image(url):
    response = requests.get(url, allow_redirects=True)

    # Check type of image
    contentType = response.headers["Content-Type"]
    if (contentType == "image/png"):
        mimeType = "png"
    elif (contentType == "image/jpeg"):
        mimeType = "jpg"
    else:
        return None
    
    # Randomly generate filename
    timestamp = int(time.time())
    randomString = int(random.random()*1E9)
    fileName = "{:d}-{:d}.{:s}".format(timestamp, randomString, mimeType)
    with open("./static/{}".format(fileName), 'wb') as f:
        f.write(response.content)
    return fileName
    

detect_face("https://img.hankyung.com/photo/201912/2019122820250418689-540x360.jpg")    